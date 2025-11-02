# 🎓 Visual User Guide

## Getting Started

### Step 1: Launch the Application

```
Windows:                    Linux/Mac:
┌─────────────────┐        ┌─────────────────┐
│  Double-click   │        │   ./run.sh      │
│   run.bat       │        │                 │
└─────────────────┘        └─────────────────┘
         │                          │
         └────────┬─────────────────┘
                  │
                  ▼
         ┌─────────────────┐
         │  Choose option: │
         │  1. Web App     │
         │  2. Simple Demo │
         │  3. Emergency   │
         │  4. Tests       │
         └─────────────────┘
```

### Step 2: Open Web Interface

```
Browser opens automatically to:
http://localhost:5000

┌──────────────────────────────────────────────────────────┐
│  🚶 Pedestrian Movement Simulation                       │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ┌───────────────┐  ┌─────────────────────────────────┐ │
│  │  Controls     │  │      Canvas (Map Editor)        │ │
│  │               │  │                                 │ │
│  │ Environment   │  │  [Your map appears here]        │ │
│  │ Setup         │  │                                 │ │
│  │               │  │  Click to draw walls,           │ │
│  │ Drawing Tools │  │  place entrances/exits          │ │
│  │               │  │                                 │ │
│  │ Simulation    │  │                                 │ │
│  │ Control       │  │                                 │ │
│  │               │  │                                 │ │
│  │ Events        │  │                                 │ │
│  │               │  │                                 │ │
│  │ Statistics    │  │                                 │ │
│  └───────────────┘  └─────────────────────────────────┘ │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

## Creating Your First Map

### Step 1: Set Environment Size

```
┌─────────────────────┐
│ Environment Setup   │
├─────────────────────┤
│ Width (m):  [  50 ] │
│ Height (m): [  50 ] │
│                     │
│ [Create Environment]│
└─────────────────────┘
```

### Step 2: Select Drawing Tool

```
┌──────────────────────┐
│   Drawing Tools      │
├──────────────────────┤
│  ┌────┐  ┌────┐     │
│  │🧱  │  │📥  │     │  Click buttons to select tool
│  │Wall│  │Ent │     │
│  └────┘  └────┘     │
│  ┌────┐  ┌────┐     │
│  │📤  │  │🗑️  │     │
│  │Exit│  │Clr │     │
│  └────┘  └────┘     │
└──────────────────────┘

Selected tool highlighted in blue
```

### Step 3: Draw Walls

```
Wall Drawing Process:
━━━━━━━━━━━━━━━━━━━━━

Click 1: Start Point        Click 2: End Point
    ┌─────────────┐             ┌─────────────┐
    │      ●      │             │      ●      │
    │             │      →      │      │      │
    │             │             │      │      │
    │             │             │      ●      │
    └─────────────┘             └─────────────┘
                                      ║
                                   Wall created!
```

### Step 4: Place Entrance

```
Before clicking:                After clicking:
┌─────────────┐                ┌─────────────┐
│             │                │     ○ ○     │ ← Green circle
│             │       →        │    ○ IN○    │   appears
│             │                │     ○ ○     │
└─────────────┘                └─────────────┘

Configure first:
Flow Rate: [2.0] peds/sec
Radius:    [1.0] meters
```

### Step 5: Place Exit

```
Before clicking:                After clicking:
┌─────────────┐                ┌─────────────┐
│             │                │             │
│             │       →        │     ○ ○     │ ← Red circle
│             │                │    ○OUT○    │   appears
└─────────────┘                └─────────────┘
```

## Running the Simulation

### Control Panel

```
┌──────────────────────┐
│ Simulation Control   │
├──────────────────────┤
│  [▶️ Start]          │  ← Click to begin
│  [⏸️ Stop ]          │  ← Pause simulation
│  [🔄 Reset]          │  ← Reset everything
│                      │
│  ☑ Record for Unity  │  ← Check to export
└──────────────────────┘
```

### What You'll See

```
Canvas during simulation:

┌─────────────────────────────────────┐
│  🟢         Entrance                │
│   ○ ○                               │
│    ○●●○  ← Pedestrians (blue dots) │
│     ○ ●  spawning                   │
│       ●●                            │
│  ═══════  ← Wall (black line)      │
│         ●●                          │
│          ●● → Moving towards exit   │
│           ●●                        │
│             ●●●                     │
│                ○ ○                  │
│               ○OUT○  ← Exit (red)   │
│                🔴                   │
└─────────────────────────────────────┘

Color coding:
● Blue = Calm pedestrian
● Orange = Moderate panic
● Red = High panic
```

### Statistics Display

```
┌──────────────────────┐
│    Statistics        │
├──────────────────────┤
│ Time:    [  23.5 ]s  │  ← Simulation time
│ Active:  [   12  ]   │  ← Currently moving
│ Spawned: [   45  ]   │  ← Total created
│ Exited:  [   33  ]   │  ← Reached exit
│ Avg Panic: [ 0.3 ]   │  ← Panic level
└──────────────────────┘
```

## Adding Emergency Events

### Fire Event

```
┌──────────────────────────┐
│   Emergency Events       │
├──────────────────────────┤
│ Event Type:              │
│  [Fire ▼]                │  ← Select "Fire"
│                          │
│ Trigger Time: [ 10 ]s    │  ← When to start
│                          │
│ X Position:   [ 25 ]     │  ← Fire location
│ Y Position:   [ 25 ]     │
│                          │
│  [Add Event]             │  ← Click to schedule
└──────────────────────────┘

