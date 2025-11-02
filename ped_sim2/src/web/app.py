"""
Flask web application for pedestrian simulation.
"""
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.environment import Environment
from simulation.simulator import Simulator
from simulation.events import EventType
from export.unity_exporter import UnityExporter

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pedestrian_simulation_secret_key'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global simulator instance
simulator = None
running = False
exporter = UnityExporter()


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')


@socketio.on('create_environment')
def handle_create_environment(data):
    """Create new environment from client data."""
    global simulator
    
    try:
        width = data.get('width', 50.0)
        height = data.get('height', 50.0)
        
        env = Environment(width, height)
        
        # Add walls
        for wall in data.get('walls', []):
            env.add_wall(
                tuple(wall['start']),
                tuple(wall['end'])
            )
        
        # Add entrances
        for entrance in data.get('entrances', []):
            env.add_entrance(
                tuple(entrance['position']),
                entrance.get('radius', 1.0),
                entrance.get('flow_rate', 2.0)
            )
        
        # Add exits
        for exit_zone in data.get('exits', []):
            env.add_exit(
                tuple(exit_zone['position']),
                exit_zone.get('radius', 1.5)
            )
        
        # Create simulator
        simulator = Simulator(env, dt=0.1)
        
        emit('environment_created', {
            'status': 'success',
            'environment': env.to_dict()
        })
        
    except Exception as e:
        emit('environment_created', {
            'status': 'error',
            'message': str(e)
        })


@socketio.on('start_simulation')
def handle_start_simulation(data):
    """Start the simulation."""
    global running, simulator
    
    try:
        if simulator is None:
            emit('simulation_error', {'message': 'No environment created'})
            return
        
        # Get simulation parameters
        num_pedestrians = data.get('num_pedestrians', 100)
        initial_pedestrians = data.get('initial_pedestrians', 0)
        speed = data.get('speed', 1.0)
        record = data.get('record', False)
        flow_rate = data.get('flow_rate', None)
        exit_mode = data.get('exit_mode', 'random')
        
        print(f"Starting simulation: {num_pedestrians} peds, {initial_pedestrians} initial, speed {speed}, exit_mode {exit_mode}")
        
        # Update flow rate for all entrances if provided
        if flow_rate is not None:
            for entrance in simulator.environment.entrances:
                entrance['flow_rate'] = flow_rate
        
        # Set target pedestrian count on simulator
        simulator.target_pedestrian_count = num_pedestrians
        simulator.simulation_speed = speed
        simulator.exit_selection_mode = exit_mode
        
        # Pre-populate the map with initial pedestrians
        if initial_pedestrians > 0:
            print(f"Pre-populating {initial_pedestrians} pedestrians...")
            simulator.pre_populate_pedestrians(initial_pedestrians)
            print(f"Pre-populated. Now have {len(simulator.pedestrians)} pedestrians")
        
        running = True
        
        if record:
            simulator.start_recording()
        
        emit('simulation_started', {'status': 'running'})
        print("Simulation started, starting background task...")
        
        # Start simulation loop in background task
        socketio.start_background_task(run_simulation_loop)
        
    except Exception as e:
        print(f"ERROR in start_simulation: {e}")
        import traceback
        traceback.print_exc()
        emit('simulation_error', {'message': str(e)})


def run_simulation_loop():
    """Run simulation loop and emit updates."""
    global running, simulator
    
    while running and simulator is not None:
        # Run one step
        simulator.step()
        
        # Send state update to clients
        state = simulator.get_state()
        socketio.emit('simulation_update', state)
        
        # Continue loop if running and (still spawning OR pedestrians active)
        still_spawning = simulator.stats['spawned'] < simulator.target_pedestrian_count
        has_active_peds = simulator.stats['active'] > 0
        
        print(f"Loop: spawned={simulator.stats['spawned']}/{simulator.target_pedestrian_count}, active={simulator.stats['active']}, still_spawning={still_spawning}, has_active={has_active_peds}")
        
        if not (still_spawning or has_active_peds):
            # Simulation complete
            running = False
            print(f"Simulation stopping: reason={'complete' if simulator.stats['spawned'] >= simulator.target_pedestrian_count else 'no active'}")
            socketio.emit('simulation_stopped', {
                'reason': 'Simulation complete' if simulator.stats['spawned'] >= simulator.target_pedestrian_count else 'No active pedestrians',
                'stats': simulator.stats
            })
            break
        
        # Apply simulation speed to sleep time
        sleep_time = simulator.dt / simulator.simulation_speed
        socketio.sleep(sleep_time)
    
    if not running:
        print("Loop exiting: simulation stopped by user")


