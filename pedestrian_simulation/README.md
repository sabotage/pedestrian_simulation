# 行人运动模拟系统 🚶‍♂️🚶‍♀️

一个功能强大的行人运动仿真系统，基于**社会力模型（Social Force Model）**，支持Web可视化编辑、复杂场景模拟、突发事件处理，并可无缝导出至Unity VR应用。

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ 核心特性

### 1. 🎨 Web可视化编辑器
- **交互式地图设计**：通过鼠标绘制墙体、障碍物、出入口
- **实时参数调整**：动态设置行人数量、密度、速度等参数
- **场景保存/加载**：支持场景配置的保存和复用

### 2. 🧠 高级行人模型
- **社会力模型**：基于Helbing的经典模型，模拟真实行人行为
- **多状态系统**：正常、恐慌、疏散等多种状态
- **智能导航**：自动寻路、避障、目标跟踪

### 3. ⚡ 突发事件模拟
支持多种突发事件：
- 🔥 **火灾**：触发恐慌反应和疏散行为
- 🔫 **枪击事件**：模拟极端应急场景
- 🚪 **出入口动态开闭**：测试疏散路线变化
- 🚧 **动态障碍物**：模拟通道堵塞等情况

### 4. 📊 数据分析与可视化
- 实时统计信息（人数、速度、密度等）
- 密度热力图
- 行人轨迹可视化
- 疏散时间分析
- 高质量动画导出

### 5. 🎮 Unity VR集成
- 完整的Unity C#加载脚本
- 支持3D场景重现
- VR沉浸式体验
- 实时回放控制

## 🏗️ 系统架构

```
pedestrian_simulation/
├── core/                      # 核心仿真引擎
│   └── pedestrian_model.py    # 社会力模型实现
├── server/                    # Web服务器
│   ├── app.py                 # Flask API服务
│   └── templates/
│       └── editor.html        # Web编辑器界面
├── visualization/             # 可视化模块
│   └── visualizer.py          # Matplotlib动画生成
├── unity_integration/         # Unity集成
│   └── SimulationDataLoader.cs # Unity数据加载脚本
├── scenarios/                 # 保存的场景
├── exports/                   # 导出的数据
└── requirements.txt           # Python依赖
```

## 📦 安装指南

### 系统要求
- Python 3.8+
- 现代浏览器（Chrome/Firefox/Edge推荐）
- Unity 2020.3+ (可选，用于VR展示)

### 安装步骤

1. **克隆/下载项目**
```bash
cd pedestrian_simulation
```

2. **安装Python依赖**
```bash
pip install -r requirements.txt
```

3. **（可选）安装FFmpeg用于视频导出**
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg

# Windows: 从 https://ffmpeg.org/download.html 下载
```

## 🚀 快速开始

### 方式一：使用Web编辑器（推荐）

1. **启动Web服务器**
```bash
cd server
python app.py
```

2. **打开浏览器**
访问：`http://localhost:5000`

3. **创建场景**
   - 选择"墙体"模式，绘制房间边界（双击完成绘制）
   - 选择"出口"模式，点击位置添加出入口
   - 选择"生成区"模式，绘制行人生成区域
   - 设置行人数量等参数

4. **运行仿真**
   - 点击"开始仿真"按钮
   - 观察行人运动
   - 可随时点击"触发事件"测试突发情况

5. **导出数据**
   - 点击"导出Unity"按钮
   - 下载JSON文件用于Unity

### 方式二：使用Python脚本

创建 `run_simulation.py`：