Result on canvas:
┌──────────────────────┐
│         ●●●          │
│        ●●●●●         │  ← Pedestrians
│       ●   ●   ●      │    fleeing from
│      ● 🔥🔥🔥 ●     │    fire (red zone)
│       ● 🔥🔥 ●      │
│        ●   ●         │
│         ●●●          │
└──────────────────────┘
```

### Entrance Blocking

```
┌──────────────────────────┐
│   Emergency Events       │
├──────────────────────────┤
│ Event Type:              │
│  [Block Entrance ▼]      │
│                          │
│ Trigger Time: [ 15 ]s    │
│                          │
│ Entrance Index: [ 0 ]    │  ← Which entrance
│                          │    (0 = first)
│  [Add Event]             │
└──────────────────────────┘

Timeline:
0s ────────────── 15s ──────────────→
   Normal           🚫 Entrance blocked
   spawning            No more spawning
```

## Exporting to Unity

### Step 1: Enable Recording

```
Before starting simulation:

┌──────────────────────┐
│ Simulation Control   │
├──────────────────────┤
│  [▶️ Start]          │
│                      │
│  ☑ Record for Unity  │  ← CHECK THIS BOX!
└──────────────────────┘
```

### Step 2: Run Simulation

```
Let simulation complete:

[▶️ Running...]  →  [Completed]
     ↓
Recording trajectory data...
     ↓
Ready for export!
```

### Step 3: Export

```
┌──────────────────────┐
│      Export          │
├──────────────────────┤
│                      │
│  [📦 Export to Unity]│  ← Click here
│                      │
└──────────────────────┘
         ↓
    ┌────────────────────────────┐
    │ ✓ Export successful!       │
    │ File: exports/             │
    │   simulation_YYYYMMDD.json │
    └────────────────────────────┘
```

### Step 4: Use in Unity

```
Unity Project Structure:

Assets/
├── PedestrianSimulation/
│   ├── Data/
│   │   └── simulation_YYYYMMDD.json  ← Import here
│   ├── Scripts/
│   │   └── PedestrianSimulationPlayer.cs  ← Copy from exports/
│   ├── Prefabs/
│   │   ├── PedestrianPrefab  ← Create this
│   │   └── WallPrefab        ← Create this
│   └── Scenes/
│       └── SimulationScene

Setup:
1. Create empty GameObject
2. Add PedestrianSimulationPlayer script
3. Assign JSON file path
4. Assign prefabs
5. Press Play!
```

## Tips & Tricks

### Creating Complex Layouts

```
Strategy: Build incrementally

Step 1: Outer walls        Step 2: Add rooms
┌──────────────────┐       ┌──────────────────┐
│                  │       │  ┌────┐  ┌────┐  │
│                  │   →   │  │    │  │    │  │
│                  │       │  └────┘  └────┘  │
└──────────────────┘       └──────────────────┘

Step 3: Add corridors      Step 4: Place zones
┌──────────────────┐       ┌──────────────────┐
│  ┌────┐──┌────┐  │       │📥┌────┐──┌────┐  │
│  │    │  │    │  │   →   │  │    │  │    │📤│
│  └────┘──└────┘  │       │  └────┘──└────┘  │
└──────────────────┘       └──────────────────┘
```

### Optimal Flow Rates

```
Environment Size    Recommended Flow
─────────────────────────────────────
Small  (10-20m)     0.5 - 1.0 peds/s
Medium (20-50m)     1.0 - 3.0 peds/s
Large  (50-100m)    3.0 - 10.0 peds/s

Too high = overcrowding
Too low  = sparse simulation
```

### Event Timing

```
Simulation Timeline:
0s ──────── 10s ──────── 20s ──────── 30s →
    │           │           │
    │           │           └─ Exit blocks
    │           └─ Fire starts
    └─ Simulation starts

Recommendation:
- Wait 5-10s before first event
- Space events 5-10s apart
- Allow time to observe effects
```

## Keyboard Shortcuts (Planned)

```
Space   - Start/Stop simulation
R       - Reset simulation
E       - Export to Unity
1       - Wall tool
2       - Entrance tool
3       - Exit tool
4       - Clear tool
Esc     - Cancel current drawing
```

## Common Workflows

### Quick Test Run

```
1. Create 30×10 environment
2. Draw boundary walls
3. Place entrance (left)
4. Place exit (right)
5. Start simulation
6. Observe flow
   Total time: ~2 minutes
```

### Complex Scenario

```
1. Create 60×60 environment
2. Draw outer walls
3. Draw internal rooms
4. Place 3 entrances
5. Place 3 exits
6. Add walls for corridors
7. Schedule fire event (20s)
8. Schedule exit blocking (25s)
9. Enable recording
10. Start simulation
11. Export to Unity
    Total time: ~10 minutes
```

## Visual Reference

### Tool Icons
```
🧱 Wall     - Draw obstacles
📥 Entrance - Spawn point
📤 Exit     - Goal point
🗑️ Clear    - Remove elements
🔥 Fire     - Emergency event
🔫 Shooting - Panic event
🚫 Block    - Close access
```

### Status Colors
```
🟢 Green  - Entrance (active)
🔴 Red    - Exit / Fire hazard
🟡 Yellow - Warning
🔵 Blue   - Calm pedestrian
🟠 Orange - Moderate panic
⚫ Black  - Walls
```

---

**Ready to create your first simulation? Start with run.bat!**
