# 🚶 Pedestrian Movement Simulation System

A comprehensive, production-ready pedestrian simulation system with **modern bilingual UI**, web-based map editing, real-time visualization, emergency event handling, and Unity VR export capabilities.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎨 NEW: Modern UI Redesign (v2.0)

**Complete UI overhaul with professional dark theme and bilingual support!**

### What's New
- 🌙 **Modern Dark Theme**: Professional color scheme reducing eye strain
- 🌏 **Bilingual Interface**: Full Chinese + English support throughout
- 📊 **Enhanced Statistics**: Beautiful card-based stats with icons and animations
- 🎯 **Improved UX**: Better organization, clearer visual hierarchy
- 🎨 **Rich Interactions**: Smooth animations and hover effects
- 📱 **Responsive Design**: Adapts to different screen sizes

**Documentation:**
- [UI Redesign Overview](UI_REDESIGN.md) - Comprehensive redesign details
- [Visual Comparison](UI_COMPARISON.md) - Before/after comparisons
- [Quick Reference](UI_QUICK_REFERENCE.md) - Developer guide
- [Visual Preview](UI_VISUAL_PREVIEW.md) - Layout and components

## ✨ Features

### 🎬 Preset Scenarios (NEW!)
- **5 Complex Urban Scenarios** ready to use:
  - 🏙️ **Downtown Street** - Busy street with traffic, crosswalks, subway stations
  - 🎓 **Campus** - University with academic buildings, dorms, cafeteria
  - 🏥 **Hospital** - Emergency, inpatient, and outpatient buildings
  - 🏬 **Shopping Mall** - Multi-level mall with shops and central atrium
  - 🌳 **Urban Park** - Open space with lake, trees, and event areas
- One-click scenario loading in web interface
- Pre-configured emergency events for each scenario
- Recommended pedestrian counts (500-5000)
- Detailed Chinese & English documentation

### �🎨 Web-Based Map Editor
- Interactive HTML5 canvas for drawing walls and obstacles
- Click-to-place entrances and exits
- Real-time environment preview
- Configurable flow rates and zone sizes

### 🧮 Realistic Pedestrian Simulation  
- **Social Force Model** (Helbing & Molnár, 1995)
- **A* Pathfinding** for intelligent navigation
- Natural movement with velocity and acceleration
- Collision avoidance and personal space

### 📊 Real-Time Visualization
- 2D animated display of pedestrian movements
- Color-coded panic levels (calm → panicked)
- Velocity vectors showing movement direction
- Live statistics dashboard

### 🚨 Emergency Events
- **Fire** events creating panic zones
- **Shooting** incidents with immediate response
- **Dynamic entrance/exit blocking**
- Automatic path recalculation
- Scheduled event triggers

### 🎮 Unity VR Export
- Complete JSON export of simulation data
- Pedestrian trajectories with timestamps
- Environment geometry (walls, zones)
- Event timeline
- C# script template for Unity integration

### ⚙️ Dynamic Parameters
- Adjustable pedestrian density
- Configurable flow rates
- Panic behavior customization
- Real-time parameter updates

## 🚀 Quick Start

### Installation

1. **Clone or download this repository**

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   
   **Windows:**
   ```bash
   run.bat
   ```
   
   **Linux/Mac:**
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
   
   **Or manually:**
   ```bash
   cd src/web
   python app.py
   ```

4. **Open your browser:**
   Navigate to `http://localhost:5000`

### Quick Start with Preset Scenarios

**Option 1: Use Web Interface (Easiest)**
1. Open http://localhost:5000 in your browser
2. Select a scenario from "🎬 Preset Scenarios" dropdown
   - Example: "🏙️ Downtown Street / 繁忙街道"
3. Click "▶️ Start" to begin simulation
4. Add emergency events from the "Emergency Events" section

**Option 2: Run Demo Script**
```bash
# Demo all 5 scenarios
python examples/demo_preset_scenarios.py

# Demo a specific scenario
python examples/demo_preset_scenarios.py downtown_street
```

**Option 3: Generate Scenario Files**
```bash
# Generate all scenario JSON files
python examples/generate_preset_scenarios.py
```

