# 快速参考 - 命令速查表

## 🚀 快速开始

### 初始化项目
```bash
python init_project.py
```

### 安装依赖
```bash
pip install -r requirements.txt
```

### 启动方式

#### 方式1: 交互式菜单（推荐）
```bash
python start.py
```

#### 方式2: 直接启动Web服务器
```bash
python start.py --web
# 或
cd server && python app.py
```

#### 方式3: 运行示例
```bash
python start.py --example 1  # 基础疏散
python start.py --example 2  # 火灾应急
```

## 💻 Python API速查

### 创建仿真环境
```python
from core.pedestrian_model import SimulationEnvironment

env = SimulationEnvironment(width=50, height=50)
```

### 添加障碍物
```python
import numpy as np

# 矩形房间
walls = np.array([[0,0], [50,0], [50,50], [0,50]])
env.add_obstacle(walls)
```

### 添加出口
```python
env.add_exit(position=np.array([25, 0]), width=3.0)
```

### 添加行人
```python
position = np.array([10, 10])
goal = np.array([25, 0])
env.add_pedestrian(position, goal)
```

### 触发事件
```python
from core.pedestrian_model import EventType

# 火灾
env.trigger_event(
    EventType.FIRE, 
    position=np.array([25, 25]),
    radius=10.0
)

# 关闭出口
env.trigger_event(
    EventType.ENTRANCE_CLOSE,
    position=np.array([25, 0])
)
```

### 运行仿真
```python
# 方式1: 逐步执行
for _ in range(1000):
    env.step()

# 方式2: 可视化
from visualization.visualizer import SimulationVisualizer

viz = SimulationVisualizer(env)
viz.animate(duration=60.0)
```

### 导出数据
```python
env.export_for_unity('output.json')
```

## 🌐 Web API速查

### 启动仿真
```http
POST http://localhost:5000/api/start_simulation
Content-Type: application/json

{
  "width": 50,
  "height": 50,
  "obstacles": [...],
  "exits": [...],
  "pedestrian_spawn": {
    "count": 100
  }
}
```

### 获取状态
```http
GET http://localhost:5000/api/get_state
```

### 触发事件
```http
POST http://localhost:5000/api/trigger_event
Content-Type: application/json

{
  "event_type": "fire",
  "position": [25, 25],
  "radius": 10,
  "intensity": 1.0
}
```

### 控制仿真
```http
POST http://localhost:5000/api/pause_simulation
POST http://localhost:5000/api/resume_simulation
POST http://localhost:5000/api/stop_simulation
```

### 导出Unity数据
```http
POST http://localhost:5000/api/export_unity
```

## 🎮 Unity集成速查

### 1. 导出数据（Python）
```python
env.export_for_unity('simulation_data.json')
```

### 2. Unity中加载（C#）
```csharp
// 附加到GameObject
SimulationDataLoader loader = gameObject.AddComponent<SimulationDataLoader>();
loader.simulationDataFile = jsonFile;  // 拖入TextAsset

// 控制播放
loader.Play();
loader.Pause();
loader.Stop();
loader.SetPlaybackSpeed(2.0f);
```

### 3. VR控制器（Oculus）
```csharp
// A键 - 播放/暂停
if (OVRInput.GetDown(OVRInput.Button.One))
{
    loader.Play();
}

// B键 - 重启
if (OVRInput.GetDown(OVRInput.Button.Two))
{
    loader.Restart();
}
```

## 📊 可视化速查

### 生成动画
```python
from visualization.visualizer import SimulationVisualizer

viz = SimulationVisualizer(env)
viz.animate(duration=60.0)

# 保存为视频
viz.animate(duration=60.0, save_path='output.mp4')
```

### 生成分析图表
```python
from visualization.visualizer import AnalysisPlotter

# 密度热力图
fig = AnalysisPlotter.plot_density_heatmap(env)
fig.savefig('heatmap.png')

# 疏散曲线
fig = AnalysisPlotter.plot_evacuation_time_distribution(env)
fig.savefig('evacuation.png')

# 速度分布
fig = AnalysisPlotter.plot_speed_distribution(env)
fig.savefig('speed.png')
```

## ⚙️ 参数调优速查

### 社会力模型参数
```python
env.model.A = 2000        # 排斥力强度 (1000-3000)
env.model.B = 0.08        # 排斥力范围 (0.05-0.15)
env.model.tau = 0.5       # 放松时间 (0.3-1.0)
env.model.k = 1.2e5       # 接触力系数
env.model.kappa = 2.4e5   # 摩擦力系数
```

### 行人参数
```python
ped.radius = 0.3          # 半径 (0.2-0.4米)
ped.mass = 70.0           # 质量 (50-100kg)
ped.desired_speed = 1.34  # 期望速度 (1.0-1.5 m/s)
ped.max_speed = 2.0       # 最大速度 (1.5-2.5 m/s)
```

## 🐛 常见问题速查

### Web服务器端口被占用
```bash
python start.py --port 8080
```

### 依赖安装失败
```bash
pip install --upgrade pip
pip install -r requirements.txt --user
```

### JSON导出失败
```python
# 确保目录存在
from pathlib import Path
Path('exports').mkdir(exist_ok=True)
env.export_for_unity('exports/data.json')
```

### Unity加载失败
- 检查JSON格式（使用在线验证器）
- 确认文件编码为UTF-8
- 检查Unity Console错误信息

### 性能问题
```python
# 减少行人数量
env = SimulationEnvironment(width=30, height=30)
for _ in range(50):  # 而不是500
    env.add_pedestrian(...)

# 增加时间步长
env.model.dt = 0.2  # 而不是0.1
```

## 📁 目录速查

```
pedestrian_simulation/
├── core/                    # 核心引擎
├── server/                  # Web服务
├── visualization/           # 可视化
├── unity_integration/       # Unity集成
├── examples/               # 示例代码
├── scenarios/              # 场景配置
└── exports/                # 导出数据
```

## 🔗 文档链接

- **主文档**: README.md
- **项目总览**: PROJECT_OVERVIEW.md
- **Unity集成**: unity_integration/UNITY_INTEGRATION_GUIDE.md
- **示例代码**: examples/

## 📞 获取帮助

```bash
python start.py --help
```

---

**提示**: 将此文件保存为书签，方便快速查阅！
