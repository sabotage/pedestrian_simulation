# Pedestrian Movement Simulation System - Technical Documentation

## System Overview

This is a comprehensive pedestrian movement simulation system designed for complex scenarios with web-based editing, real-time visualization, emergency event handling, and Unity VR export capabilities.

## Architecture

### Core Components

1. **Simulation Engine** (`src/simulation/`)
   - **pedestrian.py**: Individual pedestrian agent with properties and behaviors
   - **social_force.py**: Helbing's Social Force Model for realistic crowd dynamics
   - **pathfinding.py**: A* algorithm for navigation around obstacles
   - **environment.py**: Map representation with walls, entrances, exits, hazards
   - **events.py**: Emergency event scheduling and management
   - **simulator.py**: Main controller integrating all components

2. **Web Interface** (`src/web/`)
   - **app.py**: Flask server with Socket.IO for real-time communication
   - **templates/index.html**: Interactive web interface
   - **static/app.js**: Client-side logic and canvas rendering
   - **static/style.css**: Modern responsive styling

3. **Export System** (`src/export/`)
   - **unity_exporter.py**: JSON export for Unity VR integration
   - Includes C# script template for Unity

## Technical Details

### Social Force Model

Based on Helbing & Molnár (1995), the model calculates forces:

1. **Driving Force**: Propels pedestrian toward goal
   ```
   F_driving = (v_desired - v_current) / τ * m
   ```

2. **Repulsion Force**: Between pedestrians
   ```
   F_rep = A * exp((r_i + r_j - d_ij) / B) * n_ij
   ```

3. **Wall Force**: Prevents walking through obstacles
   ```
   F_wall = A_wall * exp((r - d) / B_wall) * n
   ```

4. **Random Fluctuation**: Natural movement variation

### Pathfinding

- **Algorithm**: A* with 8-directional movement
- **Grid**: Dynamic obstacle grid with configurable cell size
- **Path Simplification**: Removes unnecessary waypoints
- **Dynamic Recalculation**: When exits blocked or hazards appear

### Emergency Events

Supported event types:
- **Fire**: Creates panic zone, pedestrians flee
- **Shooting**: Immediate high panic in radius
- **Entrance/Exit Blocking**: Dynamic access control
- **Custom Events**: Extensible event system

### Panic Behavior

Panic level (0.0 to 1.0) affects:
- Movement speed (increases up to 50%)
- Repulsion force strength
- Path selection (prefer safer routes)

## Data Flow

```
User Input (Web) → Flask Server → Simulator
                                      ↓
                              Social Force Model
                                      ↓
                              Update Positions
                                      ↓
                              Event Manager
                                      ↓
                     WebSocket → Real-time Update → Canvas
```

## Unity VR Integration

### Export Format

JSON structure:
```json
{
  "metadata": {
    "duration": 120.5,
    "total_pedestrians": 145,
    "frame_count": 1205
  },
  "environment": {
    "dimensions": {"width": 50, "height": 50},
    "walls": [{"start": {...}, "end": {...}, "height": 3.0}],
    "entrances": [...],
    "exits": [...]
  },
  "trajectories": [
    {
      "id": 0,
      "keyframes": [
        {
          "time": 0.0,
          "position": {"x": 5.0, "y": 0.9, "z": 25.0},
          "velocity": {"x": 1.2, "y": 0, "z": 0.1},
          "panic_level": 0.0
        }
      ]
    }
  ],
  "events": [...]
}
```

### Unity Implementation Steps

1. **Import JSON**: Load simulation data file
2. **Create Prefabs**: Pedestrian and wall prefabs
3. **Attach Script**: Use provided `PedestrianSimulationPlayer.cs`
4. **Configure**: Assign prefabs and file path
5. **Play**: Run scene to visualize 3D movement

### Coordinate System Conversion

- **2D Simulation**: X-Z plane (Y = 0)
- **Unity**: X-Z plane (Y = pedestrian height ~0.9m)
- Automatic conversion in exporter

## Performance Optimization

### Simulation
- Spatial partitioning for collision detection (future enhancement)
- Configurable time step (default 0.1s)
- Lazy pathfinding (recalculate only when needed)

### Web Interface
- Canvas rendering optimized for 60 FPS
- WebSocket for efficient real-time updates
- Server-side simulation (no client lag)

### Unity
- Keyframe interpolation for smooth movement
- LOD system recommended for large crowds
- Asynchronous JSON loading

## Parameters Reference

### Environment
- **Width/Height**: Size in meters (10-200m recommended)
- **Cell Size**: Pathfinding grid resolution (0.5m default)

### Pedestrian
- **Max Speed**: 0.8-2.0 m/s (1.3 default)
- **Radius**: Personal space 0.2-0.5m (0.3 default)
- **Mass**: 60-100 kg (80 default)

### Social Force
- **Relaxation Time**: 0.3-0.7s (0.5 default)
- **A_ped**: Pedestrian repulsion strength (2000 N)
- **B_ped**: Repulsion range (0.08m)
- **A_wall**: Wall repulsion strength (2000 N)
- **B_wall**: Wall repulsion range (0.08m)

### Entrance
- **Flow Rate**: Pedestrians/second (0.1-10, 2.0 default)
- **Radius**: Spawn area size (0.5-5m)

### Events
- **Fire Radius**: Panic zone size (3-15m)
- **Shooting Radius**: Immediate panic zone (5-20m)

## Extension Points

### Custom Pedestrian Behaviors

Extend `Pedestrian` class:
```python
class CustomPedestrian(Pedestrian):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_property = value
    
    def custom_behavior(self):
        # Your logic here
        pass
```

### Custom Events

Extend `Event` class:
```python
class CustomEvent(Event):
    def __init__(self, trigger_time, custom_params):
        super().__init__(
            EventType.CUSTOM, 
            trigger_time, 
            custom_params
        )
```

### Alternative Force Models

Replace `SocialForceModel`:
```python
class AlternativeForceModel:
    def calculate_total_force(self, ped, others, walls):
        # Your physics model
        return force_vector
```

## Troubleshooting

### Common Issues

1. **No pedestrians appearing**
   - Check entrance flow rate > 0
   - Verify entrance not inside wall
   - Ensure exits exist

2. **Pedestrians stuck**
   - Check for closed paths
   - Reduce wall density
   - Increase pathfinding grid resolution

3. **Slow performance**
   - Reduce pedestrian count (lower flow rate)
   - Increase time step (0.2-0.3s)
   - Simplify environment

4. **Unity export issues**
   - Ensure recording was enabled
   - Check JSON file validity
   - Verify coordinate system conversion

## Future Enhancements

Potential additions:
- [ ] 3D multi-floor environments
- [ ] Group behavior (families, friends)
- [ ] Age/mobility variations
- [ ] Machine learning for path prediction
- [ ] Real-time density heatmaps
- [ ] Video export
- [ ] Scenario templates library
- [ ] Multi-agent cooperation
- [ ] Accessibility features (wheelchairs, etc.)

## References

1. Helbing, D., & Molnár, P. (1995). Social force model for pedestrian dynamics.
2. Helbing, D., Farkas, I., & Vicsek, T. (2000). Simulating dynamical features of escape panic.
3. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). A Formal Basis for the Heuristic Determination of Minimum Cost Paths (A* algorithm).

## License

MIT License - See LICENSE file for details

## Support

For issues, questions, or contributions, please refer to the project repository.
