# System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PEDESTRIAN SIMULATION SYSTEM                    │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│                         WEB INTERFACE LAYER                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────┐         ┌──────────────────┐                 │
│  │   HTML5 Canvas   │◄────────┤   JavaScript     │                 │
│  │  (Visualization) │         │   (app.js)       │                 │
│  └──────────────────┘         └──────────────────┘                 │
│           ▲                            │                             │
│           │                            │ Socket.IO                   │
│           │                            ▼                             │
│  ┌────────────────────────────────────────────────┐                 │
│  │            Flask Server (app.py)               │                 │
│  │  - REST API endpoints                          │                 │
│  │  - WebSocket communication                     │                 │
│  │  - Real-time event broadcasting                │                 │
│  └────────────────────────────────────────────────┘                 │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      SIMULATION ENGINE LAYER                         │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Simulator (Main Controller)                │  │
│  │  - Manages simulation loop                                    │  │
│  │  - Coordinates all subsystems                                 │  │
│  │  - Collects statistics                                        │  │
│  └──────────────────────────────────────────────────────────────┘  │
│           │              │              │              │             │
│           ▼              ▼              ▼              ▼             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌───────────┐ │
│  │ Social Force │ │  Pathfinding │ │ Event Manager│ │Environment│ │
│  │    Model     │ │   (A* Algo)  │ │  (Schedule)  │ │  (Map)    │ │
│  └──────────────┘ └──────────────┘ └──────────────┘ └───────────┘ │
│           │              │              │              │             │
│           └──────────────┴──────────────┴──────────────┘             │
│                            │                                         │
│                            ▼                                         │
│           ┌────────────────────────────────┐                        │
│           │      Pedestrian Agents         │                        │
│           │  - Position & Velocity         │                        │
│           │  - Goal & Path                 │                        │
│           │  - Panic Level                 │                        │
│           └────────────────────────────────┘                        │
│                                                                       │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         EXPORT LAYER                                 │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                    Unity Exporter                             │  │
│  │  - Trajectory Data (JSON)                                     │  │
│  │  - Environment Geometry                                       │  │
│  │  - Event Timeline                                             │  │
│  │  - C# Script Template                                         │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                            │                                         │
│                            ▼                                         │
│           ┌────────────────────────────────┐                        │
│           │        JSON Export File        │                        │
│           │  {                             │                        │
│           │    "metadata": {...},          │                        │
│           │    "environment": {...},       │                        │
│           │    "trajectories": [...],      │                        │
│           │    "events": [...]             │                        │
│           │  }                             │                        │
│           └────────────────────────────────┘                        │
│                            │                                         │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
                             ▼
                    ┌────────────────┐
                    │  Unity VR App  │
                    │   (3D Playback)│
                    └────────────────┘


DATA FLOW DIAGRAM:
==================

User Interaction ──► Web Interface ──► Flask Server ──► Simulator
                                                            │
                          ┌─────────────────────────────────┤
                          ▼                                 ▼
                    Social Forces ◄──► Pathfinding    Event Manager
                          │                                 │
                          ▼                                 │
                    Update Positions ◄────────────────────┘
                          │
                          ▼
                    Check Collisions & Goals
                          │
                          ▼
                    Update Statistics
                          │
                          ├──► WebSocket ──► Real-time Update
                          │
                          └──► Recording ──► Export ──► Unity


COMPONENT INTERACTIONS:
=======================

┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Pedestrian  │─────▶│Social Force │─────▶│ Environment │
│   Agent     │      │   Model     │      │   (Walls)   │
└─────────────┘      └─────────────┘      └─────────────┘
       │                    │                     │
       │                    ▼                     │
       │             Calculate Forces             │
       │                    │                     │
       └──────┬─────────────┴─────────────────────┘
              │
              ▼
       Update Position & Velocity
              │
              ▼
       ┌─────────────┐
       │ Pathfinder  │──► Find Route Around Obstacles
       └─────────────┘
              │
              ▼
       Update Waypoints
              │
              ▼
       Check Event Triggers ◄── Event Manager
              │
              ▼
       Update Panic Level
              │
              ▼
       Render to Canvas / Export


EMERGENCY EVENT FLOW:
=====================

Event Scheduled ──► Event Manager
                          │
                          ▼
                    Wait for Trigger Time
                          │
                          ▼
                    Event Triggered
                          │
     ┌────────────────────┼────────────────────┐
     ▼                    ▼                    ▼
Fire Event          Exit Blocked      Entrance Blocked
     │                    │                    │
     ▼                    ▼                    ▼
Create Hazard      Deactivate Exit    Deactivate Entrance
Zone                    │                    │
     │                  │                    │
     └──────────────────┴────────────────────┘
                        │
                        ▼
              Recalculate All Paths
                        │
                        ▼
              Update Pedestrian Goals
                        │
                        ▼
              Increase Panic Levels
                        │
                        ▼
              Continue Simulation
```

## Key Design Principles

1. **Modularity**: Each component is independent and can be modified separately
2. **Real-time**: WebSocket enables live updates without polling
3. **Scalability**: Physics calculations optimized for large crowds
4. **Extensibility**: Easy to add new behaviors, events, and export formats
5. **Separation of Concerns**: Simulation logic separate from visualization
