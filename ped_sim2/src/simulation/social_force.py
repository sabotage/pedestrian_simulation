"""
Social Force Model for pedestrian movement simulation.
Based on Helbing & Molnár (1995) and Helbing et al. (2000).
"""
import numpy as np
from typing import List
from .pedestrian import Pedestrian


class SocialForceModel:
    """
    Implements the social force model for realistic pedestrian dynamics.
    """
    
    def __init__(self):
        """Initialize social force model parameters."""
        # Driving force parameters
        self.relaxation_time = 0.5  # Time to reach desired velocity
        
        # Pedestrian-pedestrian repulsion
        self.A_ped = 2000.0  # Interaction strength (N)
        self.B_ped = 0.08    # Interaction range (m)
        
        # Pedestrian-wall repulsion
        self.A_wall = 2000.0  # Wall interaction strength (N)
        self.B_wall = 0.08    # Wall interaction range (m)
        
        # Hazard repulsion (fire, shooting, etc.)
        self.A_hazard = 5000.0  # Hazard interaction strength (N) - stronger than walls
        self.B_hazard = 2.0     # Hazard interaction range (m) - wider range
        
        # Fluctuation parameters
        self.fluctuation_strength = 0.3
        
    def calculate_driving_force(self, pedestrian: Pedestrian) -> np.ndarray:
        """
        Calculate the driving force towards the goal.
        
        Args:
            pedestrian: Pedestrian agent
            
        Returns:
            Driving force vector
        """
        desired_direction = pedestrian.get_desired_direction()
        desired_velocity = desired_direction * pedestrian.desired_speed
        
        # Adjust for panic (higher panic = faster desired speed)
        desired_velocity *= (1.0 + 0.3 * pedestrian.panic_level)
        
        # Force to reach desired velocity
        force = (desired_velocity - pedestrian.velocity) / self.relaxation_time
        force *= pedestrian.mass
        
        return force
    
    def calculate_pedestrian_repulsion(self, ped_i: Pedestrian, 
                                      ped_j: Pedestrian) -> np.ndarray:
        """
        Calculate repulsive force between two pedestrians.
        
        Args:
            ped_i: First pedestrian
            ped_j: Second pedestrian
            
        Returns:
            Repulsive force vector on ped_i
        """
        if not ped_i.active or not ped_j.active:
            return np.zeros(2)
            
        diff = ped_i.position - ped_j.position
        distance = np.linalg.norm(diff)
        
        # Avoid division by zero
        if distance < 0.01:
            distance = 0.01
            
        # Normalized direction
        direction = diff / distance
        
        # Social force magnitude (exponential decay)
        combined_radius = ped_i.radius + ped_j.radius
        force_magnitude = self.A_ped * np.exp((combined_radius - distance) / self.B_ped)
        
        # Additional panic effect - higher repulsion when panicked
        panic_factor = 1.0 + ped_i.panic_level
        force_magnitude *= panic_factor
        
        return force_magnitude * direction
    
    def calculate_wall_repulsion(self, pedestrian: Pedestrian, 
                                 walls: List[np.ndarray]) -> np.ndarray:
        """
        Calculate repulsive force from walls/obstacles.
        
        Args:
            pedestrian: Pedestrian agent
            walls: List of wall segments [start, end]
            
        Returns:
            Total wall repulsion force
        """
        total_force = np.zeros(2)
        
        for wall in walls:
            # Find closest point on wall segment
            closest_point, distance = self._closest_point_on_segment(
                pedestrian.position, wall[0], wall[1]
            )
            
            # Direction from wall to pedestrian
            diff = pedestrian.position - closest_point
            
            # Avoid division by zero
            if distance < 0.01:
                distance = 0.01
                diff = np.array([0.1, 0.1])  # Small perturbation
                
            direction = diff / distance
            
            # Wall force magnitude
            force_magnitude = self.A_wall * np.exp(
                (pedestrian.radius - distance) / self.B_wall
            )
            
            total_force += force_magnitude * direction
            
        return total_force
    
    def _closest_point_on_segment(self, point: np.ndarray, 
                                  seg_start: np.ndarray, 
                                  seg_end: np.ndarray) -> tuple:
        """
        Find the closest point on a line segment to a given point.
        
        Args:
            point: Point to measure from
            seg_start: Segment start point
            seg_end: Segment end point
            
        Returns:
            Tuple of (closest_point, distance)
        """
        segment = seg_end - seg_start
        segment_length_sq = np.dot(segment, segment)
        
        if segment_length_sq < 1e-6:
            # Degenerate segment
            closest = seg_start
        else:
            # Project point onto line
            t = np.dot(point - seg_start, segment) / segment_length_sq
            t = np.clip(t, 0, 1)  # Clamp to segment
            closest = seg_start + t * segment
            
        distance = np.linalg.norm(point - closest)
        return closest, distance
    
    def calculate_random_fluctuation(self) -> np.ndarray:
        """
        Calculate random fluctuation force for natural movement variation.
        
        Returns:
            Random force vector
        """
        angle = np.random.uniform(0, 2 * np.pi)
        magnitude = np.random.normal(0, self.fluctuation_strength)
        return magnitude * np.array([np.cos(angle), np.sin(angle)])
    
    def calculate_hazard_repulsion(self, pedestrian: Pedestrian,
                                   hazard_zones: List[dict]) -> np.ndarray:
        """
        Calculate repulsive force from hazard zones (fire, shooting, etc.).
        
        Args:
            pedestrian: Pedestrian agent
            hazard_zones: List of hazard zone dictionaries with 'position', 'radius', 'type'
            
        Returns:
            Total hazard repulsion force
        """
        total_force = np.zeros(2)
        
        for hazard in hazard_zones:
            # Direction from hazard to pedestrian
            diff = pedestrian.position - hazard['position']
            distance = np.linalg.norm(diff)
            
            # Avoid division by zero
            if distance < 0.01:
                distance = 0.01
                diff = np.array([0.1, 0.1])  # Small perturbation
            
            direction = diff / distance
            
            # Hazard force magnitude - exponential decay from hazard edge
            hazard_radius = hazard['radius']
            penetration = hazard_radius - distance
            
            # Strong repulsion when inside or near hazard zone
            if distance < hazard_radius * 1.5:
                force_magnitude = self.A_hazard * np.exp(penetration / self.B_hazard)
                
                # Fire hazards have stronger repulsion
                if hazard.get('type') == 'fire':
                    force_magnitude *= 1.5
                
                # Panic increases repulsion sensitivity
                panic_factor = 1.0 + 2.0 * pedestrian.panic_level
                force_magnitude *= panic_factor
                
                total_force += force_magnitude * direction
        
        return total_force
    
    def calculate_total_force(self, pedestrian: Pedestrian, 
                             other_pedestrians: List[Pedestrian],
                             walls: List[np.ndarray],
                             hazard_zones: List[dict] = None) -> np.ndarray:
        """
        Calculate total force acting on a pedestrian.
        
        Args:
            pedestrian: Target pedestrian
            other_pedestrians: List of other pedestrians
            walls: List of wall segments
            hazard_zones: List of hazard zone dictionaries (optional)
            
        Returns:
            Total force vector
        """
        # Driving force towards goal
        force = self.calculate_driving_force(pedestrian)
        
        # Repulsion from other pedestrians
        for other in other_pedestrians:
            if other.id != pedestrian.id:
                force += self.calculate_pedestrian_repulsion(pedestrian, other)
        
        # Repulsion from walls
        force += self.calculate_wall_repulsion(pedestrian, walls)
        
        # Repulsion from hazards
        if hazard_zones:
            force += self.calculate_hazard_repulsion(pedestrian, hazard_zones)
        
        # Random fluctuation
        force += self.calculate_random_fluctuation()
        
        return force
