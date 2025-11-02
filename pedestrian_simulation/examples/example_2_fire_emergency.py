"""
Example 2: Fire Emergency Evacuation Scenario
Demonstrate fire emergency and pedestrian response in complex environment
"""
import numpy as np
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from core.pedestrian_model import SimulationEnvironment, EventType
from visualization.visualizer import SimulationVisualizer, AnalysisPlotter
import matplotlib.pyplot as plt

def create_complex_building():
    """创建复杂建筑场景"""
    
    # 创建50x50meters的大型建筑
    env = SimulationEnvironment(width=50, height=50)
    
    # 外墙
    outer_walls = np.array([
        [0, 0], [50, 0], [50, 50], [0, 50]
    ])
    env.add_obstacle(outer_walls)
    
    # 内部房间隔断
    # 中央走廊的Walls
    corridor_wall_1 = np.array([
        [0, 20], [20, 20], [20, 18], [0, 18]
    ])
    env.add_obstacle(corridor_wall_1)
    
    corridor_wall_2 = np.array([
        [30, 20], [50, 20], [50, 18], [30, 18]
    ])
    env.add_obstacle(corridor_wall_2)
    
    # 添加一些内部房间
    room_1 = np.array([
        [10, 25], [20, 25], [20, 35], [10, 35]
    ])
    env.add_obstacle(room_1)
    
    room_2 = np.array([
        [30, 25], [40, 25], [40, 35], [30, 35]
    ])
    env.add_obstacle(room_2)
    
    # 添加多个Exits
    env.add_exit(np.array([25, 0]), width=3.0)   # 南Exits（主Exits）
    env.add_exit(np.array([50, 25]), width=2.5)  # 东Exits
    env.add_exit(np.array([0, 25]), width=2.5)   # 西Exits
    env.add_exit(np.array([25, 50]), width=2.0)  # 北Exits（备用）
    
    # 生成行人 - 在不同区域
    np.random.seed(123)
    
    # 区域1: 南部区域 (30人)
    for _ in range(30):
        x = np.random.uniform(5, 45)
        y = np.random.uniform(2, 15)
        position = np.array([x, y])
        # 选择最近的Exits
        goal = env.exits[0].position  # 主Exits
        env.add_pedestrian(position, goal)
    
    # 区域2: 北部区域 (40人)
    for _ in range(40):
        x = np.random.uniform(5, 45)
        y = np.random.uniform(22, 48)
        position = np.array([x, y])
        # 选择随机Exits
        goal = env.exits[np.random.randint(len(env.exits))].position
        env.add_pedestrian(position, goal)
    
    # 区域3: 中央走廊 (30人)
    for _ in range(30):
        x = np.random.uniform(22, 28)
        y = np.random.uniform(5, 45)
        position = np.array([x, y])
        goal = env.exits[0].position
        env.add_pedestrian(position, goal)
    
    print(f"复杂建筑场景创建完成:")
    print(f"- 建筑Size: {env.width}x{env.height}meters")
    print(f"- 总Pedestrian count: {len(env.pedestrians)}")
    print(f"- Exits数量: {len(env.exits)}")
    print(f"- Obstacles数量: {len(env.obstacles)}")
    
    return env

def run_emergency_simulation(env):
    """运行应急仿真，包含Emergency event"""
    
    print("\n开始应急疏散仿真...")
    
    # 创建可视化器
    visualizer = SimulationVisualizer(env)
    
    # 记录是否已触发事件
    fire_triggered = False
    exit_closed = False
    
    # 自定义更新函数，在特定Time触发事件
    original_update = visualizer.update_frame
    
    def custom_update(frame):
        nonlocal fire_triggered, exit_closed
        
        # 在10seconds时触发Fire
        if env.time >= 10.0 and not fire_triggered:
            print(f"\n⚠️  Fire警报! Time: {env.time:.1f}seconds")
            print("   Position: Building center (25, 25)")
            env.trigger_event(
                event_type=EventType.FIRE,
                position=np.array([25, 25]),
                radius=12.0,
                intensity=0.9
            )
            fire_triggered = True
        
        # 在20seconds时关闭主Exits（模拟Exits堵塞）
        if env.time >= 20.0 and not exit_closed:
            print(f"\n🚪 主Exits堵塞! Time: {env.time:.1f}seconds")
            env.trigger_event(
                event_type=EventType.ENTRANCE_CLOSE,
                position=env.exits[0].position,
                radius=1.0
            )
            exit_closed = True
            
            # 重新为部分行人规划路线
            for ped in env.pedestrians:
                if np.linalg.norm(ped.goal - env.exits[0].position) < 5:
                    # 选择其他开放的Exits
                    open_exits = [e for e in env.exits if e.is_open]
                    if open_exits:
                        ped.update_goal(open_exits[0].position)
        
        return original_update(frame)
    
    visualizer.update_frame = custom_update
    
    # 运行仿真
    visualizer.animate(duration=90.0)
    
    # 生成分析报告
    generate_analysis_report(env)
    
    # Export Unity data
    export_path = Path(__file__).parent.parent / 'exports' / 'fire_emergency.json'
    export_path.parent.mkdir(exist_ok=True)
    env.export_for_unity(str(export_path))
    
    print("\n✅ Simulation complete，数据已Export!")

def generate_analysis_report(env):
    """生成分析报告"""
    
    print("\n" + "="*60)
    print("疏散分析报告")
    print("="*60)
    
    stats = env.get_statistics()
    
    print(f"\n基本统计:")
    print(f"  - 仿真时长: {env.time:.2f}seconds")
    print(f"  - 初始Pedestrian count: 100")
    print(f"  - successfully疏散: {100 - stats['current_pedestrians']}")
    print(f"  - Remaining pedestrians: {stats['current_pedestrians']}")
    print(f"  - 疏散率: {(100 - stats['current_pedestrians'])/100*100:.1f}%")
    
    # 生成可视化报告
    print("\n正在生成可视化分析图表...")
    
    # 1. Density Heatmap
    fig1 = AnalysisPlotter.plot_density_heatmap(env)
    fig1.savefig('density_heatmap.png', dpi=150, bbox_inches='tight')
    print("  ✓ Density Heatmap已保存: density_heatmap.png")
    
    # 2. Evacuation curve
    fig2 = AnalysisPlotter.plot_evacuation_time_distribution(env)
    fig2.savefig('evacuation_curve.png', dpi=150, bbox_inches='tight')
    print("  ✓ Evacuation curve已保存: evacuation_curve.png")
    
    # 3. Speed distribution
    if len(env.pedestrians) > 0:
        fig3 = AnalysisPlotter.plot_speed_distribution(env)
        fig3.savefig('speed_distribution.png', dpi=150, bbox_inches='tight')
        print("  ✓ Speed distribution已保存: speed_distribution.png")
    
    plt.close('all')
    
    print("\n建议:")
    if stats['current_pedestrians'] > 20:
        print("  ⚠️  疏散效率较低，建议:")
        print("     - 增加Exits数量")
        print("     - 优化ExitsPosition")
        print("     - 改善内部通道设计")
    else:
        print("  ✓ 疏散方案合理")
    
    print("="*60)

if __name__ == '__main__':
    print("=" * 60)
    print("Example 2: Fire Emergency Evacuation Scenario")
    print("=" * 60)
    
    # 创建复杂建筑场景
    environment = create_complex_building()
    
    # 运行应急仿真
    run_emergency_simulation(environment)
    
    print("\n📊 Analysis report and Unity data generated!")
    print("   Can be loaded in Unity 'fire_emergency.json' 文件")
