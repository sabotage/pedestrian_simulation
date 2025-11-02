# Pedestrian Simulation - Quick Start Guide

## Installation

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -c "import numpy, flask, scipy; print('All packages installed successfully!')"
   ```

## Running the Web Application

1. **Start the server:**
   ```bash
   cd src/web
   python app.py
   ```

2. **Open your browser:**
   Navigate to `http://localhost:5000`

3. **Create your simulation:**
   - Set environment dimensions
   - Click "Create Environment"
   - Select drawing tools (Wall, Entrance, Exit)
   - Click on canvas to draw
   - Configure entrance flow rates
   - Click "Start" to run simulation

## Running Command-Line Examples

1. **Simple corridor simulation:**
   ```bash
   python examples/run_simulation.py --mode simple
   ```

2. **Emergency evacuation scenario:**
   ```bash
   python examples/run_simulation.py --mode emergency
   ```

3. **Run both scenarios:**
   ```bash
   python examples/run_simulation.py --mode both
   ```

## Using Emergency Events

In the web interface:

1. **Fire Event:**
   - Select "Fire" from event type
   - Set position (X, Y coordinates)
   - Set trigger time in seconds
   - Click "Add Event"

2. **Entrance/Exit Blocking:**
   - Select appropriate event type
   - Specify entrance/exit index (0, 1, 2, ...)
   - Set trigger time
   - Click "Add Event"

## Exporting to Unity VR

1. **Enable recording:**
   - Check "Record for Unity Export" before starting simulation
   
2. **Run simulation:**
   - Complete the simulation run
   
3. **Export data:**
   - Click "Export to Unity" button
   - Files will be saved in `exports/` folder

4. **In Unity:**
   - Import the JSON file generated
   - Use the C# script template from `exports/scene_template.txt`
   - Create pedestrian and wall prefabs
   - Assign in the PedestrianSimulationPlayer component
   - Play the scene to visualize

## Tips

- **Entrance flow rate:** Higher values = more pedestrians per second
- **Panic response:** Pedestrians near hazards move faster and more erratically
- **Path recalculation:** Happens automatically when exits are blocked
- **Clear tool:** Click near any element to remove it

## Troubleshooting

**"Module not found" error:**
```bash
pip install -r requirements.txt --upgrade
```

**Canvas not drawing:**
- Ensure JavaScript console shows no errors
- Try refreshing the page
- Check that WebSocket connection is established

**Simulation running slow:**
- Reduce flow rate
- Decrease environment size
- Limit number of walls

## Advanced Usage

See `examples/run_simulation.py` for programmatic usage examples.
Modify parameters in simulation classes for fine-tuning behavior.
