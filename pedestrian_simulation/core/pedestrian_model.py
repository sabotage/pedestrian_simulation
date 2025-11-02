"""
Pedestrian Movement Simulation Core Module - Based on Social Force Model
"""
import numpy as np
from dataclasses import dataclass, field
from typing import List, Tuple, Optional, Dict
from enum import Enum
import json

class PedestrianState(Enum):
    NORMAL = "normal"
    PANIC = "panic"
    EVACUATING = "evacuating"
    STOPPED = "stopped"

class EventType(Enum):
    FIRE = "fire"
    SHOOTING = "shooting"
    ENTRANCE_CLOSE = "entrance_close"
    ENTRANCE_OPEN = "entrance_open"
    OBSTACLE = "obstacle"

@dataclass
class Pedestrian:
    """Pedestrian object"""
    id: int
    position: np.ndarray  # [x, y]
    velocity: np.ndarray  # [vx, vy]
    goal: np.ndarray  # Target position
    radius: float = 0.3  # Pedestrian radius (meters)
    mass: float = 70.0  # Mass (kg)
    desired_speed: float = 1.34  # Desired speed (m/s)
    max_speed: float = 1.5  # Maximum speed
    state: PedestrianState = PedestrianState.NORMAL
    panic_level: float = 0.0  # Panic level 0-1
    path: List[np.ndarray] = field(default_factory=list)  # Path history
    
    def __post_init__(self):
        """Ensure arrays are float64"""
        self.position = self.position.astype(np.float64)
        self.velocity = self.velocity.astype(np.float64)
        self.goal = self.goal.astype(np.float64)
    
    def update_goal(self, new_goal: np.ndarray):
        """Update target position"""
        self.goal = new_goal
    
    def set_panic(self, level: float):
        """Set panic level"""
        self.panic_level = np.clip(level, 0, 1)
        if self.panic_level > 0.5:
            self.state = PedestrianState.PANIC
            self.desired_speed = 2.0  # Speed up when panicking
        else:
            self.state = PedestrianState.NORMAL
            self.desired_speed = 1.34

@dataclass
class Obstacle:
    """Obstacle"""
    vertices: np.ndarray  # Polygon vertices
    is_wall: bool = True

@dataclass
class Exit:
    """Exit/Entrance"""
    position: np.ndarray  # Center position
    width: float  # Width
    is_open: bool = True
    capacity: float = 1.0  # Flow capacity

@dataclass
class Event:
    """Emergency Event"""
    event_type: EventType
    position: np.ndarray  # Event position
    radius: float  # Effect radius
    start_time: float
    intensity: float = 1.0  # Intensity

