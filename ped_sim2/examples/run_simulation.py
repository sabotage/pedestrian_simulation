"""
Example script demonstrating the pedestrian simulation without web interface.
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.environment import Environment
from src.simulation.simulator import Simulator
from src.export.unity_exporter import UnityExporter


def create_simple_scenario():
    """Create a simple corridor scenario."""
    env = Environment(width=30, height=10)
    
    # Add boundary walls
    env.add_wall((0, 0), (30, 0))
    env.add_wall((30, 0), (30, 10))
    env.add_wall((30, 10), (0, 10))
    env.add_wall((0, 10), (0, 0))
    
    # Add entrance and exit
    env.add_entrance((2, 5), radius=1.5, flow_rate=2.0)
    env.add_exit((28, 5), radius=1.5)
    
    return env


def create_emergency_scenario():
    """Create an emergency evacuation scenario."""
    env = Environment(width=50, height=50)
    
    # Add boundary walls
    env.add_boundary_walls()
    
    # Add some internal walls (rooms)
    env.add_wall((25, 0), (25, 20))
    env.add_wall((25, 30), (25, 50))
    env.add_wall((0, 25), (20, 25))
    env.add_wall((30, 25), (50, 25))
    
    # Add entrances
    env.add_entrance((5, 5), radius=2.0, flow_rate=3.0)
    env.add_entrance((45, 5), radius=2.0, flow_rate=2.5)
    
    # Add exits
    env.add_exit((5, 45), radius=2.0)
    env.add_exit((45, 45), radius=2.0)
    env.add_exit((25, 45), radius=2.0)
    
    return env


def run_simulation_example():
    """Run a simple simulation example."""
    print("Creating environment...")
    env = create_simple_scenario()
    
    print("Initializing simulator...")
    sim = Simulator(env, dt=0.1)
    
    # Start recording for export
    sim.start_recording()
    
    print("Running simulation...")
    max_steps = 500
    
    for step in range(max_steps):
        sim.step()
        
        if step % 50 == 0:
            print(f"Step {step}: Active={sim.stats['active']}, "
                  f"Spawned={sim.stats['spawned']}, Exited={sim.stats['exited']}")
        
        # Stop if no more active pedestrians
        if sim.stats['active'] == 0 and step > 100:
            print("No more active pedestrians. Stopping simulation.")
            break
    
    sim.stop_recording()
    
    print("\nSimulation complete!")
    print(f"Total spawned: {sim.stats['spawned']}")
    print(f"Total exited: {sim.stats['exited']}")
    print(f"Final time: {sim.time:.1f}s")
    
    # Export to Unity
    print("\nExporting to Unity...")
    exporter = UnityExporter()
    filepath = exporter.export_simulation(sim)
    exporter.export_unity_scene_template()
    
    print(f"\nExport complete! Check the 'exports' folder.")
    
    return sim


def run_emergency_simulation():
    """Run an emergency evacuation simulation with events."""
    print("Creating emergency scenario...")
    env = create_emergency_scenario()
    
    print("Initializing simulator...")
    sim = Simulator(env, dt=0.1)
    
    # Schedule emergency events
    print("Scheduling emergency events...")
    sim.event_manager.schedule_fire(
        trigger_time=10.0,
        position=(25, 25),
        radius=8.0
    )
    sim.event_manager.schedule_exit_closure(
        trigger_time=15.0,
        exit_idx=1
    )
    
    # Start recording
    sim.start_recording()
    
    print("Running simulation with emergency events...")
    max_steps = 1000
    
    for step in range(max_steps):
        sim.step()
        
        if step % 100 == 0:
            print(f"Step {step}: Time={sim.time:.1f}s, Active={sim.stats['active']}, "
                  f"Avg Panic={sim.stats['total_panic']/max(sim.stats['active'], 1):.2f}")
        
        # Stop if no more active pedestrians
        if sim.stats['active'] == 0 and step > 200:
            print("No more active pedestrians. Stopping simulation.")
            break
    
    sim.stop_recording()
    
    print("\nEmergency simulation complete!")
    print(f"Total spawned: {sim.stats['spawned']}")
    print(f"Total exited: {sim.stats['exited']}")
    print(f"Event log: {len(sim.event_manager.get_event_log())} events triggered")
    
    # Export to Unity
    print("\nExporting to Unity...")
    exporter = UnityExporter()
    filepath = exporter.export_simulation(sim, filename="emergency_evacuation.json")
    
    print(f"\nExport complete!")
    
    return sim


def visualize_static(sim):
    """Create a static visualization of final state."""
    fig, ax = plt.subplots(figsize=(10, 10))
    
    env = sim.environment
    
    # Draw walls
    for wall in env.walls:
        ax.plot([wall[0][0], wall[1][0]], [wall[0][1], wall[1][1]], 
               'k-', linewidth=2)
    
    # Draw entrances
    for ent in env.entrances:
        circle = plt.Circle(ent['position'], ent['radius'], 
                          color='green', alpha=0.3, label='Entrance')
        ax.add_patch(circle)
    
    # Draw exits
    for exit_zone in env.exits:
        circle = plt.Circle(exit_zone['position'], exit_zone['radius'],
                          color='red', alpha=0.3, label='Exit')
        ax.add_patch(circle)
    
    ax.set_xlim(0, env.width)
    ax.set_ylim(0, env.height)
    ax.set_aspect('equal')
    ax.set_xlabel('X (meters)')
    ax.set_ylabel('Y (meters)')
    ax.set_title('Pedestrian Simulation Environment')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('simulation_environment.png', dpi=150)
    print("Static visualization saved as 'simulation_environment.png'")
    plt.show()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run pedestrian simulation examples')
    parser.add_argument('--mode', choices=['simple', 'emergency', 'both'], 
                       default='simple',
                       help='Simulation mode to run')
    
    args = parser.parse_args()
    
    if args.mode == 'simple':
        sim = run_simulation_example()
        visualize_static(sim)
    elif args.mode == 'emergency':
        sim = run_emergency_simulation()
        visualize_static(sim)
    else:
        print("Running both scenarios...\n")
        print("=" * 50)
        print("SIMPLE SCENARIO")
        print("=" * 50)
        sim1 = run_simulation_example()
        
        print("\n" + "=" * 50)
        print("EMERGENCY SCENARIO")
        print("=" * 50)
        sim2 = run_emergency_simulation()
        
        visualize_static(sim2)
