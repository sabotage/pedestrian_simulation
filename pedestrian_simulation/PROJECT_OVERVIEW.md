# 项目总览 - 行人运动模拟系统

## 📁 完整目录结构

```
pedestrian_simulation/
│
├── README.md                          # 项目主文档
├── requirements.txt                   # Python依赖
├── start.py                          # 快速启动脚本
├── init_project.py                   # 项目初始化
│
├── core/                             # 核心模拟引擎
│   └── pedestrian_model.py           # 社会力模型实现
│       ├── Pedestrian类              # 行人对象
│       ├── SocialForceModel类        # 社会力计算
│       └── SimulationEnvironment类   # 仿真环境
│
├── server/                           # Web服务
│   ├── app.py                        # Flask API服务器
│   └── templates/
│       └── editor.html               # Web编辑器界面
│
├── visualization/                    # 可视化模块
│   └── visualizer.py                 # Matplotlib动画生成
│       ├── SimulationVisualizer      # 实时动画
│       └── AnalysisPlotter           # 数据分析图表
│
├── unity_integration/                # Unity VR集成
│   ├── SimulationDataLoader.cs       # 数据加载脚本
│   ├── SimulationUIController.cs     # UI控制脚本
│   └── UNITY_INTEGRATION_GUIDE.md    # Unity集成指南
│
├── examples/                         # 示例代码
│   ├── example_1_basic_evacuation.py # 基础疏散示例
│   └── example_2_fire_emergency.py   # 火灾应急示例
│
├── scenarios/                        # 保存的场景配置
├── exports/                          # 导出的数据文件
├── data/                            # 临时数据
└── logs/                            # 日志文件
```

## 🔄 系统工作流程

```
1. 场景设计
   ↓
   [Web编辑器] 或 [Python脚本]
   ↓
2. 仿真运行
   ↓
   [社会力模型计算]
   ↓
3. 数据收集
   ↓
   [实时状态 + 历史轨迹]
   ↓
4. 可视化/导出
   ↓
   [Python动画] 或 [Unity 3D/VR]
```

## 🎯 核心组件说明

### 1. 核心模拟引擎 (core/)

**pedestrian_model.py**

#### Pedestrian类
```python
- 属性:
  * position: 位置 [x, y]
  * velocity: 速度向量
  * goal: 目标位置
  * state: 状态 (正常/恐慌/疏散)
  * panic_level: 恐慌程度 (0-1)
  
- 方法:
  * update_goal(): 更新目标
  * set_panic(): 设置恐慌状态
```

#### SocialForceModel类
```python
- 参数:
  * A, B: 排斥力参数
  * k, kappa: 接触力参数
  * tau: 放松时间
  
- 核心方法:
  * desired_force(): 期望速度力
  * pedestrian_repulsion(): 行人间排斥
  * wall_repulsion(): 墙体排斥
  * compute_total_force(): 总力计算
```

#### SimulationEnvironment类
```python
- 管理:
  * pedestrians: 行人列表
  * obstacles: 障碍物列表
  * exits: 出口列表
  * events: 事件列表
  
- 核心功能:
  * step(): 执行一步仿真
  * trigger_event(): 触发突发事件
  * export_for_unity(): 导出Unity数据
```

### 2. Web服务器 (server/)

**app.py - Flask API**

#### 主要端点:

| 端点 | 方法 | 功能 |
|-----|------|------|
| `/` | GET | Web编辑器页面 |
| `/api/start_simulation` | POST | 启动仿真 |
| `/api/stop_simulation` | POST | 停止仿真 |
| `/api/trigger_event` | POST | 触发事件 |
| `/api/get_state` | GET | 获取实时状态 |
| `/api/export_unity` | POST | 导出Unity数据 |

#### 请求示例:

```javascript
// 启动仿真
fetch('/api/start_simulation', {
  method: 'POST',
  body: JSON.stringify({
    width: 50,
    height: 50,
    obstacles: [...],
    exits: [...],
    pedestrian_spawn: {...}
  })
})

// 触发火灾
fetch('/api/trigger_event', {
  method: 'POST',
  body: JSON.stringify({
    event_type: 'fire',
    position: [25, 25],
    radius: 10,
    intensity: 1.0
  })
})
```

### 3. 可视化系统 (visualization/)

**visualizer.py**

#### SimulationVisualizer
- 实时2D动画
- Matplotlib绘图
- 支持保存视频

#### AnalysisPlotter
- 密度热力图
- 轨迹路径图
- 疏散时间分析
- 速度分布统计

### 4. Unity集成 (unity_integration/)

#### 数据流:

```
Python仿真 → JSON导出 → Unity加载 → 3D渲染
```

#### 关键脚本:

1. **SimulationDataLoader.cs**
   - 加载JSON数据
   - 创建3D场景
   - 控制回放

2. **SimulationUIController.cs**
   - UI控制面板
   - VR交互

3. **数据格式**:
```json
{
  "metadata": {
    "width": 50,
    "height": 50,
    "total_time": 120,
    "dt": 0.1
  },
  "frames": [
    {
      "time": 0.0,
      "pedestrians": [
        {
          "id": 0,
          "position": [10, 20],
          "velocity": [1.2, 0.5],
          "state": "normal",
          "panic_level": 0.0
        }
      ]
    }
  ]
}
```