@socketio.on('stop_simulation')
def handle_stop_simulation():
    """Stop the simulation."""
    global running, simulator
    
    running = False
    
    if simulator and simulator.recording:
        simulator.stop_recording()
    
    emit('simulation_stopped', {
        'reason': 'User stopped',
        'stats': simulator.stats if simulator else {}
    })


@socketio.on('reset_simulation')
def handle_reset_simulation():
    """Reset the simulation."""
    global running, simulator
    
    running = False
    
    if simulator:
        simulator.reset()
        emit('simulation_reset', {'status': 'success'})
    else:
        emit('simulation_error', {'message': 'No simulator to reset'})


@socketio.on('add_event')
def handle_add_event(data):
    """Add an emergency event."""
    global simulator
    
    if simulator is None:
        emit('event_error', {'message': 'No simulator created'})
        return
    
    try:
        event_type = data.get('type')
        trigger_time = data.get('trigger_time', simulator.time + 5.0)
        
        if event_type == 'fire':
            simulator.event_manager.schedule_fire(
                trigger_time,
                tuple(data['position']),
                data.get('radius', 5.0)
            )
        elif event_type == 'shooting':
            simulator.event_manager.schedule_shooting(
                trigger_time,
                tuple(data['position']),
                data.get('radius', 10.0)
            )
        elif event_type == 'entrance_blocked':
            simulator.event_manager.schedule_entrance_closure(
                trigger_time,
                data['entrance_idx']
            )
        elif event_type == 'entrance_opened':
            simulator.event_manager.schedule_entrance_opening(
                trigger_time,
                data['entrance_idx']
            )
        elif event_type == 'exit_blocked':
            simulator.event_manager.schedule_exit_closure(
                trigger_time,
                data['exit_idx']
            )
        elif event_type == 'exit_opened':
            simulator.event_manager.schedule_exit_opening(
                trigger_time,
                data['exit_idx']
            )
        
        emit('event_added', {
            'status': 'success',
            'type': event_type,
            'trigger_time': trigger_time
        })
        
    except Exception as e:
        emit('event_error', {'message': str(e)})


@socketio.on('export_unity')
def handle_export_unity(data):
    """Export simulation data for Unity."""
    global simulator
    
    if simulator is None:
        emit('export_error', {'message': 'No simulation to export'})
        return
    
    try:
        filename = data.get('filename')
        filepath = exporter.export_simulation(simulator, filename)
        
        # Also export Unity script template
        exporter.export_unity_scene_template()
        
        emit('export_complete', {
            'status': 'success',
            'filepath': filepath
        })
        
    except Exception as e:
        emit('export_error', {'message': str(e)})


@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    """Get all predefined scenarios."""
    scenarios_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'scenarios')
    scenarios = {}
    
    # Load each scenario file
    scenario_files = [
        'busy_intersection.json',
        'downtown_street.json',
        'campus.json',
        'hospital.json',
        'shopping_mall.json',
        'urban_park.json'
    ]
    
    for filename in scenario_files:
        filepath = os.path.join(scenarios_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    scenario_id = filename.replace('.json', '')
                    scenarios[scenario_id] = json.load(f)
            except Exception as e:
                print(f"Error loading scenario {filename}: {e}")
    
    return jsonify(scenarios)


@socketio.on('load_scenario')
def handle_load_scenario(data):
    """Load a preset scenario."""
    global simulator
    
    try:
        scenario_id = data.get('scenario_id')
        scenarios_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'scenarios')
        filepath = os.path.join(scenarios_dir, f'{scenario_id}.json')
        
        if not os.path.exists(filepath):
            emit('scenario_error', {'message': f'Scenario not found: {scenario_id}'})
            return
        
        # Load scenario
        with open(filepath, 'r', encoding='utf-8') as f:
            scenario_data = json.load(f)
        
        # Create environment from scenario
        env = Environment.from_dict(scenario_data['environment'])
        
        # Create simulator
        simulator = Simulator(env, dt=0.1)
        
        emit('scenario_loaded', {
            'status': 'success',
            'scenario': scenario_data,
            'environment': env.to_dict()
        })
        
        print(f"Loaded scenario: {scenario_data['name']} ({scenario_data['name_en']})")
        
    except Exception as e:
        emit('scenario_error', {'message': str(e)})
        print(f"Error loading scenario: {e}")


if __name__ == '__main__':
    print("Starting Pedestrian Simulation Server...")
    print("Open http://localhost:5000 in your browser")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
