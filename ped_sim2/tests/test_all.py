"""
Test script to verify all components work correctly.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
from src.simulation.pedestrian import Pedestrian
from src.simulation.social_force import SocialForceModel
from src.simulation.pathfinding import PathFinder
from src.simulation.environment import Environment
from src.simulation.events import EventManager, EventType
from src.simulation.simulator import Simulator
from src.export.unity_exporter import UnityExporter


def test_pedestrian():
    """Test pedestrian creation and movement."""
    print("Testing Pedestrian class...")
    ped = Pedestrian(0, [0, 0], [10, 10], max_speed=1.5)
    
    assert ped.id == 0
    assert ped.active == True
    assert np.array_equal(ped.position, [0, 0])
    assert np.array_equal(ped.goal, [10, 10])
    
    # Test movement
    force = np.array([1.0, 1.0])
    ped.update_position(force, 0.1)
    assert not np.array_equal(ped.position, [0, 0])
    
    # Test panic
    ped.set_panic_level(0.8)
    assert ped.panic_level == 0.8
    
    print("✓ Pedestrian tests passed")


def test_social_force():
    """Test social force model."""
    print("Testing Social Force Model...")
    model = SocialForceModel()
    
    ped1 = Pedestrian(0, [0, 0], [10, 0])
    ped2 = Pedestrian(1, [1, 0], [10, 0])
    
    # Test driving force
    force = model.calculate_driving_force(ped1)
    assert force.shape == (2,)
    
    # Test pedestrian repulsion
    repulsion = model.calculate_pedestrian_repulsion(ped1, ped2)
    assert repulsion.shape == (2,)
    assert repulsion[0] < 0  # Should push away in negative x
    
    # Test wall repulsion
    walls = [[np.array([0, -1]), np.array([10, -1])]]
    wall_force = model.calculate_wall_repulsion(ped1, walls)
    assert wall_force.shape == (2,)
    
    print("✓ Social Force Model tests passed")


def test_pathfinding():
    """Test pathfinding."""
    print("Testing Pathfinding...")
    pathfinder = PathFinder((50, 50), cell_size=0.5)
    
    # Add obstacle
    pathfinder.set_obstacle(25, 25, 5, 5)
    
    # Find path
    start = np.array([10, 10])
    goal = np.array([40, 40])
    path = pathfinder.find_path(start, goal)
    
    assert len(path) > 0
    assert isinstance(path[0], np.ndarray)
    
    print("✓ Pathfinding tests passed")


def test_environment():
    """Test environment."""
    print("Testing Environment...")
    env = Environment(50, 50)
    
    # Add elements
    env.add_wall((0, 0), (50, 0))
    env.add_entrance((5, 25), radius=2.0, flow_rate=3.0)
    env.add_exit((45, 25), radius=2.0)
    env.add_hazard_zone((25, 25), radius=5.0, hazard_type='fire')
    
    assert len(env.walls) == 1
    assert len(env.entrances) == 1
    assert len(env.exits) == 1
    assert len(env.hazard_zones) == 1
    
    # Test hazard detection
    in_hazard, panic = env.is_point_in_hazard(np.array([25, 25]))
    assert in_hazard == True
    assert panic > 0
    
    # Test exit finding
    nearest_exit = env.get_nearest_exit(np.array([10, 25]))
    assert isinstance(nearest_exit, np.ndarray)
    
    # Test serialization
    data = env.to_dict()
    env2 = Environment.from_dict(data)
    assert env2.width == env.width
    assert len(env2.walls) == len(env.walls)
    
    print("✓ Environment tests passed")


def test_events():
    """Test event system."""
    print("Testing Event System...")
    event_mgr = EventManager()
    
    # Schedule events
    event_mgr.schedule_fire(5.0, (25, 25), radius=5.0)
    event_mgr.schedule_entrance_closure(10.0, entrance_idx=0)
    
    assert len(event_mgr.events) == 2
    
    # Test event triggering
    triggered = event_mgr.update(4.9)
    assert len(triggered) == 0
    
    triggered = event_mgr.update(5.1)
    assert len(triggered) == 1
    
    print("✓ Event System tests passed")


def test_simulator():
    """Test full simulator."""
    print("Testing Simulator...")
    
    # Create environment
    env = Environment(30, 10)
    env.add_wall((0, 0), (30, 0))
    env.add_wall((30, 0), (30, 10))
    env.add_wall((30, 10), (0, 10))
    env.add_wall((0, 10), (0, 0))
    env.add_entrance((2, 5), radius=1.5, flow_rate=5.0)
    env.add_exit((28, 5), radius=1.5)
    
    # Create simulator
    sim = Simulator(env, dt=0.1)
    
    # Run simulation
    for _ in range(100):
        sim.step()
    
    assert sim.time > 0
    assert sim.stats['spawned'] > 0
    
    # Test recording
    sim.start_recording()
    for _ in range(10):
        sim.step()
    sim.stop_recording()
    
    assert len(sim.trajectory_data) > 0
    
    # Test state
    state = sim.get_state()
    assert 'time' in state
    assert 'pedestrians' in state
    assert 'stats' in state
    
    print("✓ Simulator tests passed")


def test_unity_exporter():
    """Test Unity exporter."""
    print("Testing Unity Exporter...")
    
    # Create simple simulation
    env = Environment(20, 20)
    env.add_entrance((5, 10), radius=1.0, flow_rate=2.0)
    env.add_exit((15, 10), radius=1.0)
    
    sim = Simulator(env, dt=0.1)
    sim.start_recording()
    
    for _ in range(50):
        sim.step()
    
    sim.stop_recording()
    
    # Export
    exporter = UnityExporter(output_dir='test_exports')
    filepath = exporter.export_simulation(sim, filename='test_export.json')
    
    assert os.path.exists(filepath)
    
    # Export template
    template_path = exporter.export_unity_scene_template('test_template.txt')
    assert os.path.exists(template_path)
    
    # Cleanup
    os.remove(filepath)
    os.remove(template_path)
    os.rmdir('test_exports')
    
    print("✓ Unity Exporter tests passed")


def run_all_tests():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("Running Pedestrian Simulation Tests")
    print("=" * 50 + "\n")
    
    try:
        test_pedestrian()
        test_social_force()
        test_pathfinding()
        test_environment()
        test_events()
        test_simulator()
        test_unity_exporter()
        
        print("\n" + "=" * 50)
        print("✓ ALL TESTS PASSED!")
        print("=" * 50 + "\n")
        return True
        
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
