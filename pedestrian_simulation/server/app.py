"""
Web Server - Provide map editing and simulation control API
"""
from flask import Flask, render_template, jsonify, request, send_file
from flask_cors import CORS
import numpy as np
import json
import threading
import time
from pathlib import Path
import sys

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))
from core.pedestrian_model import (
    SimulationEnvironment, EventType, PedestrianState
)

app = Flask(__name__)
CORS(app)

# 全局Simulation Environment
simulation = None
simulation_thread = None
simulation_running = False

def create_simulation(config):
    """根据配置创建Simulation Environment"""
    global simulation
    
    width = config.get('width', 50)
    height = config.get('height', 50)
    simulation = SimulationEnvironment(width, height)
    
    # 添加Obstacles/Walls
    for obs in config.get('obstacles', []):
        vertices = np.array(obs['vertices'])
        simulation.add_obstacle(vertices)
    
    # 添加Exit/Entrance
    for exit_data in config.get('exits', []):
        position = np.array(exit_data['position'])
        width = exit_data.get('width', 2.0)
        simulation.add_exit(position, width)
    
    # 生成行人
    spawn_config = config.get('pedestrian_spawn', {})
    num_pedestrians = spawn_config.get('count', 50)
    spawn_areas = spawn_config.get('areas', [])
    
    for _ in range(num_pedestrians):
        # 随机选择生成区域和目标
        if spawn_areas:
            area = spawn_areas[np.random.randint(len(spawn_areas))]
            x = np.random.uniform(area['x_min'], area['x_max'])
            y = np.random.uniform(area['y_min'], area['y_max'])
            position = np.array([x, y])
        else:
            position = np.random.rand(2) * [width, height]
        
        # 随机选择一个Exits作为目标
        if simulation.exits:
            goal = simulation.exits[np.random.randint(len(simulation.exits))].position
        else:
            goal = np.array([width/2, height/2])
        
        simulation.add_pedestrian(position, goal)
    
    return simulation

def simulation_loop():
    """仿真主循环"""
    global simulation, simulation_running
    
    while simulation_running and simulation:
        if len(simulation.pedestrians) == 0:
            break
        
        simulation.step()
        time.sleep(simulation.model.dt)
    
    simulation_running = False

@app.route('/')
def index():
    """主页 - 地图编辑器"""
    return render_template('editor.html')

