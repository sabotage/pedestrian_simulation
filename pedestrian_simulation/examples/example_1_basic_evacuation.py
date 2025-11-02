"""
Example 1: Basic Evacuation Scenario
Demonstrate a simple room evacuation scenario
"""
import numpy as np
import sys
from pathlib import Path

# 添加项目路径
sys.path.append(str(Path(__file__).parent.parent))

from core.pedestrian_model import SimulationEnvironment, EventType
from visualization.visualizer import SimulationVisualizer

def create_basic_evacuation_scene():
    """创建基础疏散场景"""
    
    # 创建30x30meters的环境
    env = SimulationEnvironment(width=30, height=30)
    
    # 创建房间Walls
    room_walls = np.array([
        [2, 2],   # 左下
        [28, 2],  # 右下
        [28, 28], # 右上
        [2, 28]   # 左上
    ])
    env.add_obstacle(room_walls)
    
    # 添加Exits（在南墙）
    env.add_exit(np.array([15, 2]), width=2.5)
    
    # 在房间内随机生成50个行人
    np.random.seed(42)  # 固定随机种子以便复现
    
    for i in range(50):
        # 在房间内部随机Position生成
        x = np.random.uniform(4, 26)
        y = np.random.uniform(4, 26)
        position = np.array([x, y])
        
        # 目标是Exits
        goal = np.array([15, 2])
        
        env.add_pedestrian(position, goal)
    
    print(f"场景创建完成:")
    print(f"- 环境大小: {env.width}x{env.height}meters")
    print(f"- Pedestrian count量: {len(env.pedestrians)}")
    print(f"- Exits数量: {len(env.exits)}")
    
    return env

def run_simulation(env, duration=60.0):
    """运行仿真"""
    print(f"\nStart simulation，时长: {duration}seconds")
    
    # 创建可视化器
    visualizer = SimulationVisualizer(env)
    
    # 运行动画
    visualizer.animate(duration=duration)
    
    # Export数据
    export_path = Path(__file__).parent.parent / 'exports' / 'basic_evacuation.json'
    export_path.parent.mkdir(exist_ok=True)
    env.export_for_unity(str(export_path))
    
    # 打印统计信息
    stats = env.get_statistics()
    print(f"\nSimulation complete:")
    print(f"- 总Time: {env.time:.2f}seconds")
    print(f"- Remaining pedestrians: {stats['current_pedestrians']}")
    print(f"- 平均疏散Time: {env.time:.2f}seconds")

if __name__ == '__main__':
    print("=" * 60)
    print("Example 1: Basic Evacuation Scenario")
    print("=" * 60)
    
    # 创建场景
    environment = create_basic_evacuation_scene()
    
    # 运行仿真
    run_simulation(environment, duration=60.0)
    
    print("\n数据已Export，Can be imported into Unity!")
