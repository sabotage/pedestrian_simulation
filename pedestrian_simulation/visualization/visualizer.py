"""
Visualization Module - Generate high-quality animations and analysis charts using Matplotlib
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Polygon, Rectangle
import numpy as np
from typing import List
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from core.pedestrian_model import SimulationEnvironment, Pedestrian, PedestrianState

class SimulationVisualizer:
    """Simulation Visualizer"""
    
    def __init__(self, simulation: SimulationEnvironment):
        self.simulation = simulation
        self.fig, self.ax = plt.subplots(figsize=(12, 10))
        self.fig.patch.set_facecolor('#1a1a2e')
        self.ax.set_facecolor('#0f3460')
        
        # Set coordinate axes
        self.ax.set_xlim(0, simulation.width)
        self.ax.set_ylim(0, simulation.height)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3, color='white')
        
        # Title and labels
        self.ax.set_xlabel('X (meters)', fontsize=12, color='white')
        self.ax.set_ylabel('Y (meters)', fontsize=12, color='white')
        self.ax.tick_params(colors='white')
        
        # Store drawing objects
        self.pedestrian_circles = []
        self.pedestrian_arrows = []
        self.time_text = None
        self.stats_text = None
        
        self._setup_static_elements()
    
    def _setup_static_elements(self):
        """Setup static elements (walls, exits, etc.)"""
        # Draw walls
        for obstacle in self.simulation.obstacles:
            poly = Polygon(
                obstacle.vertices,
                closed=True,
                facecolor='#333333',
                edgecolor='#666666',
                linewidth=3,
                alpha=0.8
            )
            self.ax.add_patch(poly)
        
        # Draw exits
        for exit in self.simulation.exits:
            color = '#00d4aa' if exit.is_open else '#ff6b6b'
            rect = Rectangle(
                (exit.position[0] - exit.width/2, exit.position[1] - 0.3),
                exit.width,
                0.6,
                facecolor=color,
                edgecolor='white',
                linewidth=2,
                alpha=0.9
            )
            self.ax.add_patch(rect)
            self.ax.text(
                exit.position[0],
                exit.position[1] + 1,
                'EXIT' if exit.is_open else 'CLOSED',
                ha='center',
                fontsize=10,
                color='white',
                weight='bold'
            )
        
        # Add time and statistics text
        self.time_text = self.ax.text(
            0.02, 0.98,
            '',
            transform=self.ax.transAxes,
            fontsize=14,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.8),
            color='white',
            weight='bold'
        )
        
        self.stats_text = self.ax.text(
            0.02, 0.88,
            '',
            transform=self.ax.transAxes,
            fontsize=10,
            verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='black', alpha=0.8),
            color='white'
        )
    
    def update_frame(self, frame_num):
        """Update animation frame"""
        # Clear previous pedestrians
        for circle in self.pedestrian_circles:
            circle.remove()
        for arrow in self.pedestrian_arrows:
            arrow.remove()
        
        self.pedestrian_circles = []
        self.pedestrian_arrows = []
        
        # Execute simulation step
        if len(self.simulation.pedestrians) > 0:
            self.simulation.step()
        
        # Draw pedestrians
        for ped in self.simulation.pedestrians:
            # Choose color based on state
            if ped.state == PedestrianState.PANIC:
                color = '#ff6b6b'
                alpha = 0.9
            elif ped.state == PedestrianState.EVACUATING:
                color = '#ffa500'
                alpha = 0.8
            else:
                color = '#4CAF50'
                alpha = 0.7
            
            # Draw pedestrian circles
            circle = Circle(
                ped.position,
                ped.radius,
                facecolor=color,
                edgecolor='white',
                linewidth=1,
                alpha=alpha
            )
            self.ax.add_patch(circle)
            self.pedestrian_circles.append(circle)
            
            # Draw velocity direction arrows
            vel_magnitude = np.linalg.norm(ped.velocity)
            if vel_magnitude > 0.1:
                arrow = self.ax.arrow(
                    ped.position[0],
                    ped.position[1],
                    ped.velocity[0] * 0.5,
                    ped.velocity[1] * 0.5,
                    head_width=0.3,
                    head_length=0.2,
                    fc=color,
                    ec=color,
                    alpha=0.6,
                    width=0.05
                )
                self.pedestrian_arrows.append(arrow)
        
        # Update text information
        stats = self.simulation.get_statistics()
        self.time_text.set_text(f'Time: {self.simulation.time:.1f}s')
        self.stats_text.set_text(
            f'Pedestrian count: {stats["current_pedestrians"]}\n'
            f'Panic count: {stats["panic_count"]}\n'
            f'Average speed: {stats["average_speed"]:.2f} m/s'
        )
        
        return self.pedestrian_circles + self.pedestrian_arrows + [self.time_text, self.stats_text]
    
    def animate(self, duration: float = 60.0, fps: int = 30, save_path: str = None):
        """
        Create animation
        
        Args:
            duration: 动画时长(seconds)
            fps: 帧率
            save_path: 保存路径(None则直接显示)
        """
        frames = int(duration / self.simulation.model.dt)
        
        anim = animation.FuncAnimation(
            self.fig,
            self.update_frame,
            frames=frames,
            interval=self.simulation.model.dt * 1000,
            blit=True,
            repeat=False
        )
        
        if save_path:
            print(f"Saving animation to {save_path}...")
            writer = animation.FFMpegWriter(fps=fps, bitrate=2000)
            anim.save(save_path, writer=writer)
            print("Animation saved!")
        else:
            plt.show()
        
        return anim
    
    def save_snapshot(self, filename: str):
        """Save current frame screenshot"""
        plt.savefig(filename, dpi=150, bbox_inches='tight', facecolor=self.fig.get_facecolor())
        print(f"Screenshot saved to: {filename}")

class AnalysisPlotter:
    """Analysis Plotter"""
    
    @staticmethod
    def plot_density_heatmap(simulation: SimulationEnvironment, grid_size: int = 50):
        """Draw pedestriansDensity Heatmap"""
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create density grid
        density = np.zeros((grid_size, grid_size))
        
        for ped in simulation.pedestrians:
            x_idx = int(ped.position[0] / simulation.width * grid_size)
            y_idx = int(ped.position[1] / simulation.height * grid_size)
            
            if 0 <= x_idx < grid_size and 0 <= y_idx < grid_size:
                density[y_idx, x_idx] += 1
        
        # Draw heatmap
        im = ax.imshow(
            density,
            cmap='hot',
            origin='lower',
            extent=[0, simulation.width, 0, simulation.height],
            interpolation='gaussian'
        )
        
        plt.colorbar(im, ax=ax, label='Pedestrian density')
        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.set_title('行人Density Heatmap')
        
        return fig
    
    @staticmethod
    def plot_trajectory_paths(simulation: SimulationEnvironment, sample_count: int = 20):
        """Draw pedestrians轨迹"""
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # 绘制Obstacles
        for obstacle in simulation.obstacles:
            poly = Polygon(obstacle.vertices, closed=True, 
                         facecolor='gray', alpha=0.3)
            ax.add_patch(poly)
        
        # Randomly select pedestrians to draw paths
        sampled_peds = simulation.pedestrians[:sample_count] if len(simulation.pedestrians) > sample_count else simulation.pedestrians
        
        colors = plt.cm.rainbow(np.linspace(0, 1, len(sampled_peds)))
        
        for ped, color in zip(sampled_peds, colors):
            if len(ped.path) > 1:
                path = np.array(ped.path)
                ax.plot(path[:, 0], path[:, 1], color=color, alpha=0.6, linewidth=2)
                ax.scatter(path[0, 0], path[0, 1], color=color, s=100, marker='o', label=f'Ped {ped.id} 起点')
                ax.scatter(path[-1, 0], path[-1, 1], color=color, s=100, marker='s')
        
        ax.set_xlim(0, simulation.width)
        ax.set_ylim(0, simulation.height)
        ax.set_xlabel('X (meters)')
        ax.set_ylabel('Y (meters)')
        ax.set_title('行人Movement trajectory')
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @staticmethod
    def plot_evacuation_time_distribution(simulation: SimulationEnvironment):
        """绘制Evacuation time distribution"""
        # 这需要记录每个行人的疏散Time
        # 简化版本：显示当前仍在场景中的Pedestrian count量随Time变化
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # Extract from history data
        times = [frame['time'] for frame in simulation.history]
        counts = [len(frame['pedestrians']) for frame in simulation.history]
        
        ax.plot(times, counts, linewidth=2, color='#e94560')
        ax.fill_between(times, counts, alpha=0.3, color='#e94560')
        
        ax.set_xlabel('Time (seconds)', fontsize=12)
        ax.set_ylabel('场景中的Pedestrian count', fontsize=12)
        ax.set_title('行人Evacuation curve', fontsize=14)
        ax.grid(True, alpha=0.3)
        
        return fig
    
    @staticmethod
    def plot_speed_distribution(simulation: SimulationEnvironment):
        """绘制Speed distribution直方图"""
        fig, ax = plt.subplots(figsize=(10, 6))
        
        speeds = [np.linalg.norm(ped.velocity) for ped in simulation.pedestrians]
        
        ax.hist(speeds, bins=30, color='#00d4aa', alpha=0.7, edgecolor='black')
        ax.axvline(np.mean(speeds), color='#e94560', linestyle='--', 
                  linewidth=2, label=f'Average speed: {np.mean(speeds):.2f} m/s')
        
        ax.set_xlabel('速度 (m/s)', fontsize=12)
        ax.set_ylabel('Pedestrian count', fontsize=12)
        ax.set_title('行人Speed distribution', fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3, axis='y')
        
        return fig

def create_example_animation():
    """Create example animation"""
    # 创建Simulation Environment
    env = SimulationEnvironment(width=30, height=30)
    
    # 添加Walls - 创建一个房间
    room_walls = np.array([
        [0, 0], [30, 0], [30, 30], [0, 30]
    ])
    env.add_obstacle(room_walls)
    
    # 添加内部Obstacles
    obstacle1 = np.array([[10, 10], [15, 10], [15, 15], [10, 15]])
    env.add_obstacle(obstacle1)
    
    # 添加Exits
    env.add_exit(np.array([15, 0]), width=2.0)
    env.add_exit(np.array([30, 15]), width=2.0)
    
    # 添加行人
    for _ in range(80):
        position = np.random.rand(2) * [30, 30]
        goal = env.exits[np.random.randint(len(env.exits))].position
        env.add_pedestrian(position, goal)
    
    # 创建可视化器
    visualizer = SimulationVisualizer(env)
    
    # 在10seconds时触发Fire事件
    def trigger_fire_at_time():
        if env.time >= 10.0 and len(env.events) == 0:
            env.trigger_event(
                event_type=EventType.FIRE,
                position=np.array([15, 15]),
                radius=10.0,
                intensity=1.0
            )
    
    # 运行动画
    visualizer.animate(duration=30.0, fps=30)

if __name__ == '__main__':
    create_example_animation()
