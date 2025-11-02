# Pedestrian Simulation System - File Index

## 📁 Complete File Reference

### Root Level
```
ped_sim2/
├── README.md                    # Project overview and introduction
├── QUICKSTART.md                # Quick start guide for users
├── DOCUMENTATION.md             # Technical documentation
├── PROJECT_SUMMARY.md           # Complete feature summary
├── ARCHITECTURE.md              # System architecture diagrams
├── PRESET_SCENARIOS.md          # 🆕 Detailed guide for 5 preset scenarios (Chinese/English)
├── UPDATE_NOTES.md              # 🆕 Preset scenarios system update notes
├── FEATURES_CHECKLIST.md        # Requirements fulfillment checklist
├── VISUAL_GUIDE.md              # Visual tutorials with ASCII diagrams
├── FILE_INDEX.md                # This file - complete file reference
├── requirements.txt             # Python dependencies
├── config.json                  # Configuration parameters
├── .gitignore                   # Git ignore rules
├── run.bat                      # Windows launcher script
└── run.sh                       # Linux/Mac launcher script
```

### Source Code (`src/`)

#### Simulation Engine (`src/simulation/`)
```
src/simulation/
├── __init__.py                  # Package initialization
├── pedestrian.py                # Pedestrian agent class
│   └── Classes: Pedestrian
│   └── Features: Position, velocity, goals, panic levels
│
├── social_force.py              # Social Force Model implementation
│   └── Classes: SocialForceModel
│   └── Features: Helbing's model, repulsion forces
│
├── pathfinding.py               # A* pathfinding algorithm
│   └── Classes: PathFinder
│   └── Features: Grid-based navigation, obstacle avoidance
│
├── environment.py               # Environment and map management
│   └── Classes: Environment
│   └── Features: Walls, entrances, exits, hazards
│
├── events.py                    # Emergency event system
│   └── Classes: Event, EventManager, EventType
│   └── Features: Fire, shooting, blockages
│
└── simulator.py                 # Main simulation controller
    └── Classes: Simulator
    └── Features: Integration, statistics, recording
```

#### Web Interface (`src/web/`)
```
src/web/
├── app.py                       # Flask server with Socket.IO
│   └── Routes: /, /api/scenarios
│   └── Socket Events: create_environment, start_simulation, etc.
│
├── templates/
│   └── index.html               # Main web interface
│       └── Features: Canvas editor, controls, statistics
│
└── static/
    ├── style.css                # Responsive modern styling
    │   └── Features: Gradient backgrounds, clean UI
    │
    └── app.js                   # Client-side logic
        └── Features: Canvas rendering, Socket.IO client
```

#### Export System (`src/export/`)
```
src/export/
├── __init__.py                  # Package initialization
└── unity_exporter.py            # Unity VR export
    └── Classes: UnityExporter
    └── Features: JSON export, C# template generation
```

### Examples (`examples/`)
```
examples/
├── run_simulation.py            # Basic usage examples
│   └── Functions: create_simple_scenario(), create_emergency_scenario()
│   └── Features: Command-line examples, static visualization
│
├── generate_preset_scenarios.py # 🆕 Preset scenario generator
│   └── Classes: ScenarioGenerator
│   └── Functions: create_downtown_street(), create_campus(), etc.
│   └── Features: Generate 5 preset scenarios, create JSON files
│
└── demo_preset_scenarios.py     # 🆕 Interactive demo script
    └── Classes: ScenarioDemonstration
    └── Functions: demo_all_scenarios(), demo_single_scenario()
    └── Features: Run scenarios with events, visualization
```

### Scenarios (`scenarios/`) 🆕
```
scenarios/
├── downtown_street.json         # 🏙️ Downtown Street scenario (100×40m, 1000 peds)
├── campus.json                  # 🎓 Campus scenario (120×100m, 2000 peds)
├── hospital.json                # 🏥 Hospital scenario (90×80m, 800 peds)
├── shopping_mall.json           # 🏬 Shopping Mall scenario (100×80m, 3000 peds)
├── urban_park.json              # 🌳 Urban Park scenario (100×100m, 1500 peds)
└── scenarios_index.json         # Scenario index with metadata
```

### Tests (`tests/`)
```
tests/
├── test_all.py                  # Comprehensive test suite
│   └── Tests: All major components
│   └── Coverage: Pedestrian, forces, pathfinding, environment, events
│
└── test_preset_scenarios.py    # 🆕 Preset scenarios system tests
    └── Tests: Scenario files, Web API, environment loading
    └── Features: Comprehensive validation and reporting
```