class SocialForceModel:
    """Social Force Model"""
    
    def __init__(self, dt: float = 0.1):
        self.dt = dt  # Time step
        
        # Social force model parameters
        self.A = 2000  # Repulsion force strength between pedestrians
        self.B = 0.08  # Repulsion force range
        self.k = 1.2e5  # Body contact force coefficient
        self.kappa = 2.4e5  # Friction force coefficient
        
        # Wall repulsion parameters
        self.A_wall = 2000
        self.B_wall = 0.08
        
        # Desired speed adjustment parameters
        self.tau = 0.5  # Relaxation time
        
    def desired_force(self, ped: Pedestrian) -> np.ndarray:
        """Calculate desired velocity force"""
        direction = ped.goal - ped.position
        distance = np.linalg.norm(direction)
        
        if distance < 0.1:
            return np.zeros(2, dtype=np.float64)
        
        direction = direction / distance
        desired_velocity = direction * ped.desired_speed
        
        # Add randomness when panicking
        if ped.state == PedestrianState.PANIC:
            noise = np.random.randn(2) * 0.3
            desired_velocity += noise
        
        return ped.mass * (desired_velocity - ped.velocity) / self.tau
    
    def pedestrian_repulsion(self, ped1: Pedestrian, ped2: Pedestrian) -> np.ndarray:
        """Calculate repulsion force between pedestrians"""
        diff = ped1.position - ped2.position
        distance = np.linalg.norm(diff)
        
        if distance < 0.01:
            return np.zeros(2, dtype=np.float64)
        
        direction = diff / distance
        r_sum = ped1.radius + ped2.radius
        
        # Social force (psychological repulsion)
        social_force = self.A * np.exp((r_sum - distance) / self.B) * direction
        
        # Body contact force
        if distance < r_sum:
            contact_force = self.k * (r_sum - distance) * direction
            
            # Tangential friction force
            relative_velocity = ped2.velocity - ped1.velocity
            tangent = np.array([-direction[1], direction[0]], dtype=np.float64)
            friction = self.kappa * (r_sum - distance) * np.dot(relative_velocity, tangent) * tangent
            
            return social_force + contact_force + friction
        
        return social_force
    
    def wall_repulsion(self, ped: Pedestrian, obstacle: Obstacle) -> np.ndarray:
        """Calculate wall repulsion force"""
        # Simplified: calculate distance to nearest point
        min_distance = float('inf')
        nearest_point = None
        
        vertices = obstacle.vertices
        for i in range(len(vertices)):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % len(vertices)]
            
            # Calculate shortest distance from point to line segment
            line_vec = p2 - p1
            point_vec = ped.position - p1
            line_len = np.linalg.norm(line_vec)
            
            if line_len < 0.01:
                continue
            
            line_unit = line_vec / line_len
            proj_length = np.dot(point_vec, line_unit)
            proj_length = np.clip(proj_length, 0, line_len)
            
            closest = p1 + proj_length * line_unit
            distance = np.linalg.norm(ped.position - closest)
            
            if distance < min_distance:
                min_distance = distance
                nearest_point = closest
        
        if nearest_point is None or min_distance > 5.0:
            return np.zeros(2, dtype=np.float64)
        
        direction = ped.position - nearest_point
        direction = direction / (np.linalg.norm(direction) + 1e-6)
        
        force = self.A_wall * np.exp((ped.radius - min_distance) / self.B_wall) * direction
        
        return force
    
    def compute_total_force(self, ped: Pedestrian, 
                           all_pedestrians: List[Pedestrian],
                           obstacles: List[Obstacle]) -> np.ndarray:
        """Calculate total force"""
        total_force = self.desired_force(ped)
        
        # Inter-pedestrian forces
        for other in all_pedestrians:
            if other.id != ped.id:
                total_force += self.pedestrian_repulsion(ped, other)
        
        # Wall forces
        for obstacle in obstacles:
            total_force += self.wall_repulsion(ped, obstacle)
        
        return total_force