```python
import numpy as np
from core.pedestrian_model import SimulationEnvironment, EventType
from visualization.visualizer import SimulationVisualizer

# 创建环境
env = SimulationEnvironment(width=40, height=40)

# 添加墙体（房间边界）
room = np.array([[0, 0], [40, 0], [40, 40], [0, 40]])
env.add_obstacle(room)

# 添加内部障碍物
obstacle = np.array([[15, 15], [25, 15], [25, 25], [15, 25]])
env.add_obstacle(obstacle)

# 添加出口
env.add_exit(np.array([20, 0]), width=3.0)
env.add_exit(np.array([40, 20]), width=3.0)

# 生成100个行人
for _ in range(100):
    position = np.random.rand(2) * [40, 40]
    goal = env.exits[np.random.randint(len(env.exits))].position
    env.add_pedestrian(position, goal)

# 在10秒时触发火灾
def check_events():
    if env.time >= 10.0 and len(env.events) == 0:
        env.trigger_event(
            event_type=EventType.FIRE,
            position=np.array([20, 20]),
            radius=15.0,
            intensity=1.0
        )

# 运行仿真并可视化
visualizer = SimulationVisualizer(env)

# 方式1: 实时显示
visualizer.animate(duration=60.0)

# 方式2: 保存为视频
# visualizer.animate(duration=60.0, save_path='simulation.mp4')

# 导出Unity数据
env.export_for_unity('exports/simulation_data.json')
```

运行：
```bash
python run_simulation.py
```

## 🎮 Unity集成详细步骤

### 1. 准备Unity项目

1. 创建新的Unity 3D项目或使用现有VR项目
2. 创建空的GameObject命名为"SimulationManager"
3. 将 `SimulationDataLoader.cs` 脚本附加到该对象

### 2. 导入仿真数据

1. 从Python系统导出数据：
   - 使用Web界面的"导出Unity"按钮
   - 或使用Python代码：`env.export_for_unity('simulation_data.json')`

2. 将JSON文件导入Unity项目：
   - 拖放JSON文件到Unity的Assets文件夹
   - Unity会自动识别为TextAsset

### 3. 配置脚本

在Inspector中设置：
- **Simulation Data File**: 拖入JSON文件
- **Pedestrian Prefab**: （可选）自定义行人模型
- **Wall Material**: 墙体材质
- **Exit Marker Prefab**: （可选）出口标识模型

### 4. 自定义行人预制体（可选）

创建更真实的行人模型：

```csharp
// 简单的动画控制器
public class PedestrianAnimator : MonoBehaviour
{
    private Animator animator;
    
    void Start()
    {
        animator = GetComponent<Animator>();
    }
    
    public void SetWalkSpeed(float speed)
    {
        if (animator != null)
        {
            animator.SetFloat("Speed", speed);
        }
    }
}
```

### 5. VR相机设置

```csharp
// 添加到VR相机
public class SimulationController : MonoBehaviour
{
    private SimulationDataLoader loader;
    
    void Start()
    {
        loader = FindObjectOfType<SimulationDataLoader>();
    }
    
    void Update()
    {
        // 使用VR控制器按钮控制播放
        if (OVRInput.GetDown(OVRInput.Button.One))
        {
            loader.Play();
        }
        
        if (OVRInput.GetDown(OVRInput.Button.Two))
        {
            loader.Pause();
        }
    }
}
```

## 📊 API文档

### Web API端点

#### 1. 启动仿真
```http
POST /api/start_simulation
Content-Type: application/json

{
  "width": 50,
  "height": 50,
  "obstacles": [...],
  "exits": [...],
  "pedestrian_spawn": {
    "count": 100,
    "areas": [...]
  }
}
```

#### 2. 触发事件
```http
POST /api/trigger_event
Content-Type: application/json

{
  "event_type": "fire",
  "position": [25, 25],
  "radius": 10,
  "intensity": 1.0
}
```

#### 3. 获取实时状态
```http
GET /api/get_state

Response:
{
  "status": "success",
  "time": 15.3,
  "pedestrians": [...],
  "exits": [...],
  "statistics": {...}
}
```

#### 4. 导出Unity数据
```http
POST /api/export_unity

Returns: simulation_data.json file
```

### Python API

#### 基础使用

```python
from core.pedestrian_model import SimulationEnvironment, EventType

# 创建环境
env = SimulationEnvironment(width=50, height=50)

# 添加障碍物
vertices = np.array([[x1, y1], [x2, y2], ...])
env.add_obstacle(vertices)

# 添加出口
env.add_exit(position=np.array([x, y]), width=2.0)

# 添加行人
env.add_pedestrian(position=np.array([x, y]), goal=np.array([gx, gy]))

# 触发事件
env.trigger_event(EventType.FIRE, position=np.array([x, y]), radius=10.0)

# 执行仿真步骤
for _ in range(1000):
    env.step()

# 导出数据
env.export_for_unity('output.json')
```