See [PRESET_SCENARIOS.md](PRESET_SCENARIOS.md) for detailed scenario documentation.

### First Custom Simulation

1. Set environment dimensions (e.g., 50m × 50m)
2. Click **"Create Custom Environment"**
3. Select **"Wall"** tool and click to draw walls
4. Select **"Entrance"** and click to place entrance
5. Select **"Exit"** and click to place exit
6. Click **"▶️ Start"** to run simulation
7. Watch pedestrians move in real-time!

## 📖 Usage Guide

### Creating Your Map

**Drawing Tools:**
- 🧱 **Wall**: Click start point, then end point
- 📥 **Entrance**: Click to place (configure flow rate first)
- 📤 **Exit**: Click to place
- 🗑️ **Clear**: Click near any element to remove it

**Tips:**
- Draw boundary walls first
- Place entrances on edges
- Place exits away from entrances
- Test with low flow rates initially

### Adding Emergency Events

1. **Select event type:**
   - 🔥 Fire (creates panic zone)
   - 🔫 Shooting (immediate panic)
   - 🚫 Block Entrance/Exit

2. **Set trigger time** (in seconds)

3. **Configure position** (for fire/shooting) or **index** (for blocking)

4. **Click "Add Event"**

Events trigger automatically during simulation!

### Exporting to Unity VR

1. ✅ **Enable "Record for Unity Export"** before starting
2. ▶️ **Run your simulation**
3. 📦 **Click "Export to Unity"** when complete
4. 📁 Files saved in `exports/` folder

**Unity Integration:**
- Import JSON file
- Use C# script from `exports/scene_template.txt`
- Create pedestrian and wall prefabs
- Assign to PedestrianSimulationPlayer
- Play scene for 3D visualization

## 💻 Command-Line Examples

Run pre-configured scenarios without web interface:

```bash
# Simple corridor
python examples/run_simulation.py --mode simple

# Emergency evacuation with fire
python examples/run_simulation.py --mode emergency

# Both scenarios
python examples/run_simulation.py --mode both
```

## 📁 Project Structure

```
ped_sim2/
├── src/
│   ├── simulation/       # Core simulation engine
│   │   ├── pedestrian.py # Pedestrian agent class
│   │   ├── social_force.py # Social force model
│   │   ├── pathfinding.py # A* pathfinding
│   │   ├── environment.py # Map and obstacles
│   │   ├── events.py     # Emergency event system
│   │   └── simulator.py  # Main simulation controller
│   ├── web/              # Web interface
│   │   ├── app.py        # Flask application
│   │   ├── static/       # CSS, JS files
│   │   └── templates/    # HTML templates
│   └── export/           # Unity export utilities
├── scenarios/            # Pre-defined scenarios
├── examples/             # Usage examples
├── tests/                # Test suite
├── exports/              # Exported simulation data
├── requirements.txt      # Python dependencies
├── run.bat / run.sh      # Easy launcher scripts
├── README.md             # This file
├── QUICKSTART.md         # Quick start guide
├── DOCUMENTATION.md      # Technical documentation
├── ARCHITECTURE.md       # System architecture
└── FILE_INDEX.md         # Complete file reference
```

## 🔬 Technical Details

### Social Force Model

Implements Helbing's Social Force Model with:
- **Driving Force**: Propels pedestrian toward goal
- **Repulsion Force**: Maintains personal space
- **Wall Force**: Prevents obstacle collision
- **Fluctuation**: Natural movement variation

### Pathfinding

- **Algorithm**: A* with 8-directional movement
- **Grid-based**: Dynamic obstacle mapping
- **Path Simplification**: Removes unnecessary waypoints
- **Dynamic Updates**: Recalculates when environment changes

### Panic Behavior

Panic level (0.0-1.0) affects:
- Movement speed (+50% at maximum panic)
- Repulsion strength (stronger at higher panic)
- Path selection (prefers safer routes)

## 🎯 Key Parameters