class SimulationEnvironment:
    """Simulation Environment"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
        self.pedestrians: List[Pedestrian] = []
        self.obstacles: List[Obstacle] = []
        self.exits: List[Exit] = []
        self.events: List[Event] = []
        
        self.model = SocialForceModel()
        self.time = 0.0
        self.pedestrian_counter = 0
        
        # Record data for export
        self.history: List[Dict] = []
        
    def add_pedestrian(self, position: np.ndarray, goal: np.ndarray) -> Pedestrian:
        """Add pedestrian"""
        ped = Pedestrian(
            id=self.pedestrian_counter,
            position=position.astype(np.float64),
            velocity=np.zeros(2, dtype=np.float64),
            goal=goal.astype(np.float64)
        )
        self.pedestrians.append(ped)
        self.pedestrian_counter += 1
        return ped
    
    def add_obstacle(self, vertices: np.ndarray):
        """Add obstacle"""
        self.obstacles.append(Obstacle(vertices=vertices))
    
    def add_exit(self, position: np.ndarray, width: float):
        """Add exit/entrance"""
        self.exits.append(Exit(position=position, width=width))
    
    def trigger_event(self, event_type: EventType, position: np.ndarray, 
                     radius: float = 5.0, intensity: float = 1.0):
        """Trigger emergency event"""
        event = Event(
            event_type=event_type,
            position=position,
            radius=radius,
            start_time=self.time,
            intensity=intensity
        )
        self.events.append(event)
        
        # Handle based on event type
        if event_type == EventType.FIRE or event_type == EventType.SHOOTING:
            self._handle_panic_event(event)
        elif event_type == EventType.ENTRANCE_CLOSE:
            self._close_nearest_exit(position)
        elif event_type == EventType.ENTRANCE_OPEN:
            self._open_nearest_exit(position)
    
    def _handle_panic_event(self, event: Event):
        """Handle panic event"""
        for ped in self.pedestrians:
            distance = np.linalg.norm(ped.position - event.position)
            if distance < event.radius:
                panic_level = event.intensity * (1 - distance / event.radius)
                ped.set_panic(panic_level)
                
                # Find nearest exit to escape
                nearest_exit = self._find_nearest_exit(ped.position)
                if nearest_exit and nearest_exit.is_open:
                    ped.update_goal(nearest_exit.position)
    
    def _close_nearest_exit(self, position: np.ndarray):
        """Close nearest exit"""
        nearest = self._find_nearest_exit(position)
        if nearest:
            nearest.is_open = False
    
    def _open_nearest_exit(self, position: np.ndarray):
        """Open nearest exit"""
        nearest = self._find_nearest_exit(position)
        if nearest:
            nearest.is_open = True
    
    def _find_nearest_exit(self, position: np.ndarray) -> Optional[Exit]:
        """Find nearest exit"""
        if not self.exits:
            return None
        
        min_dist = float('inf')
        nearest = None
        for exit in self.exits:
            dist = np.linalg.norm(position - exit.position)
            if dist < min_dist:
                min_dist = dist
                nearest = exit
        return nearest
    
    def step(self):
        """Execute one simulation step"""
        for ped in self.pedestrians[:]:
            # Calculate total force
            force = self.model.compute_total_force(ped, self.pedestrians, self.obstacles)
            
            # Update velocity and position
            acceleration = force / ped.mass
            ped.velocity += acceleration * self.model.dt
            
            # Limit maximum speed
            speed = np.linalg.norm(ped.velocity)
            if speed > ped.max_speed:
                ped.velocity = ped.velocity / speed * ped.max_speed
            
            ped.position += ped.velocity * self.model.dt
            
            # Record path
            ped.path.append(ped.position.copy())
            
            # Check if reached goal
            if np.linalg.norm(ped.position - ped.goal) < 0.5:
                self.pedestrians.remove(ped)
        
        self.time += self.model.dt
        
        # Record current frame data
        self._record_frame()
    
    def _record_frame(self):
        """Record current frame data for export"""
        frame_data = {
            'time': self.time,
            'pedestrians': [
                {
                    'id': p.id,
                    'position': p.position.tolist(),
                    'velocity': p.velocity.tolist(),
                    'state': p.state.value,
                    'panic_level': p.panic_level
                }
                for p in self.pedestrians
            ]
        }
        self.history.append(frame_data)
    
    def export_for_unity(self, filename: str):
        """Export data to Unity-readable JSON format"""
        data = {
            'metadata': {
                'width': self.width,
                'height': self.height,
                'total_time': self.time,
                'dt': self.model.dt
            },
            'obstacles': [
                {
                    'vertices': obs.vertices.tolist()
                }
                for obs in self.obstacles
            ],
            'exits': [
                {
                    'position': exit.position.tolist(),
                    'width': exit.width
                }
                for exit in self.exits
            ],
            'frames': self.history
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Data exported to: {filename}")
    
    def get_statistics(self) -> Dict:
        """Get statistics"""
        return {
            'current_pedestrians': len(self.pedestrians),
            'total_time': self.time,
            'panic_count': sum(1 for p in self.pedestrians if p.state == PedestrianState.PANIC),
            'average_speed': np.mean([np.linalg.norm(p.velocity) for p in self.pedestrians]) if self.pedestrians else 0
        }
