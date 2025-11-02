"""
预置场景演示脚本
Preset Scenarios Demonstration Script

运行所有5个预置场景的演示，展示突发事件效果
"""
import sys
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from examples.generate_preset_scenarios import ScenarioGenerator
from src.simulation.simulator import Simulator
from src.simulation.events import EventType


class ScenarioDemonstration:
    """演示预置场景"""
    
    def __init__(self, scenario_name, env, recommended_peds):
        self.scenario_name = scenario_name
        self.env = env
        self.recommended_peds = recommended_peds
        self.simulator = Simulator(env, dt=0.1)
        
    def spawn_pedestrians(self, count=None):
        """生成行人"""
        if count is None:
            count = self.recommended_peds
        
        # 根据入口数量分配行人
        peds_per_entrance = count // len(self.env.entrances)
        
        for entrance_idx in range(len(self.env.entrances)):
            for _ in range(peds_per_entrance):
                self.simulator.spawn_pedestrian(entrance_idx=entrance_idx)
        
        print(f"✓ Spawned {self.simulator.stats['spawned']} pedestrians")
    
    def add_scenario_events(self):
        """根据场景类型添加典型突发事件"""
        if 'downtown_street' in self.scenario_name.lower():
            # 繁忙街道: 交通异常 + 火灾
            print("  Adding events: Traffic disruption + Fire")
            self.simulator.event_manager.schedule_fire(
                trigger_time=15.0,
                position=(50, 35),
                radius=8.0
            )
            
        elif 'campus' in self.scenario_name.lower():
            # 校园: 火灾疏散 + 正门封闭
            print("  Adding events: Building fire + Main gate closure")
            self.simulator.event_manager.schedule_fire(
                trigger_time=10.0,
                position=(27, 25),
                radius=15.0
            )
            if len(self.env.entrances) > 0:
                self.simulator.event_manager.schedule_entrance_closure(
                    trigger_time=25.0,
                    entrance_idx=0
                )
            
        elif 'hospital' in self.scenario_name.lower():
            # 医院: 火灾 + 急救通道阻塞
            print("  Adding events: Fire alarm + Emergency route blocked")
            self.simulator.event_manager.schedule_fire(
                trigger_time=12.0,
                position=(52, 25),
                radius=12.0
            )
            if len(self.env.entrances) > 0:
                self.simulator.event_manager.schedule_entrance_closure(
                    trigger_time=20.0,
                    entrance_idx=0
                )
            
        elif 'shopping_mall' in self.scenario_name.lower():
            # 购物中心: 大范围火灾 + Panic扩散
            print("  Adding events: Large fire + Panic spread")
            self.simulator.event_manager.schedule_fire(
                trigger_time=15.0,
                position=(50, 40),
                radius=20.0
            )
            self.simulator.event_manager.schedule_shooting(
                trigger_time=25.0,
                position=(85, 30),
                radius=15.0
            )
            
        elif 'urban_park' in self.scenario_name.lower():
            # 城市公园: 枪击事件 (大范围Panic)
            print("  Adding events: Shooting incident + Mass evacuation")
            self.simulator.event_manager.schedule_shooting(
                trigger_time=20.0,
                position=(50, 50),
                radius=25.0
            )
    
    def run_simulation(self, max_time=60.0, visualize=True):
        """运行模拟"""
        print(f"\n{'='*60}")
        print(f"Running scenario: {self.scenario_name}")
        print(f"{'='*60}")
        
        # 生成行人
        self.spawn_pedestrians()
        
        # 添加事件
        self.add_scenario_events()
        
        # 运行模拟
        print("\nSimulation progress:")
        step_count = 0
        while self.simulator.time < max_time and self.simulator.stats['active'] > 0:
            self.simulator.step()
            step_count += 1
            
            # 每10秒输出一次状态
            if step_count % 100 == 0:
                print(f"  Time: {self.simulator.time:6.1f}s | "
                      f"Active: {self.simulator.stats['active']:4d} | "
                      f"Exited: {self.simulator.stats['exited']:4d} | "
                      f"Max Panic: {max([p.panic_level for p in self.simulator.pedestrians] or [0.0]):.2f}")
        
        # 最终统计
        print(f"\n{'='*60}")
        print("Simulation completed!")
        print(f"Total time: {self.simulator.time:.1f}s")
        print(f"Total spawned: {self.simulator.stats['spawned']}")
        print(f"Successfully exited: {self.simulator.stats['exited']}")
        print(f"Remaining: {self.simulator.stats['active']}")
        print(f"{'='*60}\n")
        
        # 可视化
        if visualize:
            self.visualize_static()
    
    def visualize_static(self):
        """静态可视化最终状态"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 绘制墙体
        for wall in self.env.walls:
            # Handle both Wall objects and dict/list representations
            if hasattr(wall, 'start'):
                start, end = wall.start, wall.end
            elif isinstance(wall, dict):
                start, end = wall['start'], wall['end']
            else:  # list format
                start, end = wall[0], wall[1]
            
            xs = [start[0], end[0]]
            ys = [start[1], end[1]]
            ax.plot(xs, ys, 'k-', linewidth=2)
        
        # 绘制入口
        for ent in self.env.entrances:
            if hasattr(ent, 'position'):
                pos, radius = ent.position, ent.radius
            else:
                pos, radius = ent['position'], ent.get('radius', 1.0)
            
            circle = plt.Circle(pos, radius, 
                               color='green', alpha=0.3, label='Entrance')
            ax.add_patch(circle)
            ax.plot(pos[0], pos[1], 'g^', markersize=10)
        
        # 绘制出口
        for ext in self.env.exits:
            if hasattr(ext, 'position'):
                pos, radius = ext.position, ext.radius
            else:
                pos, radius = ext['position'], ext.get('radius', 1.5)
            
            circle = plt.Circle(pos, radius, 
                               color='blue', alpha=0.3, label='Exit')
            ax.add_patch(circle)
            ax.plot(pos[0], pos[1], 'bs', markersize=10)
        
        # 绘制危险区域
        if hasattr(self.env, 'hazards'):
            for hazard in self.env.hazards:
                if hasattr(hazard, 'position'):
                    pos, radius, htype = hazard.position, hazard.radius, hazard.type.value
                else:
                    pos, radius = hazard['position'], hazard.get('radius', 5.0)
                    htype = hazard.get('type', 'hazard')
                
                circle = plt.Circle(pos, radius, 
                                   color='red', alpha=0.5, label=htype)
                ax.add_patch(circle)
        
        # 绘制行人
        if self.simulator.pedestrians:
            positions = np.array([p.position for p in self.simulator.pedestrians])
            panic_levels = np.array([p.panic_level for p in self.simulator.pedestrians])
            
            scatter = ax.scatter(positions[:, 0], positions[:, 1], 
                               c=panic_levels, cmap='RdYlGn_r', 
                               s=30, alpha=0.6, vmin=0, vmax=1)
            plt.colorbar(scatter, ax=ax, label='Panic Level')
        
        ax.set_xlim(0, self.env.width)
        ax.set_ylim(0, self.env.height)
        ax.set_aspect('equal')
        ax.set_title(f'{self.scenario_name}\nFinal State (Time: {self.simulator.time:.1f}s)', 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.grid(True, alpha=0.3)
        
        # 去重图例
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right')
        
        plt.tight_layout()
        
        # 保存图像
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'exports')
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{self.scenario_name.lower().replace(' ', '_')}_visualization.png"
        filepath = os.path.join(output_dir, filename)
        plt.savefig(filepath, dpi=150, bbox_inches='tight')
        print(f"✓ Saved visualization: {filepath}")
        
        plt.show()


def demo_all_scenarios():
    """演示所有5个场景"""
    print("="*70)
    print(" 🎬 预置场景演示 / Preset Scenarios Demonstration")
    print("="*70)
    print("\nThis script will run all 5 preset scenarios with typical emergency events.")
    print("Each scenario will run for 60 seconds or until all pedestrians exit.\n")
    
    input("Press Enter to start the demonstrations...")
    
    generator = ScenarioGenerator()
    
    scenarios = [
        ("🏙️ Downtown Street (繁忙街道)", 
         generator.create_downtown_street(), 1000),
        
        ("🎓 Campus (大学校园)", 
         generator.create_campus(), 2000),
        
        ("🏥 Hospital (医院)", 
         generator.create_hospital(), 800),
        
        ("🏬 Shopping Mall (购物中心)", 
         generator.create_shopping_mall(), 3000),
        
        ("🌳 Urban Park (城市公园)", 
         generator.create_urban_park(), 1500),
    ]
    
    for idx, (name, env, peds) in enumerate(scenarios, 1):
        print(f"\n\n{'#'*70}")
        print(f" Scenario {idx}/5: {name}")
        print(f"{'#'*70}\n")
        
        demo = ScenarioDemonstration(name, env, peds)
        demo.run_simulation(max_time=60.0, visualize=True)
        
        if idx < len(scenarios):
            input(f"\nScenario {idx} completed. Press Enter to continue to next scenario...")
    
    print("\n" + "="*70)
    print(" ✅ All scenarios demonstrated successfully!")
    print("="*70)
    print("\nVisualization images saved to: exports/")
    print("You can now:")
    print("  1. Review the generated visualizations")
    print("  2. Run individual scenarios using the web interface")
    print("  3. Customize scenarios in examples/generate_preset_scenarios.py")


def demo_single_scenario(scenario_id):
    """演示单个场景"""
    generator = ScenarioGenerator()
    
    scenarios = {
        'downtown_street': ("🏙️ Downtown Street", 
                           generator.create_downtown_street(), 1000),
        'campus': ("🎓 Campus", 
                  generator.create_campus(), 2000),
        'hospital': ("🏥 Hospital", 
                    generator.create_hospital(), 800),
        'shopping_mall': ("🏬 Shopping Mall", 
                         generator.create_shopping_mall(), 3000),
        'urban_park': ("🌳 Urban Park", 
                      generator.create_urban_park(), 1500),
    }
    
    if scenario_id not in scenarios:
        print(f"❌ Unknown scenario: {scenario_id}")
        print(f"Available scenarios: {', '.join(scenarios.keys())}")
        return
    
    name, env, peds = scenarios[scenario_id]
    demo = ScenarioDemonstration(name, env, peds)
    demo.run_simulation(max_time=60.0, visualize=True)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        # 运行单个场景
        scenario_id = sys.argv[1]
        demo_single_scenario(scenario_id)
    else:
        # 运行所有场景演示
        demo_all_scenarios()
