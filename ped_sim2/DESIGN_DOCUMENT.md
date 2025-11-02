# Pedestrian Simulation System - Design Document

**Version:** 2.0  
**Date:** November 1, 2025  
**Status:** Production Ready

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [System Architecture](#2-system-architecture)
3. [Core Components](#3-core-components)
4. [Simulation Algorithms](#4-simulation-algorithms)
5. [User Interface Design](#5-user-interface-design)
6. [Data Models](#6-data-models)
7. [Traffic Control System](#7-traffic-control-system)
8. [Rendering System](#8-rendering-system)
9. [Emergency Event System](#9-emergency-event-system)
10. [Export & Integration](#10-export--integration)
11. [Performance Considerations](#11-performance-considerations)
12. [Future Enhancements](#12-future-enhancements)

---

## 1. Executive Summary

### 1.1 Purpose

The Pedestrian Simulation System is a comprehensive web-based application designed to simulate realistic pedestrian movement in urban environments. It combines physics-based behavioral modeling with intuitive visualization to support:

- **Urban Planning**: Analyzing pedestrian flow in public spaces
- **Emergency Preparedness**: Testing evacuation scenarios
- **Research & Education**: Demonstrating crowd dynamics
- **VR/Game Development**: Exporting realistic pedestrian behavior to Unity

### 1.2 Key Features

- ✅ **Physics-Based Simulation**: Social Force Model (Helbing & Molnár, 1995)
- ✅ **Intelligent Pathfinding**: A* algorithm with dynamic obstacle avoidance
- ✅ **Traffic Light System**: Realistic intersection behavior with compliance
- ✅ **Emergency Events**: Fire, shooting, entrance/exit blocking
- ✅ **Isometric 3D Visualization**: Modern rendering with buildings, vehicles, decorations
- ✅ **Bilingual UI**: Full Chinese + English support
- ✅ **Preset Scenarios**: 5 complex urban environments ready to use
- ✅ **Unity Export**: Complete simulation data for VR integration

### 1.3 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend** | Python 3.9+ | Simulation engine |
| **Web Framework** | Flask 3.0 + Flask-SocketIO | Real-time communication |
| **Frontend** | HTML5 + Canvas API | Interactive visualization |
| **Data Format** | JSON | Configuration & export |
| **Algorithms** | NumPy | High-performance computation |

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser (Client)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐ │
│  │  HTML/CSS   │  │   Canvas     │  │  JavaScript    │ │
│  │  UI Layer   │  │  Renderer    │  │  Controller    │ │
│  └──────┬──────┘  └──────┬───────┘  └────────┬───────┘ │
│         │                │                    │         │
└─────────┼────────────────┼────────────────────┼─────────┘
          │                │                    │
          └────────────────┴────────────────────┘
                           │
                    WebSocket (Socket.IO)
                           │
┌─────────────────────────┴─────────────────────────────┐
│               Flask Web Server (Backend)               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Routes     │  │  WebSocket   │  │   Export    │ │
│  │   Handler    │  │   Events     │  │   System    │ │
│  └──────┬───────┘  └──────┬───────┘  └──────┬──────┘ │
│         └──────────────────┴──────────────────┘        │
└─────────────────────────┬──────────────────────────────┘
                          │
┌─────────────────────────┴──────────────────────────────┐
│              Simulation Engine (Core)                   │
│  ┌────────────┐  ┌─────────────┐  ┌────────────────┐  │
│  │ Simulator  │  │ Environment │  │    Events      │  │
│  │ Controller │  │   Manager   │  │    Manager     │  │
│  └─────┬──────┘  └──────┬──────┘  └────────┬───────┘  │
│        │                │                   │          │
│  ┌─────┴──────┐  ┌──────┴───────┐  ┌───────┴────────┐ │
│  │Pedestrians │  │Social Force  │  │  Pathfinding   │ │
│  │  (Agents)  │  │    Model     │  │   (A* Search)  │ │
│  └────────────┘  └──────────────┘  └────────────────┘ │
└────────────────────────────────────────────────────────┘
```

### 2.2 Component Interaction Flow

```
User Interaction → Web UI → Flask Route/WebSocket → Simulator
                                                         ↓
                    ┌────────────────────────────────────┘
                    ↓
    [For each simulation step]
    1. Spawn new pedestrians at entrances
    2. Check traffic light states
    3. Update pedestrian paths (A* if needed)
    4. Calculate social forces
    5. Apply forces to update positions
    6. Check for exits/goals reached
    7. Trigger scheduled events
    8. Emit state update to client
                    ↓
    Client receives update → Render new state → Display
```

### 2.3 Directory Structure

```
ped_sim2/
├── src/
│   ├── simulation/          # Core simulation engine
│   │   ├── simulator.py     # Main controller (570 lines)
│   │   ├── environment.py   # World representation (458 lines)
│   │   ├── pedestrian.py    # Agent behavior (112 lines)
│   │   ├── social_force.py  # Physics model (252 lines)
│   │   ├── pathfinding.py   # A* algorithm (316 lines)
│   │   └── events.py        # Emergency events (280 lines)
│   ├── web/                 # Web interface
│   │   ├── app.py           # Flask server (365 lines)
│   │   ├── static/
│   │   │   ├── app.js       # Frontend logic (2529 lines)
│   │   │   └── style.css    # Modern UI styling
│   │   └── templates/
│   │       └── index.html   # Main interface
│   └── export/              # Unity integration
│       └── unity_exporter.py
├── scenarios/               # Preset configurations
├── examples/                # Usage examples
└── tests/                   # Test suite
```

---

## 3. Core Components

### 3.1 Simulator (Main Controller)

**File:** `src/simulation/simulator.py`  
**Responsibility:** Orchestrates all simulation components

**Key Methods:**

```python
class Simulator:
    def __init__(self, environment, dt=0.1):
        """Initialize with environment and timestep"""
        
    def step(self):
        """Execute one simulation timestep"""
        # 1. Spawn pedestrians
        # 2. Update traffic lights
        # 3. Calculate forces
        # 4. Update positions
        # 5. Check goals
        # 6. Process events
        
    def select_exit_for_pedestrian(self, position):
        """Choose exit based on strategy (random/nearest/weighted)"""
        
    def _update_traffic_lights(self):
        """30-second cycle: 15s green, 15s red, alternating NS/EW"""
```

**Simulation Loop:**

```
┌─→ Spawn pedestrians at entrances (if flow rate permits)
│   ↓
│   Update traffic light states (30-second cycle)
│   ↓
│   For each pedestrian:
│   ├─ Check traffic light compliance
│   ├─ Calculate social forces (driving, repulsion, walls, hazards)
│   ├─ Update velocity and position
│   ├─ Check if reached exit
│   └─ Update panic level based on hazards
│   ↓
│   Process scheduled events (fires, blockages)
│   ↓
│   Emit state to client via WebSocket
│   ↓
└─── Sleep for dt/simulation_speed
```

### 3.2 Environment

**File:** `src/simulation/environment.py`  
**Responsibility:** Manages world geometry and zones

**Components:**

- **Walls**: Line segments blocking movement
- **Entrances**: Spawn zones with flow rates
- **Exits**: Goal zones for pedestrians
- **Hazards**: Dynamic danger zones (fire, shooting)
- **Roads**: Navigable paths
- **Decorations**: Visual elements (trees, ponds, buildings)
- **Traffic Lights**: Intersection control points
- **Lanes**: Car lanes, pedestrian lanes, crossings

**Key Features:**

```python
class Environment:
    def add_wall(self, start, end):
        """Add obstacle line segment"""
        
    def add_entrance(self, position, radius, flow_rate):
        """Add spawn point"""
        
    def add_traffic_light(self, position, orientation):
        """Add intersection control"""
        
    def get_traffic_light_state(self, position, velocity):
        """Check if pedestrian should stop at red light"""
        # Returns: 'stop', 'go', or None
```

**Traffic Light Detection Algorithm:**

```python
# For each crossing with a traffic light:
# 1. Calculate perpendicular distance to crossing center
# 2. Check if pedestrian is ON crossing (within 2m)
#    → If yes, allow continuation (already committed)
# 3. Check if approaching (moving toward crossing)
# 4. Check if within lateral bounds (0 to crossing_length)
# 5. If approaching and within bounds:
#    → Check light state
#    → Return 'stop' if red, 'go' if green
```

### 3.3 Pedestrian (Agent)

**File:** `src/simulation/pedestrian.py`  
**Responsibility:** Individual pedestrian behavior

**State Variables:**

```python
class Pedestrian:
    id: int                  # Unique identifier
    position: np.ndarray     # Current [x, y] position
    velocity: np.ndarray     # Current [vx, vy] velocity
    goal: np.ndarray         # Target [x, y] position
    max_speed: float         # Maximum walking speed (m/s)
    radius: float            # Personal space radius (m)
    mass: float              # 80.0 kg (for force calculations)
    panic_level: float       # 0.0 (calm) to 1.0 (panic)
    path: List[np.ndarray]   # Waypoints to follow
    reached_goal: bool       # Completion flag
```

**Behavior:**

- **Goal-Seeking**: Calculates desired direction to current waypoint
- **Speed Adjustment**: `effective_speed = max_speed * (1 + 0.5 * panic_level)`
- **Pathfinding**: Updates path when obstacles change
- **Traffic Compliance**: Stops at red lights (unless already on crossing)

### 3.4 Social Force Model

**File:** `src/simulation/social_force.py`  
**Responsibility:** Realistic pedestrian movement physics

**Based on:** Helbing & Molnár (1995)

**Force Components:**

```python
Total Force = Driving Force 
            + Σ(Pedestrian Repulsion) 
            + Σ(Wall Repulsion)
            + Σ(Hazard Repulsion)
            + Random Fluctuation
```

**1. Driving Force** (toward goal):
```python
F_drive = m * (v_desired - v_current) / τ
# τ = relaxation time (0.5s)
# m = mass (80 kg)
```

**2. Pedestrian Repulsion** (personal space):
```python
F_repel = A * exp((r_ij - d_ij) / B) * n_ij
# A = 2000 N (strength)
# B = 0.08 m (range)
# r_ij = sum of radii
# d_ij = distance between pedestrians
# n_ij = unit vector from j to i
```

**3. Wall Repulsion** (obstacle avoidance):
```python
F_wall = A_wall * exp(-d_wall / B_wall) * n_wall
# A_wall = 2000 N
# B_wall = 0.08 m
# d_wall = distance to nearest wall point
```

**4. Hazard Repulsion** (emergency avoidance):
```python
F_hazard = A_hazard * exp(-d_hazard / B_hazard) * n_hazard
# A_hazard = 5000 N (stronger than walls)
# B_hazard = 2.0 m (wider range)
```

### 3.5 Pathfinding (A*)

**File:** `src/simulation/pathfinding.py`  
**Responsibility:** Intelligent navigation around obstacles

**Grid System:**

- **Cell Size**: 0.5m × 0.5m (configurable)
- **Heuristic**: Euclidean distance to goal
- **Movement**: 8-directional (cardinal + diagonal)
- **Cost**: 1.0 for cardinal, 1.414 (√2) for diagonal

**Dynamic Features:**

```python
class PathFinder:
    def find_path(self, start, goal):
        """A* search with obstacle avoidance"""
        
    def update_hazard_zones(self, hazards):
        """Dynamically add danger zones to avoid"""
        
    def set_roads_only_mode(self, enabled):
        """Restrict movement to road network"""
```

**Path Simplification:**

After A* search, removes unnecessary waypoints using line-of-sight checks to create smoother, more natural paths.

---

## 4. Simulation Algorithms

### 4.1 Timestep Integration

**Method:** Forward Euler Integration  
**Timestep:** 0.1 seconds (default)

```python
# For each pedestrian:
1. Calculate total force: F_total = sum(all forces)
2. Calculate acceleration: a = F_total / mass
3. Update velocity: v_new = v_old + a * dt
4. Limit speed: v_new = min(|v_new|, max_speed) * normalize(v_new)
5. Update position: pos_new = pos_old + v_new * dt
```

### 4.2 Spawning Algorithm

```python
# For each entrance:
spawn_timer += dt * flow_rate

if spawn_timer >= 1.0 and spawned < target_count:
    # Calculate random position within entrance radius
    angle = random(0, 2π)
    offset = random(0, radius) * [cos(angle), sin(angle)]
    spawn_position = entrance.position + offset
    
    # Select exit based on mode (random/nearest/weighted)
    exit_position = select_exit(spawn_position)
    
    # Create pedestrian with path
    path = find_path(spawn_position, exit_position)
    pedestrian = Pedestrian(id, spawn_position, exit_position)
    pedestrian.update_path(path)
    
    spawn_timer -= 1.0
```

### 4.3 Traffic Light Cycle

**Timing:** 30-second cycle  
**Pattern:** Alternating North-South / East-West

```python
cycle_time = simulation_time % 30

if crossing.orientation == 'ns':
    state = 'green' if cycle_time >= 15 else 'red'
elif crossing.orientation == 'ew':
    state = 'red' if cycle_time >= 15 else 'green'

# Timeline:
# 0-15s:  NS red,   EW green
# 15-30s: NS green, EW red
# [repeat]
```

### 4.4 Traffic Light Compliance

**Detection Zone:**
- **Lateral Buffer**: 5.0m perpendicular to crossing
- **Stop Distance**: 5.0m before crossing center
- **On-Crossing Exception**: Within 2.0m of crossing center

```python
# Pedestrian approaching crossing:
perp_dist = distance_perpendicular_to_crossing(position)
proj_on_crossing = projection_along_crossing_length(position)

# Check 1: Already on crossing?
if perp_dist < 2.0:
    return None  # Continue moving (already committed)

# Check 2: Within approach zone?
if perp_dist > 5.0:
    return None  # Too far away

# Check 3: Moving toward crossing?
if dot(velocity, crossing_direction) <= 0:
    return None  # Moving away

# Check 4: Within crossing bounds?
if not (0 <= proj_on_crossing <= crossing_length):
    return None  # Laterally outside crossing

# Check light state
if light_state == 'red':
    velocity = [0, 0]  # STOP
    return 'stop'
```

### 4.5 Goal Reaching & Removal

```python
# For each pedestrian:
distance_to_goal = |position - goal|

if distance_to_goal < 0.5:  # Within goal radius
    if goal_is_exit:
        pedestrian.deactivate()
        stats['exited'] += 1
        remove_from_simulation(pedestrian)
    else:
        pedestrian.reached_goal = True
```

---

## 5. User Interface Design

### 5.1 UI Architecture

**Framework:** Modern Dark Theme with Bilingual Support  
**Version:** 2.0 (Complete Redesign)

**Layout Structure:**

```
┌─────────────────────────────────────────────────────┐
│              Header (Title + Language)               │
├──────────────┬──────────────────────────────────────┤
│              │                                       │
│   Control    │                                       │
│   Panel      │        Canvas (Isometric View)        │
│   (Left)     │                                       │
│              │                                       │
│  - Scenarios │                                       │
│  - Settings  │                                       │
│  - Tools     │                                       │
│  - Events    │                                       │
│  - Stats     │                                       │
│              │                                       │
├──────────────┴───────────────────────────────────────┤
│              Status Bar (Connection, Info)           │
└─────────────────────────────────────────────────────┘
```

### 5.2 Control Panel Sections

**1. Preset Scenarios** 🎬
- Dropdown selector with bilingual labels
- One-click scenario loading
- 5 preset urban environments

**2. Environment Settings** ⚙️
- Width/Height inputs (meters)
- Create/Reset buttons
- Grid display toggle

**3. Drawing Tools** 🎨
- Wall tool (click-click for segment)
- Entrance tool (click to place)
- Exit tool (click to place)
- Clear tool (click to remove)
- Active tool highlighting

**4. Simulation Controls** ▶️
- Number of pedestrians slider
- Flow rate slider (ped/sec)
- Simulation speed multiplier
- Start/Stop/Reset buttons
- Recording toggle (Unity export)

**5. Emergency Events** 🚨
- Event type selector
- Trigger time input
- Position/index configuration
- Add event button
- Event list display

**6. Statistics Dashboard** 📊
- Spawned count (with icon)
- Active count (animated)
- Exited count (with icon)
- Average panic level (color-coded)
- Real-time updates

### 5.3 Visual Design System

**Color Palette:**

```css
/* Dark Theme */
--bg-dark: #1a1a2e
--bg-medium: #16213e
--bg-light: #0f3460
--accent-primary: #00adb5
--accent-secondary: #00ffc6
--text-light: #eaeaea
--text-dim: #aaaaaa
--danger: #ff3366
--warning: #ffaa00
--success: #00ff88
```

**Typography:**

```css
--font-main: 'Segoe UI', 'Microsoft YaHei', sans-serif
--font-mono: 'Consolas', 'Monaco', monospace
--size-h1: 28px
--size-h2: 20px
--size-body: 14px
--size-small: 12px
```

**Component Styling:**

- **Cards**: Rounded corners (8px), subtle shadows, hover effects
- **Buttons**: Gradient backgrounds, smooth transitions (0.3s)
- **Inputs**: Dark backgrounds, cyan borders on focus
- **Stats**: Icon + value layout, animated value changes

### 5.4 Canvas Rendering

**Coordinate System:**
- **World Space**: Meters (simulation coordinates)
- **Screen Space**: Pixels (canvas coordinates)
- **Isometric Transform**: `toIso(x, y) → {x', y'}`

**Isometric Projection:**

```javascript
function toIso(x, y) {
    return {
        x: (x - y) * cos(30°),
        y: (x + y) * sin(30°) - z
    };
}

// Actual implementation:
const isoX = (x - y) * Math.cos(Math.PI / 6) * scale;
const isoY = (x + y) * Math.sin(Math.PI / 6) * scale;
```

**Render Order** (back-to-front):

```
1. Ground (grass texture)
2. Roads (asphalt)
3. Decorations (trees, ponds - except buildings)
4. Walls (3D extruded)
5. Lanes (road markings)
6. Crossings (zebra stripes)
7. Entrances (green zones)
8. Exits (blue zones)
9. Vehicles (cars on roads)
10. Hazards (fire, incidents)
11. Pedestrians (with panic colors)
12. Buildings (isometric 3D)
13. Traffic Lights (last layer, always visible)
```

### 5.5 Building Rendering

**Isometric Building Structure:**

```javascript
// Calculate 4 corners in isometric space:
corners[0] = toIso(x, y)           // Top corner
corners[1] = toIso(x + w, y)       // Right corner
corners[2] = toIso(x + w, y + h)   // Bottom corner
corners[3] = toIso(x, y + h)       // Left corner

// Draw faces:
1. Front face (corners[2] → corners[3]): Lighter shade
2. Right face (corners[1] → corners[2]): Darker shade
3. Top face: Not visible (looking down)

// Add windows:
Front face: 5 rows × 3 columns (parallelograms)
Right face: 5 rows × 2 columns (rectangles)
```

**Window Styling:**

- **Front Face Windows**: Isometric parallelograms following building face
- **Right Face Windows**: Simple rectangles positioned along diagonal
- **Frame**: Dark gray (#2c3e50)
- **Glass**: Gradient (light blue → dark blue)
- **Reflection**: White highlight overlay

---

## 6. Data Models

### 6.1 Environment Data Structure

```json
{
  "width": 100.0,
  "height": 100.0,
  "walls": [
    {"start": [x1, y1], "end": [x2, y2]}
  ],
  "entrances": [
    {
      "position": [x, y],
      "radius": 1.0,
      "flow_rate": 2.0,
      "active": true
    }
  ],
  "exits": [
    {
      "position": [x, y],
      "radius": 1.5,
      "active": true
    }
  ],
  "roads": [
    {
      "start": [x1, y1],
      "end": [x2, y2],
      "width": 6.0,
      "type": "two_way"
    }
  ],
  "decorations": [
    {
      "type": "building|tree|pond",
      "position": [x, y],
      "width": 10.0,
      "height": 15.0,
      "color": "#cccccc"
    }
  ],
  "trafficLights": [
    {
      "position": [x, y],
      "orientation": "ns|ew",
      "state": "red|green",
      "crossingIndex": 0
    }
  ],
  "crossingLanes": [
    {
      "start": [x1, y1],
      "end": [x2, y2],
      "width": 4.0,
      "orientation": "ns|ew"
    }
  ]
}
```

### 6.2 Pedestrian State

```json
{
  "id": 123,
  "position": [x, y],
  "velocity": [vx, vy],
  "goal": [gx, gy],
  "panic_level": 0.0,
  "active": true,
  "reached_goal": false,
  "path": [[x1, y1], [x2, y2], ...],
  "current_waypoint_idx": 0
}
```

### 6.3 Simulation State (WebSocket Update)

```json
{
  "time": 12.5,
  "pedestrians": [
    {
      "id": 1,
      "position": [25.3, 30.7],
      "velocity": [0.8, 1.2],
      "panic_level": 0.2
    }
  ],
  "stats": {
    "spawned": 45,
    "active": 32,
    "exited": 13,
    "total_panic": 4.5
  },
  "environment": {
    "hazard_zones": [
      {
        "position": [40, 40],
        "radius": 5.0,
        "type": "fire"
      }
    ],
    "trafficLights": [
      {
        "position": [50, 25],
        "state": "red",
        "orientation": "ns"
      }
    ]
  }
}
```

### 6.4 Unity Export Format

```json
{
  "metadata": {
    "export_time": "2025-11-01T12:00:00",
    "duration": 120.5,
    "total_pedestrians": 500,
    "timestep": 0.1
  },
  "environment": {
    "width": 100.0,
    "height": 100.0,
    "walls": [...],
    "entrances": [...],
    "exits": [...]
  },
  "trajectories": [
    {
      "pedestrian_id": 1,
      "spawn_time": 0.5,
      "exit_time": 45.2,
      "positions": [
        {"time": 0.5, "x": 10.0, "y": 5.0},
        {"time": 0.6, "x": 10.1, "y": 5.2},
        ...
      ]
    }
  ],
  "events": [
    {
      "time": 30.0,
      "type": "fire",
      "position": [40, 40],
      "radius": 5.0
    }
  ]
}
```

---

## 7. Traffic Control System

### 7.1 Architecture

**Purpose:** Realistic intersection behavior with traffic light compliance

**Components:**

1. **Traffic Lights**: Position, orientation (NS/EW), current state
2. **Crossing Lanes**: Pedestrian crossing zones (zebra crossings)
3. **Detection System**: Checks if pedestrians should stop
4. **Cycling System**: Automatic 30-second alternating cycle

### 7.2 Traffic Light Placement

```
Typical Intersection Layout:

        N (↑)
         │
    ┌────┼────┐
 W ─┤    ●    ├─ E
    │  (TL1)  │
    └────┼────┘
         │
        S (↓)

● = Traffic Light Position
Crossings: NS crossing (E-W direction), EW crossing (N-S direction)
```

**Configuration:**

```json
{
  "trafficLights": [
    {
      "position": [50, 25],     // Center of intersection
      "orientation": "ns",       // Controls NS crossing
      "crossingIndex": 0         // Links to crossingLanes[0]
    },
    {
      "position": [50, 25],
      "orientation": "ew",
      "crossingIndex": 1
    }
  ],
  "crossingLanes": [
    {
      "start": [48, 25],         // NS crossing (goes E-W)
      "end": [52, 25],
      "width": 4.0,
      "orientation": "ns"
    },
    {
      "start": [50, 23],         // EW crossing (goes N-S)
      "end": [50, 27],
      "width": 4.0,
      "orientation": "ew"
    }
  ]
}
```

### 7.3 Detection Algorithm

**File:** `src/simulation/environment.py` → `get_traffic_light_state()`

**Stages:**

```python
def get_traffic_light_state(position, velocity):
    for each crossing with traffic light:
        # Stage 1: Calculate geometry
        crossing_vector = end - start
        crossing_length = |crossing_vector|
        crossing_direction = crossing_vector / crossing_length
        perpendicular = rotate_90(crossing_direction)
        
        # Stage 2: Project pedestrian onto crossing
        to_pedestrian = position - crossing_start
        proj_on_crossing = dot(to_pedestrian, crossing_direction)
        perp_dist = |dot(to_pedestrian, perpendicular)|
        
        # Stage 3: On-crossing exception
        if perp_dist < width/2.0:  # Within 2m
            print("ON CROSSING - continue")
            continue  # Don't stop mid-crossing
        
        # Stage 4: Approach zone check
        lateral_buffer = 5.0
        stop_distance = width/2 + 3.0
        
        if perp_dist > lateral_buffer:
            continue  # Too far laterally
        
        # Stage 5: Movement direction check
        alignment = dot(velocity, crossing_direction)
        perp_alignment = dot(velocity, perpendicular)
        moving_toward = perp_alignment < 0  # Moving toward crossing
        
        if not moving_toward:
            continue  # Moving away
        
        # Stage 6: Lateral bounds check
        within_bounds = 0 <= proj_on_crossing <= crossing_length
        
        if not within_bounds:
            continue  # Outside crossing laterally
        
        # Stage 7: Check light state
        if light_state == 'red':
            return 'stop'
        else:
            return 'go'
    
    return None  # No applicable traffic light
```

**Key Innovation: On-Crossing Exception**

Problem solved: Pedestrians were getting stuck MID-CROSSING when lights changed.

```python
# Solution:
if perp_dist < width/2.0:  # Pedestrian within 2m of crossing center
    # They're already ON the crossing - let them finish!
    continue  # Skip this crossing in detection
```

This prevents the "freeze mid-crosswalk" bug while maintaining safety.

### 7.4 Stopping Behavior

**Simulator Integration:**

```python
# In simulator.step():
for pedestrian in pedestrians:
    light_state = environment.get_traffic_light_state(
        pedestrian.position,
        pedestrian.velocity
    )
    
    if light_state == 'stop':
        pedestrian.velocity = np.array([0.0, 0.0])
        continue  # Skip force calculation (frozen)
    
    # Otherwise, calculate forces and move normally
```

### 7.5 Visual Rendering

**Traffic Light Display:**

```javascript
// Draw traffic light (last render layer)
function drawTrafficLight(light) {
    const pos = toIso(light.position.x, light.position.y);
    
    // Pole
    ctx.fillStyle = '#333';
    ctx.fillRect(pos.x - 2, pos.y - 30, 4, 30);
    
    // Housing
    ctx.fillStyle = '#222';
    ctx.fillRect(pos.x - 6, pos.y - 40, 12, 10);
    
    // Light
    if (light.state === 'red') {
        ctx.fillStyle = '#ff0000';
        ctx.beginPath();
        ctx.arc(pos.x, pos.y - 35, 4, 0, Math.PI * 2);
        ctx.fill();
    } else {
        ctx.fillStyle = '#00ff00';
        ctx.beginPath();
        ctx.arc(pos.x, pos.y - 35, 4, 0, Math.PI * 2);
        ctx.fill();
    }
}
```

---

## 8. Rendering System

### 8.1 Isometric Transformation

**Mathematical Basis:**

```
Standard isometric projection (30° angle):

x' = (x - y) * cos(30°) = (x - y) * 0.866
y' = (x + y) * sin(30°) - z = (x + y) * 0.5 - z

For 2D (z=0):
x' = (x - y) * 0.866 * scale
y' = (x + y) * 0.5 * scale
```

**Implementation:**

```javascript
function toIso(x, y, scale = 5) {
    return {
        x: (x - y) * Math.cos(Math.PI / 6) * scale,
        y: (x + y) * Math.sin(Math.PI / 6) * scale
    };
}
```

### 8.2 Layer Rendering Order

**Painter's Algorithm** (back-to-front):

```javascript
function renderScene(state) {
    // Layer 1: Ground
    drawGround();
    
    // Layer 2: Roads
    state.roads.forEach(road => drawRoad(road));
    
    // Layer 3: Decorations (trees, ponds - NOT buildings)
    state.decorations.forEach(deco => {
        if (deco.type !== 'building') {
            drawDecoration(deco);
        }
    });
    
    // Layer 4: Walls (3D extruded)
    state.walls.forEach(wall => drawWall(wall));
    
    // Layer 5: Lane markings
    state.carLanes.forEach(lane => drawLane(lane));
    state.pedestrianLanes.forEach(lane => drawLane(lane));
    
    // Layer 6: Crossings (zebra stripes)
    state.crossingLanes.forEach(crossing => drawCrossing(crossing));
    
    // Layer 7: Zones
    state.entrances.forEach(ent => drawEntrance(ent));
    state.exits.forEach(exit => drawExit(exit));
    
    // Layer 8: Vehicles
    state.vehicles.forEach(vehicle => drawVehicle(vehicle));
    
    // Layer 9: Hazards
    state.hazard_zones.forEach(hazard => drawHazard(hazard));
    
    // Layer 10: Pedestrians
    state.pedestrians.forEach(ped => drawPedestrian(ped));
    
    // Layer 11: Buildings (isometric 3D)
    state.decorations.forEach(deco => {
        if (deco.type === 'building') {
            drawIsoBuilding(deco);
        }
    });
    
    // Layer 12: Traffic Lights (ALWAYS ON TOP)
    state.trafficLights.forEach(light => drawTrafficLight(light));
}
```

**Rationale:**
- Buildings before traffic lights: Ensures traffic lights always visible
- Pedestrians before buildings: Shows people in front of structures
- Roads early: Provides base layer for all movement

### 8.3 Building Rendering (Isometric 3D)

**Algorithm:**

```javascript
function drawIsoBuilding(building) {
    const {x, y, width, height, color} = building;
    const scale = 5;
    const buildingHeight = Math.max(width, height) * scale * 1.2;
    
    // Step 1: Calculate 4 base corners
    const corners = [
        toIso(x, y),              // Top
        toIso(x + width, y),      // Right
        toIso(x + width, y + height), // Bottom
        toIso(x, y + height)      // Left
    ];
    
    // Step 2: Draw front face (vertical)
    const frontFaceColor = color || '#b0b0b0';
    ctx.fillStyle = frontFaceColor;
    ctx.beginPath();
    ctx.moveTo(corners[2].x, corners[2].y);
    ctx.lineTo(corners[3].x, corners[3].y);
    ctx.lineTo(corners[3].x, corners[3].y - buildingHeight);
    ctx.lineTo(corners[2].x, corners[2].y - buildingHeight);
    ctx.closePath();
    ctx.fill();
    
    // Step 3: Draw right face (diagonal, darker)
    const sideFaceColor = shadeColor(frontFaceColor, -30);
    ctx.fillStyle = sideFaceColor;
    ctx.beginPath();
    ctx.moveTo(corners[1].x, corners[1].y);
    ctx.lineTo(corners[2].x, corners[2].y);
    ctx.lineTo(corners[2].x, corners[2].y - buildingHeight);
    ctx.lineTo(corners[1].x, corners[1].y - buildingHeight);
    ctx.closePath();
    ctx.fill();
    
    // Step 4: Draw windows on front face (parallelograms)
    drawFrontWindows(corners[2], corners[3], buildingHeight);
    
    // Step 5: Draw windows on right face (rectangles)
    drawRightWindows(corners[1], corners[2], buildingHeight);
}
```

**Window Rendering:**

```javascript
// Front face: Isometric parallelograms
function drawFrontWindows(corner2, corner3, height) {
    const windowRows = 5;
    const windowCols = 3;
    
    // Calculate spacing
    const faceWidth = corner3.x - corner2.x;
    const spacingX = faceWidth / (windowCols + 1);
    const spacingY = height / (windowRows + 1);
    
    // Get face slope for parallelogram shape
    const faceDx = corner3.x - corner2.x;
    const faceDy = corner3.y - corner2.y;
    const perpDx = -faceDy;
    const perpDy = faceDx;
    const perpLen = Math.sqrt(perpDx**2 + perpDy**2);
    
    for (let row = 1; row <= windowRows; row++) {
        for (let col = 1; col <= windowCols; col++) {
            const wx = corner2.x + spacingX * col;
            const wy = corner2.y - height + spacingY * row;
            
            // Draw parallelogram window
            const windowW = 8;
            const windowH = 12;
            const offsetX = (perpDx / perpLen) * windowW / 2;
            const offsetY = (perpDy / perpLen) * windowW / 2;
            
            // Frame
            ctx.fillStyle = '#2c3e50';
            ctx.beginPath();
            ctx.moveTo(wx - offsetX, wy - offsetY - windowH/2);
            ctx.lineTo(wx + offsetX, wy + offsetY - windowH/2);
            ctx.lineTo(wx + offsetX, wy + offsetY + windowH/2);
            ctx.lineTo(wx - offsetX, wy - offsetY + windowH/2);
            ctx.closePath();
            ctx.fill();
            
            // Glass (gradient)
            const gradient = ctx.createLinearGradient(
                wx - 3, wy - 5, wx + 3, wy + 5
            );
            gradient.addColorStop(0, '#a8d8ea');
            gradient.addColorStop(1, '#4a7c8a');
            ctx.fillStyle = gradient;
            // ... draw glass parallelogram
        }
    }
}

// Right face: Simple rectangles
function drawRightWindows(corner1, corner2, height) {
    const windowRows = 5;
    const windowCols = 2;
    const spacingY = height / (windowRows + 1);
    
    for (let row = 1; row <= windowRows; row++) {
        for (let col = 1; col <= windowCols; col++) {
            // Position along diagonal edge
            const t = col / (windowCols + 1);
            const wx = corner1.x + (corner2.x - corner1.x) * t;
            const wy = corner1.y + (corner2.y - corner1.y) * t 
                      - height + spacingY * row;
            
            // Simple rectangle
            const windowW = 6;
            const windowH = 10;
            
            ctx.fillStyle = '#2c3e50';
            ctx.fillRect(wx - windowW/2, wy - windowH/2, windowW, windowH);
            
            // Glass
            const gradient = ctx.createLinearGradient(
                wx - windowW/2, wy - windowH/2,
                wx + windowW/2, wy + windowH/2
            );
            gradient.addColorStop(0, '#6b9eb5');
            gradient.addColorStop(1, '#3d5a6b');
            ctx.fillStyle = gradient;
            ctx.fillRect(
                wx - windowW/2 + 1, wy - windowH/2 + 1,
                windowW - 2, windowH - 2
            );
        }
    }
}
```

### 8.4 Pedestrian Rendering

**Color Coding by Panic Level:**

```javascript
function getPanicColor(panic_level) {
    // 0.0 = calm (green) → 1.0 = panicked (red)
    const r = Math.floor(panic_level * 255);
    const g = Math.floor((1 - panic_level) * 200);
    const b = 50;
    return `rgb(${r}, ${g}, ${b})`;
}

function drawPedestrian(ped) {
    const pos = toIso(ped.position[0], ped.position[1]);
    const color = getPanicColor(ped.panic_level);
    
    // Body (circle)
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 3, 0, Math.PI * 2);
    ctx.fill();
    
    // Velocity vector (if moving)
    if (speed > 0.1) {
        const velEnd = toIso(
            ped.position[0] + ped.velocity[0],
            ped.position[1] + ped.velocity[1]
        );
        ctx.strokeStyle = color;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.moveTo(pos.x, pos.y);
        ctx.lineTo(velEnd.x, velEnd.y);
        ctx.stroke();
    }
}
```

---

## 9. Emergency Event System

### 9.1 Event Types

**File:** `src/simulation/events.py`

**Supported Events:**

1. **Fire**: Creates panic zone, increases panic levels
2. **Shooting**: Immediate maximum panic, larger radius
3. **Entrance Blocked**: Closes spawn point
4. **Entrance Opened**: Reopens spawn point
5. **Exit Blocked**: Closes exit, forces re-routing
6. **Exit Opened**: Reopens exit

### 9.2 Event Scheduling

```python
class EventManager:
    def schedule_fire(self, trigger_time, position, radius):
        """Schedule fire event"""
        event = Event(
            type=EventType.FIRE,
            trigger_time=trigger_time,
            position=position,
            radius=radius
        )
        heapq.heappush(self.event_queue, event)
```

### 9.3 Event Processing

```python
# In simulator.step():
def process_events(self):
    """Process events that should trigger at current time"""
    while self.event_queue and self.event_queue[0].trigger_time <= self.time:
        event = heapq.heappop(self.event_queue)
        
        if event.type == EventType.FIRE:
            # Add hazard zone
            self.environment.add_hazard_zone(
                event.position,
                event.radius,
                'fire'
            )
            
            # Update pathfinding to avoid fire
            self.pathfinder.update_hazard_zones(
                self.environment.hazard_zones
            )
            
            # Increase panic for nearby pedestrians
            for ped in self.pedestrians:
                dist = np.linalg.norm(ped.position - event.position)
                if dist < event.radius * 2:
                    panic = 1.0 - (dist / (event.radius * 2))
                    ped.set_panic_level(panic)
                    
                    # Recalculate path to avoid fire
                    new_path = self.pathfinder.find_path(
                        ped.position,
                        ped.goal
                    )
                    ped.update_path(new_path)
```

### 9.4 Panic Response

**Behavioral Changes:**

```python
# Speed increase
effective_speed = max_speed * (1 + 0.5 * panic_level)
# At max panic (1.0): 50% speed increase

# Stronger repulsion
repulsion_strength = A_ped * (1 + panic_level)
# At max panic: 2x repulsion force

# Hazard avoidance
hazard_repulsion = A_hazard * exp(-distance / B_hazard)
# Stronger force, wider range than walls
```

---

## 10. Export & Integration

### 10.1 Unity Export System

**File:** `src/export/unity_exporter.py`

**Purpose:** Convert simulation data to Unity-compatible format

**Export Process:**

```python
class UnityExporter:
    def export_simulation(self, simulator, filename):
        """Export complete simulation to JSON"""
        
        data = {
            'metadata': {
                'export_time': datetime.now().isoformat(),
                'duration': simulator.time,
                'total_pedestrians': len(simulator.trajectory_data),
                'timestep': simulator.dt
            },
            'environment': simulator.environment.to_dict(),
            'trajectories': self._export_trajectories(simulator),
            'events': self._export_events(simulator)
        }
        
        filepath = f'exports/{filename}.json'
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filepath
```

### 10.2 Trajectory Recording

```python
# In simulator, when recording enabled:
def record_trajectories(self):
    """Capture pedestrian positions each timestep"""
    for ped in self.pedestrians:
        self.trajectory_data[ped.id].append({
            'time': self.time,
            'position': ped.position.tolist(),
            'velocity': ped.velocity.tolist(),
            'panic_level': ped.panic_level
        })
```

### 10.3 Unity Integration Script

**Generated C# Template:**

```csharp
using UnityEngine;
using System.Collections.Generic;

public class PedestrianSimulationPlayer : MonoBehaviour
{
    public TextAsset simulationDataJSON;
    public GameObject pedestrianPrefab;
    public GameObject wallPrefab;
    
    private SimulationData data;
    private Dictionary<int, GameObject> pedestrians;
    private float currentTime = 0f;
    
    void Start() {
        // Load JSON
        data = JsonUtility.FromJson<SimulationData>(
            simulationDataJSON.text
        );
        
        // Create environment
        CreateWalls();
        CreateEntrances();
        CreateExits();
        
        // Prepare pedestrian pool
        pedestrians = new Dictionary<int, GameObject>();
    }
    
    void Update() {
        currentTime += Time.deltaTime;
        
        // Update each pedestrian's position
        foreach (var trajectory in data.trajectories) {
            UpdatePedestrianPosition(trajectory, currentTime);
        }
    }
    
    void UpdatePedestrianPosition(Trajectory traj, float time) {
        // Find position at current time (interpolate if needed)
        Vector3 position = InterpolatePosition(traj, time);
        
        // Create or update pedestrian GameObject
        if (!pedestrians.ContainsKey(traj.pedestrian_id)) {
            pedestrians[traj.pedestrian_id] = 
                Instantiate(pedestrianPrefab, position, Quaternion.identity);
        } else {
            pedestrians[traj.pedestrian_id].transform.position = position;
        }
    }
}
```

---

## 11. Performance Considerations

### 11.1 Computational Complexity

**Per Timestep:**

```
Pedestrian spawning:     O(E)  where E = number of entrances
Traffic light updates:   O(T)  where T = number of traffic lights
Pathfinding (if needed): O(N * (W*H) * log(W*H))  A* for N pedestrians
Social force calculation: O(N^2)  pairwise pedestrian interactions
Position updates:        O(N)  where N = number of pedestrians
Goal checking:           O(N)
Event processing:        O(log E)  priority queue

Total: O(N^2) dominated by social force interactions
```

### 11.2 Optimization Strategies

**1. Spatial Partitioning**

```python
# Divide space into grid cells
cell_size = 5.0  # meters
grid = defaultdict(list)

# Assign pedestrians to cells
for ped in pedestrians:
    cell_x = int(ped.position[0] / cell_size)
    cell_y = int(ped.position[1] / cell_size)
    grid[(cell_x, cell_y)].append(ped)

# Only check neighbors in same/adjacent cells
def get_neighbors(ped):
    cell_x = int(ped.position[0] / cell_size)
    cell_y = int(ped.position[1] / cell_size)
    
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            neighbors.extend(grid[(cell_x + dx, cell_y + dy)])
    
    return neighbors

# Reduces O(N^2) → O(N * k) where k = avg neighbors per cell
```

**2. Interaction Cutoff**

```python
# Only calculate repulsion within cutoff distance
interaction_radius = 2.0  # meters

for ped_j in neighbors:
    distance = np.linalg.norm(ped_i.position - ped_j.position)
    if distance > interaction_radius:
        continue  # Skip distant pedestrians
    
    # Calculate repulsion force
    force += calculate_repulsion(ped_i, ped_j)
```

**3. Pathfinding Caching**

```python
# Only recalculate path when:
# - Goal changes
# - Obstacles change
# - Hazard zones change

if not path_valid(ped.path, environment):
    ped.path = find_path(ped.position, ped.goal)
else:
    # Reuse existing path
    continue
```

**4. Rendering Optimization**

```javascript
// Only render pedestrians in viewport
function shouldRender(position) {
    const screenPos = toIso(position.x, position.y);
    return (
        screenPos.x >= -50 &&
        screenPos.x <= canvas.width + 50 &&
        screenPos.y >= -50 &&
        screenPos.y <= canvas.height + 50
    );
}

// Frustum culling
pedestrians.filter(shouldRender).forEach(drawPedestrian);
```

### 11.3 Scalability Limits

**Current System:**

| Pedestrians | FPS (approx) | Notes |
|------------|--------------|-------|
| 100 | 60 | Smooth, real-time |
| 500 | 30-40 | Acceptable |
| 1000 | 15-20 | Slightly laggy |
| 5000 | 5-10 | Slow, but functional |

**Recommendations:**

- **< 1000 pedestrians**: No optimization needed
- **1000-3000**: Enable spatial partitioning
- **> 3000**: Consider multi-threading (future)

---

## 12. Future Enhancements

### 12.1 Planned Features

**1. Multi-Floor Environments**

- Staircase navigation
- Elevator systems
- Floor-specific pathfinding
- 3D visualization layers

**2. Group Behavior**

```python
class PedestrianGroup:
    """Family/friend groups moving together"""
    
    def __init__(self, members):
        self.members = members  # List of pedestrian IDs
        self.cohesion_strength = 1.0
        
    def calculate_cohesion_force(self, ped):
        """Keep group together"""
        center = self.get_center_of_mass()
        direction = center - ped.position
        return direction * self.cohesion_strength
```

**3. Age/Mobility Variations**

```python
class Pedestrian:
    age_group: str  # 'child', 'adult', 'elderly'
    mobility: float  # 0.5 (wheelchair) to 1.0 (full mobility)
    
    def get_max_speed(self):
        base_speed = 1.3
        age_factor = {
            'child': 0.8,
            'adult': 1.0,
            'elderly': 0.6
        }[self.age_group]
        
        return base_speed * age_factor * self.mobility
```

**4. Machine Learning Integration**

- Neural network for pedestrian decision-making
- Reinforcement learning for evacuation optimization
- Predictive analytics for crowd flow

**5. Real-Time Data Integration**

- Import actual floor plans (DXF, SVG)
- Connect to real sensors (cameras, Wi-Fi tracking)
- Live crowd monitoring dashboard

### 12.2 Technical Debt

**Items to Address:**

1. **Replace Forward Euler with RK4**: More accurate integration
2. **Add Unit Tests**: Comprehensive coverage needed
3. **Optimize A***: Consider JPS (Jump Point Search) for grid pathfinding
4. **WebGL Rendering**: Hardware acceleration for large crowds
5. **Database Backend**: Store scenarios and simulation results

### 12.3 Research Extensions

**Potential Academic Applications:**

- Validate against real evacuation data
- Publish benchmarks for crowd simulation
- Contribute to open-source research platforms
- Integrate with existing tools (SUMO, MATSim)

---

## Appendix A: Key Equations

### Social Force Model

**Total Force:**
$$F_{total} = F_{drive} + \sum_{j \neq i} F_{ped,j} + \sum_{w} F_{wall,w} + \sum_{h} F_{hazard,h}$$

**Driving Force:**
$$F_{drive} = \frac{m(v_{desired} - v_{current})}{\tau}$$

**Pedestrian Repulsion:**
$$F_{ped} = A \cdot e^{\frac{r_{ij} - d_{ij}}{B}} \cdot \vec{n}_{ij}$$

**Wall Repulsion:**
$$F_{wall} = A_{wall} \cdot e^{\frac{-d_{wall}}{B_{wall}}} \cdot \vec{n}_{wall}$$

### A* Heuristic

**Manhattan Distance:**
$$h(n) = |n.x - goal.x| + |n.y - goal.y|$$

**Euclidean Distance:**
$$h(n) = \sqrt{(n.x - goal.x)^2 + (n.y - goal.y)^2}$$

### Isometric Projection

**2D to Isometric:**
$$x' = (x - y) \cdot \cos(30°) \cdot scale$$
$$y' = (x + y) \cdot \sin(30°) \cdot scale$$

---

## Appendix B: File Reference

### Core Simulation (Python)

| File | Lines | Purpose |
|------|-------|---------|
| `simulator.py` | 570 | Main simulation loop and control |
| `environment.py` | 458 | World geometry and traffic lights |
| `pedestrian.py` | 112 | Individual agent behavior |
| `social_force.py` | 252 | Physics-based movement model |
| `pathfinding.py` | 316 | A* navigation algorithm |
| `events.py` | 280 | Emergency event system |

### Web Interface (JavaScript/Python)

| File | Lines | Purpose |
|------|-------|---------|
| `app.py` | 365 | Flask server and WebSocket |
| `app.js` | 2529 | Frontend logic and rendering |
| `style.css` | ~500 | Modern dark theme UI |
| `index.html` | ~400 | Main interface structure |

### Export & Integration

| File | Lines | Purpose |
|------|-------|---------|
| `unity_exporter.py` | ~150 | JSON export for Unity |
| `UnitySceneTemplate.cs` | ~200 | Unity integration script |

---

## Appendix C: Configuration Reference

### Default Parameters

```json
{
  "simulation": {
    "timestep": 0.1,
    "target_pedestrian_count": 100,
    "simulation_speed": 1.0,
    "exit_selection_mode": "random"
  },
  "pedestrian": {
    "max_speed": 1.3,
    "radius": 0.3,
    "mass": 80.0,
    "relaxation_time": 0.5
  },
  "social_force": {
    "A_ped": 2000.0,
    "B_ped": 0.08,
    "A_wall": 2000.0,
    "B_wall": 0.08,
    "A_hazard": 5000.0,
    "B_hazard": 2.0
  },
  "pathfinding": {
    "cell_size": 0.5,
    "hazard_buffer": 1.5
  },
  "traffic_lights": {
    "cycle_time": 30.0,
    "lateral_buffer": 5.0,
    "stop_distance": 5.0,
    "on_crossing_threshold": 2.0
  },
  "rendering": {
    "scale": 5,
    "canvas_width": 1200,
    "canvas_height": 800
  }
}
```

---

## Appendix D: API Reference

### WebSocket Events (Client → Server)

```javascript
// Create environment
socket.emit('create_environment', {
    width: 100.0,
    height: 100.0,
    walls: [...],
    entrances: [...],
    exits: [...]
});

// Start simulation
socket.emit('start_simulation', {
    num_pedestrians: 500,
    initial_pedestrians: 0,
    speed: 1.0,
    record: true,
    flow_rate: 2.0,
    exit_mode: 'nearest'
});

// Add emergency event
socket.emit('add_event', {
    type: 'fire',
    position: [40, 40],
    radius: 5.0,
    trigger_time: 30.0
});

// Load preset scenario
socket.emit('load_scenario', {
    scenario_id: 'downtown_street'
});

// Export to Unity
socket.emit('export_unity', {
    filename: 'my_simulation'
});
```

### WebSocket Events (Server → Client)

```javascript
// Simulation state update (every timestep)
socket.on('simulation_update', (state) => {
    // state.time
    // state.pedestrians[]
    // state.stats
    // state.environment
});

// Environment created
socket.on('environment_created', (data) => {
    // data.status
    // data.environment
});

// Simulation stopped
socket.on('simulation_stopped', (data) => {
    // data.reason
    // data.stats
});
```

---

**End of Design Document**

---

*This design document describes the architecture and implementation of the Pedestrian Simulation System v2.0. For usage instructions, see README.md. For technical details, see DOCUMENTATION.md.*
