"""
Main simulation controller integrating all components.
"""
import numpy as np
from typing import List, Dict, Optional
import time
import json

from .pedestrian import Pedestrian
from .social_force import SocialForceModel
from .pathfinding import PathFinder
from .environment import Environment
from .events import EventManager, EventType, Event


class Simulator:
    """Main simulation controller."""
    
    def __init__(self, environment: Environment, dt: float = 0.1):
        """
        Initialize simulator.
        
        Args:
            environment: Simulation environment
            dt: Time step size (seconds)
        """
        self.environment = environment
        self.dt = dt
        self.time = 0.0
        self.pedestrians = []
        self.next_ped_id = 0
        
        # Simulation parameters
        self.target_pedestrian_count = 100  # Default target
        self.simulation_speed = 1.0  # Playback speed multiplier
        self.exit_selection_mode = 'random'  # 'random', 'nearest', or 'weighted'
        
        # Initialize subsystems
        self.social_force = SocialForceModel()
        self.pathfinder = PathFinder(
            (environment.width, environment.height),
            cell_size=0.5
        )
        self.event_manager = EventManager()
        
        # Statistics
        self.stats = {
            'spawned': 0,
            'exited': 0,
            'active': 0,
            'total_panic': 0.0
        }
        
        # Spawn tracking
        self.spawn_timers = [0.0] * len(environment.entrances)
        
        # Setup pathfinding grid
        self._update_pathfinding_grid()
        
        # Register event callbacks
        self._register_event_callbacks()
        
        # Recording for export
        self.recording = False
        self.trajectory_data = []
    
    def select_exit_for_pedestrian(self, position: np.ndarray) -> np.ndarray:
        """
        Select an exit for a pedestrian based on the current exit selection mode.
        
        Args:
            position: Current position of the pedestrian
            
        Returns:
            Position of the selected exit
        """
        if len(self.environment.exits) == 0:
            # No exits available, return a default position
            return np.array([self.environment.width / 2, self.environment.height / 2])
        
        if self.exit_selection_mode == 'nearest':
            # Select nearest exit
            return self.environment.get_nearest_exit(position)
            
        elif self.exit_selection_mode == 'weighted':
            # Weighted random selection (closer exits more likely)
            distances = []
            for exit_zone in self.environment.exits:
                dist = np.linalg.norm(exit_zone['position'] - position)
                distances.append(dist)
            
            # Convert distances to probabilities (inverse distance)
            # Add small epsilon to avoid division by zero
            inv_distances = [1.0 / (d + 0.1) for d in distances]
            total = sum(inv_distances)
            probabilities = [inv_d / total for inv_d in inv_distances]
            
            # Select exit based on probabilities
            exit_idx = np.random.choice(len(self.environment.exits), p=probabilities)
            return self.environment.exits[exit_idx]['position']
            
        else:  # 'random' mode (default)
            # Randomly select any exit with equal probability
            exit_idx = np.random.randint(0, len(self.environment.exits))
            return self.environment.exits[exit_idx]['position']
        
    def _update_pathfinding_grid(self):
        """Update pathfinding grid with current walls."""
        for wall in self.environment.walls:
            self.pathfinder.add_wall_segment(wall[0], wall[1])
        
        # Set up roads if present
        if hasattr(self.environment, 'roads') and self.environment.roads:
            # Enable roads-only mode
            self.pathfinder.set_roads_only_mode(True)
            
            # Add all road segments to pathfinding
            for road in self.environment.roads:
                points = [tuple(p) for p in road['points']]
                width = road.get('width', 2.0)
                self.pathfinder.add_road_segment(points, width)
    
    def _register_event_callbacks(self):
        """Register callbacks for handling events."""
        self.event_manager.register_callback(
            EventType.FIRE,
            self._handle_fire_event
        )
        self.event_manager.register_callback(
            EventType.SHOOTING,
            self._handle_shooting_event
        )
        self.event_manager.register_callback(
            EventType.ENTRANCE_BLOCKED,
            self._handle_entrance_blocked
        )
        self.event_manager.register_callback(
            EventType.ENTRANCE_OPENED,
            self._handle_entrance_opened
        )
        self.event_manager.register_callback(
            EventType.EXIT_BLOCKED,
            self._handle_exit_blocked
        )
        self.event_manager.register_callback(
            EventType.EXIT_OPENED,
            self._handle_exit_opened
        )
    
    def _handle_fire_event(self, event: Event):
        """Handle fire event."""
        position = event.parameters['position']
        radius = event.parameters['radius']
        self.environment.add_hazard_zone(position, radius, 'fire')
        print(f"Fire started at {position} with radius {radius}")
        
        # Recalculate paths for all pedestrians
        self._recalculate_all_paths()
    
    def _handle_shooting_event(self, event: Event):
        """Handle shooting event."""
        position = event.parameters['position']
        radius = event.parameters['radius']
        self.environment.add_hazard_zone(position, radius, 'shooting')
        print(f"Shooting incident at {position}")
        
        # Immediately panic nearby pedestrians
        for ped in self.pedestrians:
            if ped.active:
                distance = np.linalg.norm(ped.position - np.array(position))
                if distance < radius:
                    panic_level = 1.0 - (distance / radius)
                    ped.set_panic_level(panic_level)
        
        self._recalculate_all_paths()
    
    def _handle_entrance_blocked(self, event: Event):
        """Handle entrance blocking."""
        entrance_idx = event.parameters['entrance_idx']
        self.environment.block_entrance(entrance_idx)
        print(f"Entrance {entrance_idx} blocked")
    
    def _handle_entrance_opened(self, event: Event):
        """Handle entrance opening."""
        entrance_idx = event.parameters['entrance_idx']
        self.environment.unblock_entrance(entrance_idx)
        print(f"Entrance {entrance_idx} opened")
    
    def _handle_exit_blocked(self, event: Event):
        """Handle exit blocking."""
        exit_idx = event.parameters['exit_idx']
        self.environment.block_exit(exit_idx)
        print(f"Exit {exit_idx} blocked")
        
        # Recalculate paths to find alternative exits
        self._recalculate_all_paths()
    
    def _handle_exit_opened(self, event: Event):
        """Handle exit opening."""
        exit_idx = event.parameters['exit_idx']
        self.environment.unblock_exit(exit_idx)
        print(f"Exit {exit_idx} opened")
    
    def _recalculate_all_paths(self):
        """Recalculate paths for all active pedestrians."""
        for ped in self.pedestrians:
            if ped.active and not ped.reached_goal:
                # Find new goal (nearest safe exit)
                new_goal = self.environment.get_nearest_exit(ped.position)
                path = self.pathfinder.find_path(ped.position, new_goal)
                ped.update_path(path)
                ped.goal = new_goal
    
    def spawn_pedestrian(self, entrance_idx: int) -> Optional[Pedestrian]:
        """
        Spawn a pedestrian at an entrance.
        
        Args:
            entrance_idx: Index of entrance to spawn at
            
        Returns:
            Created pedestrian or None
        """
        if entrance_idx >= len(self.environment.entrances):
            return None
        
        entrance = self.environment.entrances[entrance_idx]
        if not entrance['active']:
            return None
        
        # Random position within entrance radius
        angle = np.random.uniform(0, 2 * np.pi)
        distance = np.random.uniform(0, entrance['radius'])
        position = entrance['position'] + distance * np.array([
            np.cos(angle), np.sin(angle)
        ])
        
        # Select exit based on configured mode (random/nearest/weighted)
        goal = self.select_exit_for_pedestrian(position)
        
        print(f"Spawning ped at entrance {entrance_idx}: pos={position}, goal={goal}, distance={np.linalg.norm(goal - position):.2f}")
        
        # Create pedestrian
        ped = Pedestrian(
            self.next_ped_id,
            position,
            goal,
            max_speed=np.random.normal(1.3, 0.2)  # Vary speed
        )
        self.next_ped_id += 1
        
        # Calculate path
        path = self.pathfinder.find_path(position, goal)
        ped.update_path(path)
        
        self.pedestrians.append(ped)
        self.stats['spawned'] += 1
        
        return ped
    
    def pre_populate_pedestrians(self, count: int):
        """
        Pre-populate the map with pedestrians distributed evenly across the entire map.
        
        Args:
            count: Number of pedestrians to pre-populate
        """
        if count <= 0:
            return
        
        if len(self.environment.exits) == 0:
            return
        
        # Check if we have roads (roads-only mode)
        has_roads = hasattr(self.environment, 'roads') and len(self.environment.roads) > 0
        
        pedestrians_spawned = 0
        max_attempts = count * 10  # Prevent infinite loop
        attempts = 0
        
        while pedestrians_spawned < count and pedestrians_spawned < self.target_pedestrian_count and attempts < max_attempts:
            attempts += 1
            
            if has_roads:
                # Spawn on roads
                position = self._get_random_road_position()
            else:
                # Generate completely random position across the entire map
                # Leave margin from edges to avoid walls
                margin = 2.0
                position = np.array([
                    np.random.uniform(margin, self.environment.width - margin),
                    np.random.uniform(margin, self.environment.height - margin)
                ])
            
            # Check if position is valid (not inside a wall)
            is_valid = True
            for wall in self.environment.walls:
                wall_start = np.array(wall[0])
                wall_end = np.array(wall[1])
                
                # Calculate distance from point to line segment
                wall_vec = wall_end - wall_start
                wall_len = np.linalg.norm(wall_vec)
                if wall_len > 0:
                    wall_dir = wall_vec / wall_len
                    point_vec = position - wall_start
                    projection = np.dot(point_vec, wall_dir)
                    projection = np.clip(projection, 0, wall_len)
                    closest_point = wall_start + projection * wall_dir
                    distance = np.linalg.norm(position - closest_point)
                    
                    # Too close to wall
                    if distance < 0.5:
                        is_valid = False
                        break
            
            if not is_valid:
                continue
            
            # Select exit based on configured mode
            goal = self.select_exit_for_pedestrian(position)
            
            # Create pedestrian
            ped = Pedestrian(
                self.next_ped_id,
                position,
                goal,
                max_speed=np.random.normal(1.3, 0.2)
            )
            self.next_ped_id += 1
            
            # Calculate path
            path = self.pathfinder.find_path(position, goal)
            ped.update_path(path)
            
            # Give them initial velocity in the direction they're heading
            direction = ped.get_desired_direction()
            if np.linalg.norm(direction) > 0:
                ped.velocity = direction * np.random.uniform(0.5, 1.2) * ped.max_speed
            
            self.pedestrians.append(ped)
            self.stats['spawned'] += 1
            pedestrians_spawned += 1
        
        if pedestrians_spawned < count:
            print(f"Warning: Could only pre-populate {pedestrians_spawned} out of {count} pedestrians")
    
    def _get_random_road_position(self) -> np.ndarray:
        """Get a random position on a road."""
        if not hasattr(self.environment, 'roads') or len(self.environment.roads) == 0:
            # Fallback to center of map if no roads
            return np.array([self.environment.width / 2, self.environment.height / 2])
        
        # Pick a random road
        road = self.environment.roads[np.random.randint(0, len(self.environment.roads))]
        points = road['points']
        
        if len(points) < 2:
            return np.array(points[0])
        
        # Pick a random segment in the road
        segment_idx = np.random.randint(0, len(points) - 1)
        start = np.array(points[segment_idx])
        end = np.array(points[segment_idx + 1])
        
        # Pick a random position along the segment
        t = np.random.uniform(0.1, 0.9)  # Avoid exact endpoints
        position = start + t * (end - start)
        
        # Add small random offset perpendicular to road (within road width)
        road_width = road.get('width', 4.0)
        road_vec = end - start
        road_len = np.linalg.norm(road_vec)
        
        if road_len > 0:
            # Perpendicular vector
            perp = np.array([-road_vec[1], road_vec[0]]) / road_len
            offset = np.random.uniform(-road_width / 3, road_width / 3)
            position = position + perp * offset
        
        return position
    
    def _check_and_reroute_pedestrian(self, ped: Pedestrian):
        """
        Check if pedestrian's path is blocked by hazards and reroute if needed.
        
        Args:
            ped: Pedestrian to check and potentially reroute
        """
        # Check if current goal is still reachable or if path is blocked
        path_blocked = self.environment.is_path_blocked_by_hazard(ped.position, ped.goal)
        
        # Also check if goal itself is in a hazard zone
        goal_in_hazard, _ = self.environment.is_point_in_hazard(ped.goal)
        
        if path_blocked or goal_in_hazard:
            # Try to find alternative exit
            alternative_exit = self.environment.get_alternative_exit(ped.position, ped.goal)
            
            # Update pathfinder with current hazards
            self.pathfinder.update_hazard_zones(self.environment.hazard_zones)
            
            # Calculate new path to alternative exit
            new_path = self.pathfinder.find_path(ped.position, alternative_exit)
            
            if len(new_path) > 0:
                # Update pedestrian's goal and path
                ped.goal = alternative_exit
                ped.update_path(new_path)
                # Increase panic level due to rerouting
                ped.set_panic_level(min(1.0, ped.panic_level + 0.3))
            else:
                # If no path found, at least update the goal
                ped.goal = alternative_exit
    
    def _update_pathfinding_hazards(self):
        """Update pathfinder with current hazard zones."""
        self.pathfinder.update_hazard_zones(self.environment.hazard_zones)
    
    def _update_traffic_lights(self):
        """Update traffic light states based on simulation time."""
        if not hasattr(self.environment, 'traffic_lights'):
            return
        
        # 30 second cycle: 0-15s = NS red/EW green, 15-30s = NS green/EW red
        cycle_time = self.time % 30
        
        for light in self.environment.traffic_lights:
            controls = light.get('controls', '')
            old_state = light.get('state')
            
            if 'north-south' in controls:
                # North-South lights: green from 15-30s, red from 0-15s
                light['state'] = 'green' if cycle_time >= 15 else 'red'
            elif 'east-west' in controls:
                # East-West lights: green from 0-15s, red from 15-30s
                light['state'] = 'green' if cycle_time < 15 else 'red'
            
            # Debug: Log state changes
            if old_state != light.get('state'):
                print(f"Traffic light {light['id']} ({controls}): {old_state} -> {light['state']} at time {self.time:.1f}s (cycle: {cycle_time:.1f}s)")
    
    def step(self):
        """Execute one simulation step."""
        # Update events
        self.event_manager.update(self.time)
        
        # Update traffic lights (30 second cycle: 15s green, 15s red, alternating)
        self._update_traffic_lights()
        
        # Update pathfinder with current hazards
        if len(self.environment.hazard_zones) > 0:
            self._update_pathfinding_hazards()
        
        # Update spawn timers and spawn pedestrians (only if under target count)
        if self.stats['spawned'] < self.target_pedestrian_count:
            for i, entrance in enumerate(self.environment.entrances):
                if entrance['active']:
                    self.spawn_timers[i] += self.dt
                    spawn_interval = 1.0 / entrance['flow_rate']
                    
                    while self.spawn_timers[i] >= spawn_interval and self.stats['spawned'] < self.target_pedestrian_count:
                        self.spawn_pedestrian(i)
                        self.spawn_timers[i] -= spawn_interval
        
        # Update each pedestrian
        active_peds = [p for p in self.pedestrians if p.active]
        walls = self.environment.get_walls_as_segments()
        
        # Periodically check all pedestrians for blocked paths (every 2 seconds)
        check_rerouting = (int(self.time * 10) % 20 == 0)  # Every 2 seconds
        
        for ped in active_peds:
            # Check if in hazard zone
            in_hazard, panic_level = self.environment.is_point_in_hazard(ped.position)
            if in_hazard:
                ped.set_panic_level(panic_level)
                # Immediate reroute check when in hazard
                self._check_and_reroute_pedestrian(ped)
            elif check_rerouting and len(self.environment.hazard_zones) > 0:
                # Periodic check for all pedestrians if hazards exist
                self._check_and_reroute_pedestrian(ped)
            
            # Check traffic lights FIRST - before calculating any forces
            desired_direction = ped.get_desired_direction()
            should_stop, reason = self.environment.get_traffic_light_state(ped.position, desired_direction)
            
            # Debug: Log first few pedestrians
            if ped.id < 3 and int(self.time * 10) % 50 == 0:  # Every 5 seconds for first 3 peds
                print(f"Ped {ped.id} at [{ped.position[0]:.1f},{ped.position[1]:.1f}], dir=[{desired_direction[0]:.2f},{desired_direction[1]:.2f}], should_stop={should_stop}, reason='{reason}', panic={ped.panic_level:.2f}")
            
            # HARD STOP at red light - completely prevent movement
            # If traffic light says stop, FREEZE the pedestrian completely
            if should_stop:
                ped.velocity = np.array([0.0, 0.0])  # Zero velocity
                # Skip position update entirely - don't move at all
                continue
            
            # Calculate social forces (including hazard repulsion)
            force = self.social_force.calculate_total_force(
                ped, active_peds, walls, self.environment.hazard_zones
            )
            
            # Update position
            ped.update_position(force, self.dt)
            
            # Check if reached exit
            for exit_zone in self.environment.exits:
                if exit_zone['active']:
                    distance = np.linalg.norm(ped.position - exit_zone['position'])
                    if distance < exit_zone['radius']:
                        ped.deactivate()
                        self.stats['exited'] += 1
                        break
        
        # Update statistics
        self.stats['active'] = len(active_peds)
        self.stats['total_panic'] = sum(p.panic_level for p in active_peds)
        
        # Record frame if recording
        if self.recording:
            self._record_frame()
        
        # Advance time
        self.time += self.dt
    
    def _record_frame(self):
        """Record current frame for export."""
        frame_data = {
            'time': self.time,
            'pedestrians': [p.to_dict() for p in self.pedestrians if p.active]
        }
        self.trajectory_data.append(frame_data)
    
    def start_recording(self):
        """Start recording simulation for export."""
        self.recording = True
        self.trajectory_data = []
    
    def stop_recording(self):
        """Stop recording."""
        self.recording = False
    
    def get_state(self) -> dict:
        """Get current simulation state."""
        return {
            'time': self.time,
            'pedestrians': [p.to_dict() for p in self.pedestrians if p.active],
            'stats': self.stats.copy(),
            'environment': self.environment.to_dict(),
            'events': self.event_manager.to_dict()
        }
    
    def reset(self):
        """Reset simulation."""
        self.time = 0.0
        self.pedestrians = []
        self.next_ped_id = 0
        self.spawn_timers = [0.0] * len(self.environment.entrances)
        self.stats = {
            'spawned': 0,
            'exited': 0,
            'active': 0,
            'total_panic': 0.0
        }
        self.event_manager.clear_events()
        self.trajectory_data = []