@app.route('/api/start_simulation', methods=['POST'])
def start_simulation():
    """启动仿真"""
    global simulation, simulation_thread, simulation_running
    
    try:
        config = request.json
        simulation = create_simulation(config)
        
        simulation_running = True
        simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
        simulation_thread.start()
        
        return jsonify({
            'status': 'success',
            'message': 'Simulation started',
            'pedestrian_count': len(simulation.pedestrians)
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/stop_simulation', methods=['POST'])
def stop_simulation():
    """Stop simulation"""
    global simulation_running
    simulation_running = False
    return jsonify({'status': 'success', 'message': 'Simulation stopped'})

@app.route('/api/pause_simulation', methods=['POST'])
def pause_simulation():
    """Pause simulation"""
    global simulation_running
    simulation_running = False
    return jsonify({'status': 'success', 'message': 'Simulation paused'})

@app.route('/api/resume_simulation', methods=['POST'])
def resume_simulation():
    """Resume simulation"""
    global simulation_running, simulation_thread
    
    if not simulation_running and simulation:
        simulation_running = True
        simulation_thread = threading.Thread(target=simulation_loop, daemon=True)
        simulation_thread.start()
        return jsonify({'status': 'success', 'message': 'Simulation resumed'})
    return jsonify({'status': 'error', 'message': 'No simulation to resume'}), 400

@app.route('/api/trigger_event', methods=['POST'])
def trigger_event():
    """触发Emergency event"""
    global simulation
    
    if not simulation:
        return jsonify({'status': 'error', 'message': 'No active simulation'}), 400
    
    data = request.json
    event_type_str = data.get('event_type')
    position = np.array(data.get('position', [0, 0]))
    radius = data.get('radius', 5.0)
    intensity = data.get('intensity', 1.0)
    
    # 转换Event type
    event_type_map = {
        'fire': EventType.FIRE,
        'shooting': EventType.SHOOTING,
        'entrance_close': EventType.ENTRANCE_CLOSE,
        'entrance_open': EventType.ENTRANCE_OPEN
    }
    
    event_type = event_type_map.get(event_type_str)
    if not event_type:
        return jsonify({'status': 'error', 'message': 'Invalid event type'}), 400
    
    simulation.trigger_event(event_type, position, radius, intensity)
    
    return jsonify({
        'status': 'success',
        'message': f'Event {event_type_str} triggered at {position.tolist()}'
    })

@app.route('/api/get_state', methods=['GET'])
def get_state():
    """获取当前仿真状态"""
    global simulation
    
    if not simulation:
        return jsonify({'status': 'error', 'message': 'No active simulation'}), 400
    
    pedestrians_data = [
        {
            'id': p.id,
            'position': p.position.tolist(),
            'velocity': p.velocity.tolist(),
            'goal': p.goal.tolist(),
            'state': p.state.value,
            'panic_level': p.panic_level
        }
        for p in simulation.pedestrians
    ]
    
    exits_data = [
        {
            'position': e.position.tolist(),
            'width': e.width,
            'is_open': e.is_open
        }
        for e in simulation.exits
    ]
    
    stats = simulation.get_statistics()
    
    return jsonify({
        'status': 'success',
        'time': simulation.time,
        'pedestrians': pedestrians_data,
        'exits': exits_data,
        'statistics': stats,
        'is_running': simulation_running
    })

@app.route('/api/export_unity', methods=['POST'])
def export_unity():
    """ExportUnity格式数据"""
    global simulation
    
    if not simulation:
        return jsonify({'status': 'error', 'message': 'No simulation data'}), 400
    
    filename = 'simulation_data.json'
    filepath = Path(__file__).parent.parent / 'exports' / filename
    filepath.parent.mkdir(exist_ok=True)
    
    simulation.export_for_unity(str(filepath))
    
    return send_file(
        str(filepath),
        as_attachment=True,
        download_name=filename,
        mimetype='application/json'
    )

@app.route('/api/add_pedestrians', methods=['POST'])
def add_pedestrians():
    """动态添加行人"""
    global simulation
    
    if not simulation:
        return jsonify({'status': 'error', 'message': 'No active simulation'}), 400
    
    data = request.json
    count = data.get('count', 10)
    spawn_area = data.get('spawn_area', {})
    
    for _ in range(count):
        x = np.random.uniform(spawn_area.get('x_min', 0), spawn_area.get('x_max', 10))
        y = np.random.uniform(spawn_area.get('y_min', 0), spawn_area.get('y_max', 10))
        position = np.array([x, y])
        
        # 随机选择Exits
        if simulation.exits:
            goal = simulation.exits[np.random.randint(len(simulation.exits))].position
        else:
            goal = np.array([simulation.width/2, simulation.height/2])
        
        simulation.add_pedestrian(position, goal)
    
    return jsonify({
        'status': 'success',
        'message': f'Added {count} pedestrians',
        'total': len(simulation.pedestrians)
    })

@app.route('/api/save_scenario', methods=['POST'])
def save_scenario():
    """保存场景配置"""
    data = request.json
    scenario_name = data.get('name', 'scenario')
    
    filepath = Path(__file__).parent.parent / 'scenarios' / f'{scenario_name}.json'
    filepath.parent.mkdir(exist_ok=True)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return jsonify({'status': 'success', 'message': f'Scenario saved as {scenario_name}'})

@app.route('/api/load_scenario/<scenario_name>', methods=['GET'])
def load_scenario(scenario_name):
    """加载场景配置"""
    filepath = Path(__file__).parent.parent / 'scenarios' / f'{scenario_name}.json'
    
    if not filepath.exists():
        return jsonify({'status': 'error', 'message': 'Scenario not found'}), 404
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    return jsonify({'status': 'success', 'data': data})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
