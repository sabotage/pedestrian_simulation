"""
A* pathfinding algorithm for pedestrian navigation.
"""
import numpy as np
from typing import List, Tuple, Optional
import heapq


class PathFinder:
    """A* pathfinding for pedestrian navigation around obstacles."""
    
    def __init__(self, grid_size: Tuple[int, int], cell_size: float = 0.5):
        """
        Initialize pathfinding grid.
        
        Args:
            grid_size: Size of environment (width, height) in meters
            cell_size: Size of each grid cell in meters
        """
        self.grid_width = int(grid_size[0] / cell_size)
        self.grid_height = int(grid_size[1] / cell_size)
        self.cell_size = cell_size
        self.grid = np.zeros((self.grid_height, self.grid_width), dtype=bool)
        self.walkable_grid = None  # Grid marking walkable areas (roads)
        self.roads_only_mode = False  # Whether to restrict movement to roads only
        self.hazard_zones = []  # Dynamic hazard zones to avoid
        self.hazard_buffer = 1.5  # Extra buffer around hazards (in meters)
        
    def set_obstacle(self, x: float, y: float, width: float = None, height: float = None):
        """
        Mark a region as obstacle.
        
        Args:
            x, y: Position in world coordinates
            width, height: Size of obstacle (optional, defaults to cell_size)
        """
        if width is None:
            width = self.cell_size
        if height is None:
            height = self.cell_size
            
        # Convert to grid coordinates
        grid_x = int(x / self.cell_size)
        grid_y = int(y / self.cell_size)
        grid_w = max(1, int(width / self.cell_size))
        grid_h = max(1, int(height / self.cell_size))
        
        # Mark cells as occupied
        for dy in range(grid_h):
            for dx in range(grid_w):
                gx = grid_x + dx
                gy = grid_y + dy
                if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
                    self.grid[gy, gx] = True
    
    def set_roads_only_mode(self, enabled: bool = True):
        """
        Enable or disable roads-only movement mode.
        
        Args:
            enabled: If True, pedestrians can only move on roads
        """
        self.roads_only_mode = enabled
        if enabled and self.walkable_grid is None:
            # Initialize walkable grid as all unwalkable
            self.walkable_grid = np.zeros((self.grid_height, self.grid_width), dtype=bool)
    
    def update_hazard_zones(self, hazards: List[dict]):
        """
        Update dynamic hazard zones that should be avoided in pathfinding.
        
        Args:
            hazards: List of hazard dictionaries with 'position' and 'radius'
        """
        self.hazard_zones = hazards
    
    def _is_in_hazard_zone(self, world_x: float, world_y: float) -> bool:
        """
        Check if a world coordinate is within any hazard zone (with buffer).
        
        Args:
            world_x, world_y: World coordinates to check
            
        Returns:
            True if point is in a hazard zone
        """
        for hazard in self.hazard_zones:
            hazard_pos = hazard['position']
            hazard_radius = hazard['radius'] + self.hazard_buffer
            
            distance = np.sqrt((world_x - hazard_pos[0])**2 + (world_y - hazard_pos[1])**2)
            if distance < hazard_radius:
                return True
        
        return False
    
    def add_road_segment(self, points: List[Tuple[float, float]], width: float = 2.0):
        """
        Add a road segment as a walkable area.
        
        Args:
            points: List of points defining the road path
            width: Width of the road in meters
        """
        if self.walkable_grid is None:
            self.walkable_grid = np.zeros((self.grid_height, self.grid_width), dtype=bool)
        
        # Draw road between consecutive points
        for i in range(len(points) - 1):
            start = np.array(points[i])
            end = np.array(points[i + 1])
            self._mark_road_segment(start, end, width)
    
    def _mark_road_segment(self, start: np.ndarray, end: np.ndarray, width: float):
        """Mark a road segment as walkable in the grid."""
        # Calculate number of steps along the road
        length = np.linalg.norm(end - start)
        steps = int(length / (self.cell_size * 0.25))
        steps = max(steps, 1)
        
        # Width in grid cells
        half_width_cells = int((width / 2) / self.cell_size)
        
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            point = start + t * (end - start)
            
            # Convert to grid coordinates
            grid_x = int(point[0] / self.cell_size)
            grid_y = int(point[1] / self.cell_size)
            
            # Mark cells around this point as walkable
            for dy in range(-half_width_cells, half_width_cells + 1):
                for dx in range(-half_width_cells, half_width_cells + 1):
                    gx = grid_x + dx
                    gy = grid_y + dy
                    if 0 <= gx < self.grid_width and 0 <= gy < self.grid_height:
                        # Check if within circular road width
                        dist = np.sqrt(dx*dx + dy*dy) * self.cell_size
                        if dist <= width / 2:
                            self.walkable_grid[gy, gx] = True
    
    def add_wall_segment(self, start: np.ndarray, end: np.ndarray, thickness: float = 0.2):
        """
        Add a wall segment as obstacle.
        
        Args:
            start: Wall start point [x, y]
            end: Wall end point [x, y]
            thickness: Wall thickness
        """
        # Bresenham-like algorithm to mark wall cells
        steps = int(np.linalg.norm(end - start) / (self.cell_size * 0.5))
        steps = max(steps, 1)
        
        for i in range(steps + 1):
            t = i / steps if steps > 0 else 0
            point = start + t * (end - start)
            self.set_obstacle(point[0], point[1], thickness, thickness)
    
    def find_path(self, start: np.ndarray, goal: np.ndarray) -> List[np.ndarray]:
        """
        Find path from start to goal using A* algorithm.
        
        Args:
            start: Start position [x, y]
            goal: Goal position [x, y]
            
        Returns:
            List of waypoints from start to goal
        """
        # Convert to grid coordinates
        start_grid = (int(start[0] / self.cell_size), int(start[1] / self.cell_size))
        goal_grid = (int(goal[0] / self.cell_size), int(goal[1] / self.cell_size))
        
        # Check if start or goal is in obstacle
        if not self._is_valid_cell(start_grid):
            start_grid = self._find_nearest_free_cell(start_grid)
        if not self._is_valid_cell(goal_grid):
            goal_grid = self._find_nearest_free_cell(goal_grid)
            
        if start_grid is None or goal_grid is None:
            return [goal]  # Return direct goal if no path found
        
        # A* algorithm
        open_set = []
        heapq.heappush(open_set, (0, start_grid))
        came_from = {}
        g_score = {start_grid: 0}
        f_score = {start_grid: self._heuristic(start_grid, goal_grid)}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            
            if current == goal_grid:
                # Reconstruct path
                path = self._reconstruct_path(came_from, current)
                # Simplify path and convert to world coordinates
                return self._simplify_path(path)
            
            for neighbor in self._get_neighbors(current):
                tentative_g = g_score[current] + self._distance(current, neighbor)
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._heuristic(neighbor, goal_grid)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # No path found, return direct goal
        return [goal]
    
    def _is_valid_cell(self, cell: Tuple[int, int]) -> bool:
        """Check if cell is within bounds and not an obstacle."""
        x, y = cell
        if x < 0 or x >= self.grid_width or y < 0 or y >= self.grid_height:
            return False
        
        # Check if cell is an obstacle
        if self.grid[y, x]:
            return False
        
        # Check if cell is in a hazard zone
        world_x = x * self.cell_size + self.cell_size / 2
        world_y = y * self.cell_size + self.cell_size / 2
        if self._is_in_hazard_zone(world_x, world_y):
            return False
        
        # If roads-only mode is enabled, check if cell is on a road
        if self.roads_only_mode and self.walkable_grid is not None:
            return self.walkable_grid[y, x]
        
        return True
    
    def _find_nearest_free_cell(self, cell: Tuple[int, int]) -> Optional[Tuple[int, int]]:
        """Find nearest free cell to given cell."""
        for radius in range(1, 20):
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if abs(dx) == radius or abs(dy) == radius:
                        neighbor = (cell[0] + dx, cell[1] + dy)
                        if self._is_valid_cell(neighbor):
                            return neighbor
        return None
    
    def _get_neighbors(self, cell: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid neighboring cells."""
        x, y = cell
        neighbors = []
        
        # 8-directional movement
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor = (x + dx, y + dy)
                if self._is_valid_cell(neighbor):
                    neighbors.append(neighbor)
        
        return neighbors
    
    def _heuristic(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Euclidean distance heuristic."""
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def _distance(self, a: Tuple[int, int], b: Tuple[int, int]) -> float:
        """Distance between adjacent cells."""
        return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
    
    def _reconstruct_path(self, came_from: dict, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Reconstruct path from A* came_from dictionary."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def _simplify_path(self, grid_path: List[Tuple[int, int]]) -> List[np.ndarray]:
        """
        Simplify path by removing unnecessary waypoints and convert to world coords.
        """
        if len(grid_path) <= 2:
            return [np.array([p[0] * self.cell_size, p[1] * self.cell_size]) 
                   for p in grid_path]
        
        simplified = [grid_path[0]]
        
        for i in range(1, len(grid_path) - 1):
            # Check if point is necessary (changes direction)
            prev = np.array(grid_path[i - 1])
            curr = np.array(grid_path[i])
            next_p = np.array(grid_path[i + 1])
            
            dir1 = curr - prev
            dir2 = next_p - curr
            
            # Normalize
            if np.linalg.norm(dir1) > 0:
                dir1 = dir1 / np.linalg.norm(dir1)
            if np.linalg.norm(dir2) > 0:
                dir2 = dir2 / np.linalg.norm(dir2)
            
            # Keep point if direction changes significantly
            if np.dot(dir1, dir2) < 0.9:  # ~25 degree threshold
                simplified.append(grid_path[i])
        
        simplified.append(grid_path[-1])
        
        # Convert to world coordinates
        world_path = [np.array([p[0] * self.cell_size + self.cell_size/2, 
                               p[1] * self.cell_size + self.cell_size/2]) 
                     for p in simplified]
        
        return world_path
