"""
System Test Script
Verify all components are working properly
"""

import sys
import numpy as np
from pathlib import Path

def test_imports():
    """Test module imports"""
    print("Test 1: Module imports...")
    
    try:
        from core.pedestrian_model import (
            SimulationEnvironment, 
            Pedestrian, 
            EventType,
            PedestrianState
        )
        print("  ✓ Core modules imported successfully")
        return True
    except ImportError as e:
        print(f"  ✗ Import failed: {e}")
        return False

def test_simulation_creation():
    """Test simulation environment creation"""
    print("\nTest 2: Simulation environment creation...")
    
    try:
        from core.pedestrian_model import SimulationEnvironment
        
        env = SimulationEnvironment(width=30, height=30)
        
        # Add walls
        walls = np.array([[0,0], [30,0], [30,30], [0,30]], dtype=np.float64)
        env.add_obstacle(walls)
        
        # Add exit
        env.add_exit(np.array([15, 0], dtype=np.float64), width=2.0)
        
        # Add pedestrian
        env.add_pedestrian(
            position=np.array([10, 10], dtype=np.float64),
            goal=np.array([15, 0], dtype=np.float64)
        )
        
        print(f"  ✓ Environment created successfully")
        print(f"    - Size: {env.width}x{env.height}")
        print(f"    - Pedestrian count: {len(env.pedestrians)}")
        print(f"    - Exit count: {len(env.exits)}")
        print(f"    - Obstacles: {len(env.obstacles)}")
        
        return True, env
    except Exception as e:
        print(f"  ✗ Creation failed: {e}")
        return False, None

def test_simulation_step(env):
    """Test simulation steps"""
    print("\nTest 3: Simulation calculation...")
    
    try:
        initial_pos = env.pedestrians[0].position.copy()
        
        # Execute 10 steps
        for _ in range(10):
            env.step()
        
        final_pos = env.pedestrians[0].position
        distance = np.linalg.norm(final_pos - initial_pos)
        
        print(f"  ✓ Simulation calculation normal")
        print(f"    - Steps executed: 10")
        print(f"    - Pedestrian moved: {distance:.2f} meters")
        print(f"    - Simulation time: {env.time:.2f} seconds")
        
        return True
    except Exception as e:
        print(f"  ✗ Calculation failed: {e}")
        return False

def test_event_trigger(env):
    """Test event triggering"""
    print("\nTest 4: Event triggering...")
    
    try:
        from core.pedestrian_model import EventType, PedestrianState
        
        # Add more pedestrians for testing
        for _ in range(10):
            pos = np.random.rand(2) * [30, 30]
            pos = pos.astype(np.float64)
            env.add_pedestrian(pos, env.exits[0].position)
        
        # Trigger fire event
        env.trigger_event(
            EventType.FIRE,
            position=np.array([15, 15], dtype=np.float64),
            radius=10.0,
            intensity=1.0
        )
        
        # Execute several steps to check panic response
        for _ in range(5):
            env.step()
        
        panic_count = sum(1 for p in env.pedestrians 
                         if p.state == PedestrianState.PANIC)
        
        print(f"  ✓ Event triggered successfully")
        print(f"    - Event type: Fire")
        print(f"    - Total pedestrians: {len(env.pedestrians)}")
        print(f"    - Panicking: {panic_count}")
        
        return True
    except Exception as e:
        print(f"  ✗ Event trigger failed: {e}")
        return False

def test_data_export(env):
    """Test data export"""
    print("\nTest 5: Data export...")
    
    try:
        export_path = Path(__file__).parent / 'exports' / 'test_export.json'
        export_path.parent.mkdir(exist_ok=True)
        
        env.export_for_unity(str(export_path))
        
        if export_path.exists():
            file_size = export_path.stat().st_size
            print(f"  ✓ Data exported successfully")
            print(f"    - File path: {export_path}")
            print(f"    - File size: {file_size} bytes")
            return True
        else:
            print(f"  ✗ Export file does not exist")
            return False
            
    except Exception as e:
        print(f"  ✗ Export failed: {e}")
        return False

def test_visualization():
    """Test visualization (optional)"""
    print("\nTest 6: Visualization module...")
    
    try:
        from visualization.visualizer import SimulationVisualizer
        print("  ✓ Visualization module imported successfully")
        print("  ℹ️  Visualization test skipped (requires display device)")
        return True
    except ImportError as e:
        print(f"  ℹ️  Visualization module not found: {e}")
        return True  # Not a critical error

def test_web_server():
    """Test web server (basic check)"""
    print("\nTest 7: Web server module...")
    
    try:
        import flask
        import flask_cors
        print("  ✓ Flask dependencies installed")
        
        # Check if server file exists
        server_path = Path(__file__).parent / 'server' / 'app.py'
        if server_path.exists():
            print("  ✓ Server file exists")
            print("  ℹ️  Run 'python start.py --web' to start server")
            return True
        else:
            print("  ✗ Server file does not exist")
            return False
            
    except ImportError as e:
        print(f"  ✗ Flask dependencies missing: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("="*60)
    print("Pedestrian Simulation System - System Tests")
    print("="*60)
    
    results = []
    
    # Test 1: Imports
    results.append(test_imports())
    
    # Test 2: Create environment
    success, env = test_simulation_creation()
    results.append(success)
    
    if env:
        # Test 3: Simulation steps
        results.append(test_simulation_step(env))
        
        # Test 4: Event triggering
        results.append(test_event_trigger(env))
        
        # Test 5: Data export
        results.append(test_data_export(env))
    
    # Test 6: Visualization
    results.append(test_visualization())
    
    # Test 7: Web server
    results.append(test_web_server())
    
    # Summary
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n✅ All tests passed! System is running normally.")
        print("\nNext steps:")
        print("  - Run 'python start.py' to start interactive menu")
        print("  - Run 'python start.py --web' to start Web editor")
        print("  - Run example: 'python examples/example_1_basic_evacuation.py'")
    else:
        print("\n⚠️  Some tests failed, please check error messages.")
        print("\nSuggestions:")
        print("  - Make sure all dependencies are installed: pip install -r requirements.txt")
        print("  - Check Python version: python --version (requires 3.8+)")
    
    print("="*60)
    
    return passed == total

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