### Exports (`exports/`)
```
exports/
└── .gitkeep                     # Directory placeholder
    └── Generated files:
        - simulation_YYYYMMDD_HHMMSS.json  # Unity export data
        - scene_template.txt                # C# script template
        - *_visualization.png               # 🆕 Scenario visualizations
```
```

## 🔧 Key Files Explained

### Core Simulation Files

**pedestrian.py**
- Represents individual pedestrian agents
- Manages position, velocity, goals, panic
- Methods: update_position(), set_panic_level(), update_path()

**social_force.py**
- Implements Helbing's Social Force Model
- Calculates: driving force, pedestrian repulsion, wall repulsion
- Methods: calculate_total_force(), calculate_driving_force()

**pathfinding.py**
- A* algorithm for navigation
- Grid-based obstacle avoidance
- Methods: find_path(), set_obstacle(), add_wall_segment()

**environment.py**
- Map representation with walls, zones
- Methods: add_wall(), add_entrance(), add_exit(), add_hazard_zone()
- Serialization: to_dict(), from_dict()

**events.py**
- Event scheduling and triggering
- Event types: Fire, shooting, blockages
- Methods: schedule_fire(), update(), register_callback()

**simulator.py**
- Main controller integrating all components
- Methods: step(), spawn_pedestrian(), reset()
- Features: Recording, statistics, event handling

### Web Interface Files

**app.py**
- Flask server with Socket.IO
- Handles: Environment creation, simulation control, events
- Socket events: create_environment, start_simulation, add_event

**index.html**
- Interactive web interface
- Sections: Controls, canvas, statistics
- Tools: Wall drawing, entrance/exit placement

**app.js**
- Client-side logic
- Canvas rendering and interaction
- Real-time updates via WebSocket

**style.css**
- Modern responsive design
- Gradient backgrounds, clean UI
- Mobile-friendly layout

### Export Files

**unity_exporter.py**
- Exports simulation data to JSON
- Generates C# script template
- Methods: export_simulation(), export_unity_scene_template()

## 📊 File Statistics

- **Total Python Files**: 14
- **Total Lines of Code**: ~3,500+
- **Total Documentation**: ~2,000+ lines
- **Test Coverage**: All major components
- **Configuration Files**: 3 (JSON, requirements.txt, .gitignore)

## 🎯 Usage Patterns

### For Running Simulation:
1. Start with: `run.bat` or `run.sh`
2. Or manually: `python src/web/app.py`

### For Testing:
1. Run: `python tests/test_all.py`

### For Examples:
1. Simple: `python examples/run_simulation.py --mode simple`
2. Emergency: `python examples/run_simulation.py --mode emergency`

### For Unity Export:
1. Enable recording in web interface
2. Run simulation
3. Click "Export to Unity"
4. Files appear in `exports/` folder

## 🔍 Finding Specific Features

| Feature | Primary File | Supporting Files |
|---------|-------------|------------------|
| Pedestrian Movement | pedestrian.py | social_force.py, simulator.py |
| Physics Model | social_force.py | pedestrian.py |
| Pathfinding | pathfinding.py | environment.py, simulator.py |
| Map Editing | app.js, index.html | app.py, environment.py |
| Emergency Events | events.py | simulator.py, app.py |
| Unity Export | unity_exporter.py | simulator.py, app.py |
| Web Interface | app.py, index.html | app.js, style.css |
| Real-time Updates | app.py (Socket.IO) | app.js |
| Visualization | app.js (Canvas) | style.css, index.html |
| Configuration | config.json | All modules |
| Testing | test_all.py | All source files |

## 💡 Quick Reference

**Want to modify pedestrian behavior?**
→ Edit `src/simulation/pedestrian.py` or `src/simulation/social_force.py`

**Want to change UI appearance?**
→ Edit `src/web/static/style.css` or `src/web/templates/index.html`

**Want to add new event types?**
→ Edit `src/simulation/events.py` and `src/web/app.py`

**Want to customize Unity export?**
→ Edit `src/export/unity_exporter.py`

**Want to create new scenarios?**
→ Add JSON files to `scenarios/` folder

**Want to test specific components?**
→ Run or modify `tests/test_all.py`