## 🔬 社会力模型详解

本系统基于Helbing的社会力模型，行人受到以下力的作用：

### 1. 期望速度力
$$\vec{F}_i^{desired} = m_i \frac{\vec{v}_i^0 - \vec{v}_i}{\tau}$$

行人试图以期望速度向目标移动。

### 2. 行人间排斥力
$$\vec{F}_{ij} = A \exp\left(\frac{r_{ij} - d_{ij}}{B}\right) \vec{n}_{ij}$$

模拟个人空间和避碰行为。

### 3. 墙体排斥力
$$\vec{F}_{iW} = A_W \exp\left(\frac{r_i - d_{iW}}{B_W}\right) \vec{n}_{iW}$$

防止行人穿墙。

### 4. 身体接触力
当行人发生物理接触时：
$$\vec{F}_{ij}^{body} = k(r_{ij} - d_{ij})\vec{n}_{ij} + \kappa(r_{ij} - d_{ij})\Delta v_{ji}^t \vec{t}_{ij}$$

## 📈 应用场景

1. **建筑设计**
   - 评估疏散路线
   - 优化出入口位置
   - 测试人流承载能力

2. **应急管理**
   - 灾难疏散演练
   - 应急响应规划
   - 风险评估

3. **城市规划**
   - 公共空间设计
   - 人行道宽度规划
   - 交通枢纽优化

4. **教育培训**
   - VR安全培训
   - 行为学研究
   - 仿真教学

5. **活动管理**
   - 大型活动人流控制
   - 场馆容量测试
   - 安保规划

## 🛠️ 高级配置

### 自定义行人参数

```python
from core.pedestrian_model import Pedestrian

# 创建自定义行人
ped = Pedestrian(
    id=0,
    position=np.array([10, 10]),
    velocity=np.zeros(2),
    goal=np.array([40, 40]),
    radius=0.3,           # 半径
    mass=70.0,            # 质量
    desired_speed=1.34,   # 期望速度
    max_speed=2.0         # 最大速度
)
```

### 调整模型参数

```python
# 修改社会力模型参数
env.model.A = 2000      # 排斥力强度
env.model.B = 0.08      # 排斥力范围
env.model.tau = 0.5     # 放松时间
```

### 批量场景测试

```python
def run_batch_simulation(scenarios):
    results = []
    for scenario in scenarios:
        env = create_environment(scenario)
        env = run_simulation(env, duration=60)
        results.append(analyze_results(env))
    return results
```

## 🐛 故障排除

### 常见问题

**Q: Web界面无法连接**
```bash
# 检查端口是否被占用
lsof -i :5000

# 更改端口
python app.py --port 8080
```

**Q: 行人行为异常**
- 检查墙体是否闭合
- 确认出口位置可达
- 调整社会力模型参数

**Q: Unity加载失败**
- 确认JSON格式正确
- 检查Unity Console错误信息
- 验证数据路径

**Q: 动画生成失败**
```bash
# 安装FFmpeg
pip install ffmpeg-python
```

## 📚 参考文献

1. Helbing, D., & Molnár, P. (1995). Social force model for pedestrian dynamics. Physical Review E, 51(5), 4282.

2. Helbing, D., Farkas, I., & Vicsek, T. (2000). Simulating dynamical features of escape panic. Nature, 407(6803), 487-490.

3. Moussaïd, M., Helbing, D., & Theraulaz, G. (2011). How simple rules determine pedestrian behavior and crowd disasters. Proceedings of the National Academy of Sciences, 108(17), 6884-6888.

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 👥 作者

- 初始开发：Claude & User
- 维护者：[Your Name]

## 🙏 致谢

- 感谢Dirk Helbing教授的开创性工作
- 感谢开源社区的支持

## 📞 联系方式

- 项目主页：[GitHub Repository]
- 问题反馈：[Issues]
- 邮箱：your.email@example.com

---

⭐ 如果这个项目对你有帮助，请给个Star！
