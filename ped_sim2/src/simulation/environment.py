"""
Environment class managing the simulation space, obstacles, and zones.
"""
import numpy as np
from typing import List, Tuple, Dict


class Environment:
    """Represents the simulation environment with walls, entrances, and exits."""
    
    def __init__(self, width: float = 50.0, height: float = 50.0):
        """
        Initialize environment.
        
        Args:
            width: Environment width in meters
            height: Environment height in meters
        """
        self.width = width
        self.height = height
        self.walls = []  # List of wall segments [(start, end), ...]
        self.entrances = []  # List of entrance zones [(center, radius, flow_rate), ...]
        self.exits = []  # List of exit zones [(center, radius), ...]
        self.hazard_zones = []  # Emergency hazards [(center, radius, type), ...]
        self.blocked_entrances = set()  # Set of blocked entrance indices
        self.roads = []  # List of road segments
        self.decorations = []  # List of decorative elements (trees, ponds, etc.)
        
    def add_wall(self, start: Tuple[float, float], end: Tuple[float, float]):
        """
        Add a wall segment.
        
        Args:
            start: Wall start point (x, y)
            end: Wall end point (x, y)
        """
        self.walls.append([np.array(start), np.array(end)])
    
    def add_entrance(self, position: Tuple[float, float], radius: float = 1.0, 
                     flow_rate: float = 2.0):
        """
        Add an entrance point.
        
        Args:
            position: Entrance center (x, y)
            radius: Entrance radius
            flow_rate: Pedestrians per second spawning rate
        """
        self.entrances.append({
            'position': np.array(position),
            'radius': radius,
            'flow_rate': flow_rate,
            'active': True
        })
    
    def add_exit(self, position: Tuple[float, float], radius: float = 1.5):
        """
        Add an exit point.
        
        Args:
            position: Exit center (x, y)
            radius: Exit radius
        """
        self.exits.append({
            'position': np.array(position),
            'radius': radius,
            'active': True
        })
    
    def add_hazard_zone(self, position: Tuple[float, float], radius: float, 
                       hazard_type: str = 'fire'):
        """
        Add a hazard zone (fire, incident, etc.).
        
        Args:
            position: Hazard center (x, y)
            radius: Hazard radius
            hazard_type: Type of hazard ('fire', 'shooting', 'obstacle')
        """
        self.hazard_zones.append({
            'position': np.array(position),
            'radius': radius,
            'type': hazard_type,
            'intensity': 1.0
        })
    
    def block_entrance(self, entrance_idx: int):
        """Block an entrance (emergency closure)."""
        if 0 <= entrance_idx < len(self.entrances):
            self.entrances[entrance_idx]['active'] = False
            self.blocked_entrances.add(entrance_idx)
    
    def unblock_entrance(self, entrance_idx: int):
        """Unblock an entrance."""
        if 0 <= entrance_idx < len(self.entrances):
            self.entrances[entrance_idx]['active'] = True
            self.blocked_entrances.discard(entrance_idx)
    
    def block_exit(self, exit_idx: int):
        """Block an exit (emergency closure)."""
        if 0 <= exit_idx < len(self.exits):
            self.exits[exit_idx]['active'] = False
    
    def unblock_exit(self, exit_idx: int):
        """Unblock an exit."""
        if 0 <= exit_idx < len(self.exits):
            self.exits[exit_idx]['active'] = True
    
    def remove_hazard(self, hazard_idx: int):
        """Remove a hazard zone."""
        if 0 <= hazard_idx < len(self.hazard_zones):
            self.hazard_zones.pop(hazard_idx)
    
    def is_point_in_hazard(self, position: np.ndarray) -> Tuple[bool, float]:
        """
        Check if point is in any hazard zone.
        
        Args:
            position: Point to check [x, y]
            
        Returns:
            Tuple of (is_in_hazard, panic_level)
        """
        max_panic = 0.0
        
        for hazard in self.hazard_zones:
            distance = np.linalg.norm(position - hazard['position'])
            if distance < hazard['radius']:
                # Panic increases closer to hazard center
                panic = hazard['intensity'] * (1.0 - distance / hazard['radius'])
                max_panic = max(max_panic, panic)
        
        return max_panic > 0, max_panic
    
    def get_nearest_exit(self, position: np.ndarray) -> np.ndarray:
        """
        Find the nearest active exit to a position.
        
        Args:
            position: Current position [x, y]
            
        Returns:
            Position of nearest exit
        """
        active_exits = [e for e in self.exits if e['active']]
        
        if not active_exits:
            # No active exits, return center of environment
            return np.array([self.width / 2, self.height / 2])
        
        min_distance = float('inf')
        nearest_exit = active_exits[0]['position']
        
        for exit_zone in active_exits:
            distance = np.linalg.norm(position - exit_zone['position'])
            if distance < min_distance:
                min_distance = distance
                nearest_exit = exit_zone['position']
        
        return nearest_exit
    
    def get_alternative_exit(self, position: np.ndarray, blocked_exit: np.ndarray) -> np.ndarray:
        """
        Find an alternative exit when the current target is blocked.
        
        Args:
            position: Current position [x, y]
            blocked_exit: The exit to avoid [x, y]
            
        Returns:
            Position of alternative exit
        """
        active_exits = [e for e in self.exits if e['active']]
        
        if not active_exits:
            return np.array([self.width / 2, self.height / 2])
        
        # Filter out the blocked exit (with some tolerance)
        alternative_exits = []
        for exit_zone in active_exits:
            distance_to_blocked = np.linalg.norm(exit_zone['position'] - blocked_exit)
            if distance_to_blocked > 2.0:  # More than 2m away from blocked exit
                alternative_exits.append(exit_zone)
        
        if not alternative_exits:
            # If all exits are near the blocked one, return the farthest one
            alternative_exits = active_exits
        
        # Find nearest alternative exit
        min_distance = float('inf')
        best_exit = alternative_exits[0]['position']
        
        for exit_zone in alternative_exits:
            distance = np.linalg.norm(position - exit_zone['position'])
            if distance < min_distance:
                min_distance = distance
                best_exit = exit_zone['position']
        
        return best_exit
    
    def is_path_blocked_by_hazard(self, start: np.ndarray, end: np.ndarray) -> bool:
        """
        Check if a straight line path is blocked by any hazard.
        
        Args:
            start: Start position [x, y]
            end: End position [x, y]
            
        Returns:
            True if path intersects any hazard zone
        """
        for hazard in self.hazard_zones:
            hazard_pos = hazard['position']
            hazard_radius = hazard['radius']
            
            # Calculate distance from hazard center to line segment
            line_vec = end - start
            line_len = np.linalg.norm(line_vec)
            
            if line_len < 0.01:
                # Start and end are the same point
                distance = np.linalg.norm(start - hazard_pos)
                if distance < hazard_radius:
                    return True
                continue
            
            line_dir = line_vec / line_len
            
            # Vector from start to hazard center
            to_hazard = hazard_pos - start
            
            # Project onto line
            projection = np.dot(to_hazard, line_dir)
            projection = np.clip(projection, 0, line_len)
            
            # Closest point on line to hazard center
            closest_point = start + line_dir * projection
            
            # Distance from hazard center to closest point
            distance = np.linalg.norm(closest_point - hazard_pos)
            
            if distance < hazard_radius:
                return True
        
        return False
    
    def get_walls_as_segments(self) -> List[np.ndarray]:
        """Get all wall segments."""
        return self.walls
    
    def get_traffic_light_state(self, position: np.ndarray, direction: np.ndarray) -> Tuple[bool, str]:
        """
        Check if pedestrian should stop at traffic light before entering crossing.
        
        Args:
            position: Current pedestrian position
            direction: Direction pedestrian is moving
            
        Returns:
            Tuple of (should_stop, reason)
        """
        if not hasattr(self, 'traffic_lights') or not hasattr(self, 'crossing_lanes'):
            return (False, "")
        
        if np.linalg.norm(direction) < 0.01:
            return (False, "")
        
        # Normalize direction
        dir_normalized = direction / np.linalg.norm(direction)
        
        # Check each crossing lane
        for crossing in self.crossing_lanes:
            start = np.array(crossing['start'])
            end = np.array(crossing['end'])
            width = crossing.get('width', 4)
            
            # Calculate crossing vector and direction
            crossing_vec = end - start
            if np.linalg.norm(crossing_vec) < 0.01:
                continue
            crossing_dir = crossing_vec / np.linalg.norm(crossing_vec)
            crossing_length = np.linalg.norm(crossing_vec)
            
            # Check if pedestrian's movement direction aligns with crossing
            # (moving parallel to the crossing)
            alignment = abs(np.dot(dir_normalized, crossing_dir))
            
            # Only check if moving parallel to crossing (alignment > 0.7)
            if alignment > 0.7:
                # Project pedestrian position onto crossing line
                to_ped = position - start
                proj_on_crossing = np.dot(to_ped, crossing_dir)
                
                # Check if pedestrian is within lateral bounds of crossing (with 5m buffer)
                # Expanded buffer to catch pedestrians approaching from outside crossing area
                lateral_buffer = 5.0
                if -lateral_buffer <= proj_on_crossing <= crossing_length + lateral_buffer:
                    # Calculate perpendicular distance to crossing line
                    # Perpendicular vector (rotate crossing_dir by 90°)
                    perp_vec = np.array([-crossing_dir[1], crossing_dir[0]])
                    perp_dist_signed = np.dot(to_ped, perp_vec)
                    perp_dist = abs(perp_dist_signed)
                    
                    # CRITICAL: If pedestrian is within the crossing width (on the zebra crossing),
                    # NEVER stop them - let them finish crossing regardless of light state
                    if perp_dist < width/2.0:
                        # Debug: Show when we skip stopping someone on the crossing
                        if np.random.random() < 0.005:  # 0.5% sampling
                            print(f"ON CROSSING: Ped at [{position[0]:.1f},{position[1]:.1f}] on {crossing.get('trafficLightId', 'unknown')}, perp_dist={perp_dist:.2f} < {width/2.0:.2f}, allowing to continue")
                        continue  # Skip this crossing, don't stop them
                    
                    # Check if approaching (moving toward crossing, not away)
                    moving_toward = np.dot(dir_normalized, perp_vec) * perp_dist_signed < 0
                    
                    # Stop line: 3m before crossing edge (5m from center)
                    stop_distance = width/2.0 + 3.0
                    
                    # Only check pedestrians in the approach zone (between crossing edge and stop line)
                    # perp_dist is between width/2 (2m) and stop_distance (5m)
                    in_approach_zone = perp_dist < stop_distance
                    
                    # Additional check: Pedestrian must be within crossing lateral bounds
                    # to be stopped (not just in the buffer zone)
                    # This prevents stopping pedestrians who are walking diagonally past the crossing
                    within_crossing_bounds = 0 <= proj_on_crossing <= crossing_length
                    
                    # Stop if in approach zone, moving toward crossing, and within lateral bounds
                    if in_approach_zone and moving_toward and within_crossing_bounds:
                        # Check traffic light state
                        traffic_light_id = crossing.get('trafficLightId')
                        if traffic_light_id:
                            for light in self.traffic_lights:
                                if light['id'] == traffic_light_id and light.get('state') == 'red':
                                    # Debug output for detection
                                    if np.random.random() < 0.01:  # Only print 1% of the time to avoid spam
                                        print(f"DETECTED! Ped at [{position[0]:.1f},{position[1]:.1f}] stop for {traffic_light_id}, perp_dist={perp_dist:.2f}, perp_signed={perp_dist_signed:.2f}, align={alignment:.2f}, moving_toward={moving_toward}")
                                    return (True, f"Red light at {traffic_light_id}")
        
        return (False, "")
    
    def is_on_crossing(self, position: np.ndarray) -> bool:
        """Check if position is on a crossing lane."""
        if not hasattr(self, 'crossing_lanes'):
            return False
        
        for crossing in self.crossing_lanes:
            start = np.array(crossing['start'])
            end = np.array(crossing['end'])
            width = crossing.get('width', 4)
            
            # Calculate distance from position to crossing line
            line_vec = end - start
            line_len = np.linalg.norm(line_vec)
            
            if line_len < 0.01:
                continue
            
            line_dir = line_vec / line_len
            to_point = position - start
            
            # Project position onto crossing line
            projection = np.dot(to_point, line_dir)
            
            # Check if within crossing bounds
            if 0 <= projection <= line_len:
                # Calculate perpendicular distance to line
                closest_point = start + line_dir * projection
                perp_dist = np.linalg.norm(position - closest_point)
                
                if perp_dist < width / 2:
                    return True
        
        return False
    
    def add_boundary_walls(self):
        """Add walls around the environment boundary."""
        # Top wall
        self.add_wall((0, 0), (self.width, 0))
        # Right wall
        self.add_wall((self.width, 0), (self.width, self.height))
        # Bottom wall
        self.add_wall((self.width, self.height), (0, self.height))
        # Left wall
        self.add_wall((0, self.height), (0, 0))
    
    def to_dict(self) -> dict:
        """Convert environment to dictionary for serialization."""
        return {
            'width': self.width,
            'height': self.height,
            'walls': [[w[0].tolist(), w[1].tolist()] for w in self.walls],
            'entrances': [{
                'position': e['position'].tolist(),
                'radius': e['radius'],
                'flow_rate': e['flow_rate'],
                'active': e['active']
            } for e in self.entrances],
            'exits': [{
                'position': e['position'].tolist(),
                'radius': e['radius'],
                'active': e['active']
            } for e in self.exits],
            'hazards': [{
                'position': h['position'].tolist(),
                'radius': h['radius'],
                'type': h['type'],
                'intensity': h['intensity']
            } for h in self.hazard_zones],
            'roads': self.roads,
            'decorations': self.decorations,
            'trafficLights': getattr(self, 'traffic_lights', []),
            'crossingLanes': getattr(self, 'crossing_lanes', []),
            'pedestrianLanes': getattr(self, 'pedestrian_lanes', []),
            'carLanes': getattr(self, 'car_lanes', []),
            'vehicles': getattr(self, 'vehicles', [])
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'Environment':
        """Create environment from dictionary."""
        env = Environment(data['width'], data['height'])
        
        for wall in data.get('walls', []):
            env.add_wall(tuple(wall[0]), tuple(wall[1]))
        
        for entrance in data.get('entrances', []):
            env.add_entrance(
                tuple(entrance['position']),
                entrance.get('radius', 1.0),
                entrance.get('flow_rate', 2.0)
            )
        
        for exit_zone in data.get('exits', []):
            env.add_exit(
                tuple(exit_zone['position']),
                exit_zone.get('radius', 1.5)
            )
        
        for hazard in data.get('hazards', []):
            env.add_hazard_zone(
                tuple(hazard['position']),
                hazard['radius'],
                hazard.get('type', 'fire')
            )
        
        # Store roads and decorations for later use
        env.roads = data.get('roads', [])
        env.decorations = data.get('decorations', [])
        
        # Store traffic-related elements
        env.traffic_lights = data.get('trafficLights', [])
        env.crossing_lanes = data.get('crossingLanes', [])
        env.pedestrian_lanes = data.get('pedestrianLanes', [])
        env.car_lanes = data.get('carLanes', [])
        env.vehicles = data.get('vehicles', [])
        
        return env
