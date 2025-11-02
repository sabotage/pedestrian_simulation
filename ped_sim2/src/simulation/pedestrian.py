"""
Pedestrian agent class representing individual pedestrians in the simulation.
"""
import numpy as np
from typing import Tuple, Optional


class Pedestrian:
    """Represents a single pedestrian agent in the simulation."""
    
    def __init__(self, ped_id: int, position: np.ndarray, goal: np.ndarray, 
                 max_speed: float = 1.3, radius: float = 0.3):
        """
        Initialize a pedestrian agent.
        
        Args:
            ped_id: Unique identifier for the pedestrian
            position: Initial position [x, y]
            goal: Target destination [x, y]
            max_speed: Maximum walking speed (m/s)
            radius: Personal space radius (m)
        """
        self.id = ped_id
        self.position = np.array(position, dtype=float)
        self.velocity = np.zeros(2)
        self.goal = np.array(goal, dtype=float)
        self.max_speed = max_speed
        self.radius = radius
        self.mass = 80.0  # kg
        self.desired_speed = max_speed
        self.active = True
        self.reached_goal = False
        self.panic_level = 0.0  # 0.0 to 1.0, affects behavior during emergencies
        self.path = [goal]  # Waypoints to follow
        self.current_waypoint_idx = 0
        
    def get_desired_direction(self) -> np.ndarray:
        """Calculate the desired direction towards current waypoint."""
        if self.current_waypoint_idx >= len(self.path):
            target = self.goal
        else:
            target = self.path[self.current_waypoint_idx]
            
        direction = target - self.position
        distance = np.linalg.norm(direction)
        
        # Check if reached current waypoint
        if distance < 0.5 and self.current_waypoint_idx < len(self.path) - 1:
            self.current_waypoint_idx += 1
            target = self.path[self.current_waypoint_idx]
            direction = target - self.position
            distance = np.linalg.norm(direction)
        
        if distance < 0.1:
            self.reached_goal = True
            return np.zeros(2)
            
        return direction / distance
    
    def update_position(self, force: np.ndarray, dt: float):
        """
        Update pedestrian position based on applied force.
        
        Args:
            force: Total force vector acting on pedestrian
            dt: Time step (seconds)
        """
        if not self.active or self.reached_goal:
            return
            
        # Update velocity using force
        acceleration = force / self.mass
        self.velocity += acceleration * dt
        
        # Limit velocity to max speed (accounting for panic)
        speed = np.linalg.norm(self.velocity)
        effective_max_speed = self.max_speed * (1.0 + 0.5 * self.panic_level)
        
        if speed > effective_max_speed:
            self.velocity = (self.velocity / speed) * effective_max_speed
        
        # Update position
        self.position += self.velocity * dt
    
    def set_panic_level(self, level: float):
        """Set panic level (0.0 = calm, 1.0 = maximum panic)."""
        self.panic_level = np.clip(level, 0.0, 1.0)
    
    def update_path(self, new_path: list):
        """Update the path to follow."""
        self.path = new_path
        self.current_waypoint_idx = 0
        self.reached_goal = False
    
    def deactivate(self):
        """Deactivate pedestrian (e.g., reached exit)."""
        self.active = False
        self.velocity = np.zeros(2)
    
    def to_dict(self) -> dict:
        """Convert pedestrian state to dictionary for serialization."""
        return {
            'id': self.id,
            'position': self.position.tolist(),
            'velocity': self.velocity.tolist(),
            'goal': self.goal.tolist(),
            'active': self.active,
            'reached_goal': self.reached_goal,
            'panic_level': self.panic_level,
            'radius': self.radius
        }