## 🔧 技术栈

### Python后端
- **NumPy**: 数值计算
- **Matplotlib**: 数据可视化
- **Flask**: Web服务器
- **SciPy**: 科学计算（可选）

### Web前端
- **HTML5 Canvas**: 2D绘图
- **Vanilla JavaScript**: 交互逻辑
- **CSS3**: 界面样式

### Unity
- **C#**: 脚本语言
- **XR Toolkit**: VR支持
- **URP**: 渲染管线

## 📊 数据流详解

### 1. 仿真数据

```python
# 每帧数据结构
frame = {
    'time': 10.5,  # 当前时间
    'pedestrians': [
        {
            'id': 0,
            'position': [x, y],
            'velocity': [vx, vy],
            'state': 'panic',
            'panic_level': 0.8
        }
    ]
}
```

### 2. 场景配置

```json
{
  "name": "商场疏散",
  "width": 100,
  "height": 80,
  "obstacles": [
    {
      "vertices": [[0,0], [100,0], [100,80], [0,80]]
    }
  ],
  "exits": [
    {
      "position": [50, 0],
      "width": 5.0,
      "is_open": true
    }
  ],
  "pedestrian_spawn": {
    "count": 200,
    "density_mode": "uniform",
    "areas": [...]
  }
}
```

## 🎮 使用场景

### 1. 建筑设计验证
```python
# 测试不同出口配置
configs = [
    {'exits': 2, 'width': 2.0},
    {'exits': 3, 'width': 2.5},
    {'exits': 4, 'width': 2.0}
]

for config in configs:
    env = create_environment(config)
    results = run_simulation(env)
    analyze_evacuation_time(results)
```

### 2. 应急演练
```python
# 模拟火灾场景
env = create_building()
env.add_pedestrians(300)

# 10秒后触发火灾
at_time(10, lambda: env.trigger_event(
    EventType.FIRE,
    position=[x, y],
    radius=15
))

# 20秒后关闭主出口
at_time(20, lambda: env.close_exit(main_exit))
```

### 3. VR培训
```
1. 加载真实建筑模型
2. 导入仿真数据
3. 沉浸式观察疏散过程
4. 识别潜在问题
```

## 🔬 社会力模型参数调优

### 基本参数
```python
model.A = 2000      # 排斥力强度 (推荐: 2000-3000)
model.B = 0.08      # 排斥力范围 (推荐: 0.08-0.15)
model.tau = 0.5     # 放松时间 (推荐: 0.5-1.0)
```

### 不同场景推荐值

| 场景 | A值 | B值 | tau值 | 说明 |
|-----|-----|-----|-------|------|
| 正常通行 | 2000 | 0.08 | 0.5 | 舒适环境 |
| 拥挤场所 | 2500 | 0.10 | 0.4 | 商场、车站 |
| 应急疏散 | 3000 | 0.12 | 0.3 | 火灾、地震 |
| 体育场馆 | 2200 | 0.09 | 0.5 | 大型活动 |

## 📈 性能指标

### 仿真性能
- 100行人: ~10ms/步
- 500行人: ~100ms/步  
- 1000行人: ~400ms/步

### Unity渲染
- 100行人: 60+ FPS
- 500行人: 45+ FPS
- 1000行人: 30+ FPS (需优化)

### 优化建议
1. 使用空间分区加速邻近搜索
2. GPU并行计算（Numba/CUDA）
3. Unity对象池和LOD
4. 减少轨迹点数量

## 🛠️ 扩展开发指南

### 添加新的事件类型

```python
# 1. 定义事件类型
class EventType(Enum):
    FIRE = "fire"
    YOUR_NEW_EVENT = "your_event"

# 2. 实现事件处理
def _handle_your_event(self, event: Event):
    for ped in self.pedestrians:
        # 事件逻辑
        pass

# 3. 在trigger_event中添加分支
elif event_type == EventType.YOUR_NEW_EVENT:
    self._handle_your_event(event)
```

### 自定义行人行为

```python
class CustomPedestrian(Pedestrian):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.custom_property = 0
    
    def custom_behavior(self):
        # 自定义行为逻辑
        pass
```

### 添加新的分析图表

```python
class AnalysisPlotter:
    @staticmethod
    def plot_your_analysis(simulation):
        fig, ax = plt.subplots()
        # 绘图逻辑
        return fig
```

## 📚 参考资料

### 学术论文
1. Helbing & Molnár (1995) - Social Force Model原始论文
2. Helbing et al. (2000) - 逃生恐慌动力学
3. Moussaïd et al. (2011) - 人群灾难的简单规则

### 在线资源
- Matplotlib动画教程
- Flask RESTful API设计
- Unity VR开发文档
- 行人仿真综述

## 🤝 贡献代码

### 开发流程
1. Fork项目
2. 创建功能分支
3. 编写代码和测试
4. 提交Pull Request

### 代码规范
- 遵循PEP 8
- 添加文档字符串
- 编写单元测试
- 更新README

## 📞 支持与反馈

- GitHub Issues: 报告bug
- Discussions: 功能讨论
- Email: 技术支持

## 📄 许可证

MIT License - 自由使用和修改

---

**祝使用愉快! 🎉**