| Parameter | Default | Range | Description |
|-----------|---------|-------|-------------|
| Pedestrian Speed | 1.3 m/s | 0.8-2.0 | Normal walking speed |
| Flow Rate | 2.0 /sec | 0.1-10 | Pedestrians spawned per second |
| Entrance Radius | 1.0 m | 0.5-5.0 | Spawn zone size |
| Exit Radius | 1.5 m | 0.5-5.0 | Exit zone size |
| Fire Radius | 5.0 m | 3.0-15.0 | Panic zone radius |
| Timestep | 0.1 s | 0.05-0.3 | Simulation time step |

## 🧪 Testing

Run the comprehensive test suite:

```bash
python tests/test_all.py
```

Tests cover:
- ✅ Pedestrian behavior
- ✅ Social force calculations
- ✅ Pathfinding algorithms
- ✅ Environment management
- ✅ Event system
- ✅ Full simulation
- ✅ Unity export

## 📚 Documentation

- **[PRESET_SCENARIOS.md](PRESET_SCENARIOS.md)**: 🆕 Complete guide to 5 preset scenarios (Chinese & English)
- **[QUICKSTART.md](QUICKSTART.md)**: Step-by-step usage guide
- **[DOCUMENTATION.md](DOCUMENTATION.md)**: Technical details and API reference
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: System architecture diagrams
- **[FILE_INDEX.md](FILE_INDEX.md)**: Complete file reference
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)**: Feature summary
- **[VISUAL_GUIDE.md](VISUAL_GUIDE.md)**: Visual tutorials with ASCII diagrams

## 🌟 Preset Scenarios Overview

### 🏙️ Downtown Street (繁忙街道)
- **Size**: 100m × 40m
- **Pedestrians**: 500-1500 (recommended: 1000)
- **Features**: Two-way road, sidewalks, crosswalks, subway stations, bus stops
- **Events**: Traffic signal failure, road construction, fire

### 🎓 Campus (大学校园)
- **Size**: 120m × 100m
- **Pedestrians**: 500-3000 (recommended: 2000)
- **Features**: Academic buildings, dorms, library, cafeteria, road network
- **Events**: Building fire evacuation, gate closure, class rush hour

### 🏥 Hospital (医院)
- **Size**: 90m × 80m
- **Pedestrians**: 500-1000 (recommended: 800)
- **Features**: Emergency, inpatient, outpatient buildings, corridors
- **Events**: Fire evacuation, elevator failure, emergency route blockage

### 🏬 Shopping Mall (购物中心)
- **Size**: 100m × 80m
- **Pedestrians**: 1000-5000 (recommended: 3000)
- **Features**: Multi-level structure, shops, central atrium, rest areas
- **Events**: Large-scale fire, escalator failure, shooting/panic incident

### 🌳 Urban Park (城市公园)
- **Size**: 100m × 100m
- **Pedestrians**: 500-2000 (recommended: 1500)
- **Features**: Open space, lake, trees, event stage, food carts
- **Events**: Mass evacuation after event, sudden rain, shooting incident

See **[PRESET_SCENARIOS.md](PRESET_SCENARIOS.md)** for detailed documentation.

## 🔧 Customization

All parameters are configurable via `config.json`:

```json
{
  "pedestrian_defaults": {
    "max_speed": 1.3,
    "radius": 0.3
  },
  "social_force": {
    "pedestrian_repulsion": {"A": 2000.0, "B": 0.08}
  }
}
```

## 🎓 Based on Research

Implementation follows published research:
- Helbing, D., & Molnár, P. (1995). Social force model for pedestrian dynamics
- Helbing, D., et al. (2000). Simulating dynamical features of escape panic
- Hart, P. E., et al. (1968). A* pathfinding algorithm

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Multi-floor environments
- Group behavior (families, friends)
- Age/mobility variations
- Machine learning integration
- Additional export formats

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Troubleshooting

**Problem: No pedestrians appearing**
- Solution: Check flow rate > 0, entrance not inside wall

**Problem: Pedestrians stuck**  
- Solution: Ensure exits are accessible, reduce wall density

**Problem: Slow performance**
- Solution: Reduce flow rate, increase timestep to 0.2s

**Problem: Import errors**
- Solution: `pip install -r requirements.txt --upgrade`

## 📞 Support

For issues, questions, or feature requests, please refer to the documentation files or create an issue in the repository.
