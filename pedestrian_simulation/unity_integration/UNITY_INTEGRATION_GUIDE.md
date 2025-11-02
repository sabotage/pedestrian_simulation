# Unity VR集成指南

## 📋 概述

本指南将详细说明如何将Python行人仿真系统的数据导入Unity，并在VR环境中展示。

## 🎯 最终效果

- ✅ 3D可视化行人运动
- ✅ VR沉浸式体验
- ✅ 实时回放控制
- ✅ 轨迹追踪显示
- ✅ 多视角观察

## 📦 准备工作

### 1. Unity版本要求
- Unity 2020.3 LTS 或更新版本
- Universal Render Pipeline (URP) - 推荐
- XR Plugin Management (VR支持)

### 2. 必需的Unity包
通过Package Manager安装：
- TextMeshPro (UI文本)
- XR Interaction Toolkit (VR交互)
- Oculus XR Plugin / OpenXR Plugin (取决于你的VR设备)

## 🛠️ 集成步骤

### 步骤1: 创建Unity项目

1. 打开Unity Hub
2. 创建新的3D项目
3. 项目名称：`PedestrianSimulationVR`
4. 选择合适的模板（3D或VR）

### 步骤2: 配置VR设置

```
Edit → Project Settings → XR Plug-in Management
- 勾选你的VR设备对应的插件
  例如: Oculus, OpenVR, Windows Mixed Reality等
```

### 步骤3: 导入脚本

将以下脚本复制到Unity项目的`Assets/Scripts`文件夹：

1. `SimulationDataLoader.cs` - 数据加载器
2. `SimulationUIController.cs` - UI控制器
3. `VRSimulationController.cs` - VR控制器（包含在UIController中）

### 步骤4: 导入仿真数据

1. 从Python系统导出JSON数据：
```python
# 在Python中
env.export_for_unity('simulation_data.json')
```

2. 将JSON文件拖入Unity的`Assets/Data`文件夹
   - Unity会自动识别为TextAsset

### 步骤5: 场景设置

#### 5.1 创建仿真管理器

1. 在Hierarchy中创建空GameObject: `SimulationManager`
2. 添加`SimulationDataLoader`脚本
3. 在Inspector中配置：

```
SimulationDataLoader组件:
├─ Simulation Data File: [拖入JSON文件]
├─ Pedestrian Prefab: [可选，自定义行人模型]
├─ Wall Material: [创建灰色材质]
├─ Exit Marker Prefab: [可选]
├─ Normal Color: 绿色 (0, 255, 0)
├─ Panic Color: 红色 (255, 0, 0)
├─ Evacuating Color: 黄色 (255, 255, 0)
├─ Playback Speed: 1.0
├─ Show Trajectories: ✓
└─ Scene Scale: 1.0
```

#### 5.2 创建VR相机设置

##### 选项A: 使用Oculus Integration

1. 从Asset Store下载Oculus Integration
2. 导入到项目
3. 使用OVRCameraRig预制体

##### 选项B: 使用Unity XR

```
Hierarchy右键 → XR → Room-Scale XR Rig
```

#### 5.3 添加控制UI（可选，桌面模式）

1. 创建Canvas (UI → Canvas)
2. Canvas设置：
   - Render Mode: Screen Space - Overlay
   - UI Scale Mode: Scale With Screen Size

3. 添加控制面板：

```
Canvas/
├─ ControlPanel (Panel)
│   ├─ PlayButton (Button)
│   ├─ PauseButton (Button)
│   ├─ StopButton (Button)
│   ├─ RestartButton (Button)
│   ├─ SpeedSlider (Slider)
│   └─ SpeedText (TextMeshPro)
└─ StatsPanel (Panel)
    ├─ TimeText (TextMeshPro)
    ├─ PedestrianCountText (TextMeshPro)
    └─ PanicCountText (TextMeshPro)
```

4. 在SimulationManager上添加`SimulationUIController`
5. 拖拽UI元素到对应的字段

### 步骤6: 创建行人预制体（可选）

#### 简单版本 - 使用胶囊体

系统默认会创建简单的胶囊体，无需额外设置。

#### 高级版本 - 使用3D角色模型

1. 创建/导入3D人物模型
2. 添加Animator组件
3. 创建简单的行走动画状态机：

```
Animator States:
- Idle (静止)
- Walk (行走)
- Run (跑步 - 恐慌时)

Parameters:
- Speed (Float) - 控制速度
```

4. 保存为预制体
5. 将预制体拖到SimulationDataLoader的`Pedestrian Prefab`字段

示例动画控制脚本：

```csharp
public class PedestrianAnimationController : MonoBehaviour
{
    private Animator animator;
    
    void Start()
    {
        animator = GetComponent<Animator>();
    }
    
    public void UpdateAnimation(float speed, bool isPanic)
    {
        animator.SetFloat("Speed", speed);
        animator.SetBool("IsPanic", isPanic);
    }
}
```

### 步骤7: 添加环境增强

#### 7.1 照明设置

```
Hierarchy → Light → Directional Light
- Intensity: 1
- Color: 浅白色
- Shadow Type: Soft Shadows

Window → Rendering → Lighting
- Skybox: Default-Skybox
- Ambient Color: 浅灰色
```

#### 7.2 添加地面

```
Hierarchy → 3D Object → Plane
- Scale: (5, 1, 5) 根据场景大小调整
- Material: 浅色地面材质
```

#### 7.3 添加网格辅助线（可选）

```csharp
public class GridRenderer : MonoBehaviour
{
    public int gridSize = 50;
    public float cellSize = 1.0f;
    public Color gridColor = Color.gray;
    
    void OnDrawGizmos()
    {
        Gizmos.color = gridColor;
        
        for (int x = 0; x <= gridSize; x++)
        {
            Gizmos.DrawLine(
                new Vector3(x * cellSize, 0, 0),
                new Vector3(x * cellSize, 0, gridSize * cellSize)
            );
        }
        
        for (int z = 0; z <= gridSize; z++)
        {
            Gizmos.DrawLine(
                new Vector3(0, 0, z * cellSize),
                new Vector3(gridSize * cellSize, 0, z * cellSize)
            );
        }
    }
}
```

## 🎮 VR交互设置

### 控制器映射

#### Oculus Quest/Rift

```
右手控制器:
- A按钮: 播放/暂停
- B按钮: 重新开始
- 摇杆上下: 调整播放速度

左手控制器:
- X按钮: 切换轨迹显示
- Y按钮: 切换视角
- 摇杆: 移动（桌面模式）
```

#### HTC Vive

```
右手控制器:
- 菜单按钮: 播放/暂停
- 触摸板点击: 重新开始
- 触摸板滑动: 调整速度
```

### VR交互脚本示例

```csharp
public class VRInteractionManager : MonoBehaviour
{
    public SimulationDataLoader dataLoader;
    public OVRInput.Controller controller = OVRInput.Controller.RTouch;
    
    void Update()
    {
        // A按钮 - 播放/暂停
        if (OVRInput.GetDown(OVRInput.Button.One, controller))
        {
            TogglePlayback();
        }
        
        // B按钮 - 重启
        if (OVRInput.GetDown(OVRInput.Button.Two, controller))
        {
            dataLoader.Restart();
        }
        
        // 摇杆控制速度
        Vector2 thumbstick = OVRInput.Get(OVRInput.Axis2D.PrimaryThumbstick, controller);
        if (Mathf.Abs(thumbstick.y) > 0.3f)
        {
            float speed = dataLoader.playbackSpeed;
            speed = Mathf.Clamp(speed + thumbstick.y * Time.deltaTime, 0.1f, 5.0f);
            dataLoader.SetPlaybackSpeed(speed);
        }
    }
    
    private bool isPlaying = false;
    
    void TogglePlayback()
    {
        if (isPlaying)
        {
            dataLoader.Pause();
        }
        else
        {
            dataLoader.Play();
        }
        isPlaying = !isPlaying;
    }
}
```

## 📊 添加数据可视化

### 实时热力图

```csharp
public class HeatmapVisualizer : MonoBehaviour
{
    public Texture2D heatmapTexture;
    public Material heatmapMaterial;
    private float[,] density;
    
    void UpdateHeatmap(List<Vector3> positions)
    {
        // 重置密度数组
        for (int x = 0; x < density.GetLength(0); x++)
        {
            for (int y = 0; y < density.GetLength(1); y++)
            {
                density[x, y] = 0;
            }
        }
        
        // 计算密度
        foreach (var pos in positions)
        {
            int x = (int)(pos.x / cellSize);
            int y = (int)(pos.z / cellSize);
            
            if (x >= 0 && x < gridSize && y >= 0 && y < gridSize)
            {
                density[x, y]++;
            }
        }
        
        // 更新纹理
        UpdateTexture();
    }
}
```

## 🎨 视觉效果增强

### 1. 添加粒子效果

在火灾事件位置添加粒子系统：

```
GameObject → Effects → Particle System
- Start Color: 橙红色渐变
- Start Size: 0.5
- Emission Rate: 100
- Shape: Cone
```

### 2. 后处理效果

```
Window → Package Manager → 安装 Post Processing
```

在相机上添加后处理：
- Bloom（辉光）
- Vignette（晕影）
- Color Grading（色彩分级）

### 3. 轨迹线效果

为轨迹添加发光材质：

```csharp
Material trailMaterial = new Material(Shader.Find("Unlit/Color"));
trailMaterial.EnableKeyword("_EMISSION");
trailMaterial.SetColor("_EmissionColor", color * 0.5f);
```

## 🔧 性能优化

### 1. LOD系统

为行人模型创建LOD组：

```
选中行人预制体 → Add Component → LOD Group

LOD 0 (近距离): 高模 - 100%到60%
LOD 1 (中距离): 中模 - 60%到30%
LOD 2 (远距离): 低模 - 30%到10%
Culled (裁剪): 10%以下
```

### 2. 对象池

```csharp
public class PedestrianPool : MonoBehaviour
{
    public GameObject pedestrianPrefab;
    private Queue<GameObject> pool = new Queue<GameObject>();
    
    public GameObject GetPedestrian()
    {
        if (pool.Count > 0)
        {
            GameObject ped = pool.Dequeue();
            ped.SetActive(true);
            return ped;
        }
        return Instantiate(pedestrianPrefab);
    }
    
    public void ReturnPedestrian(GameObject ped)
    {
        ped.SetActive(false);
        pool.Enqueue(ped);
    }
}
```

### 3. 批处理

- 使用相同材质的行人可以批处理
- 启用GPU Instancing
- 合并静态网格（墙体）

## 🐛 常见问题

### Q1: JSON加载失败

**问题**: "Could not parse JSON"

**解决**:
- 检查JSON文件格式是否正确
- 使用在线JSON验证器验证
- 确认文件编码为UTF-8

### Q2: 行人不显示

**检查清单**:
- [ ] SimulationDataLoader的Start()方法被调用
- [ ] JSON文件正确赋值
- [ ] Pedestrian Prefab或使用默认胶囊体
- [ ] 场景缩放设置正确

### Q3: VR控制器不响应

**解决**:
- 确认VR插件正确安装
- 检查Input System版本
- 测试OVRInput是否正常工作

### Q4: 性能问题

**优化建议**:
- 减少行人数量
- 使用对象池
- 降低轨迹线分辨率
- 使用LOD系统

## 📚 扩展功能

### 1. 多场景管理

```csharp
public class ScenarioManager : MonoBehaviour
{
    public List<TextAsset> scenarios;
    private int currentScenario = 0;
    
    public void LoadNextScenario()
    {
        currentScenario = (currentScenario + 1) % scenarios.Count;
        LoadScenario(scenarios[currentScenario]);
    }
    
    void LoadScenario(TextAsset data)
    {
        SimulationDataLoader loader = GetComponent<SimulationDataLoader>();
        loader.simulationDataFile = data;
        loader.Stop();
        loader.Play();
    }
}
```

### 2. 数据分析面板

创建实时图表显示：
- 行人数量变化曲线
- 平均速度统计
- 恐慌程度分布

### 3. 自定义事件触发

在VR中通过射线触发事件：

```csharp
public class VREventTrigger : MonoBehaviour
{
    public SimulationEnvironment env;
    
    void Update()
    {
        if (OVRInput.GetDown(OVRInput.Button.PrimaryIndexTrigger))
        {
            RaycastHit hit;
            if (Physics.Raycast(transform.position, transform.forward, out hit))
            {
                TriggerEventAt(hit.point);
            }
        }
    }
    
    void TriggerEventAt(Vector3 position)
    {
        // 触发事件的逻辑
    }
}
```

## ✅ 测试清单

部署前测试：

- [ ] 数据正确加载
- [ ] 行人显示正常
- [ ] 墙体/障碍物正确显示
- [ ] 出口标识清晰
- [ ] 播放控制功能正常
- [ ] 速度调节工作
- [ ] 轨迹显示正确
- [ ] VR控制器响应
- [ ] 性能稳定（60 FPS+）
- [ ] 多场景切换正常

## 📖 更多资源

- Unity官方文档: https://docs.unity3d.com
- Oculus开发文档: https://developer.oculus.com
- XR Interaction Toolkit: https://docs.unity3d.com/Packages/com.unity.xr.interaction.toolkit

## 🎓 学习建议

1. 先在桌面模式测试
2. 确保功能正常后再添加VR
3. 逐步添加复杂功能
4. 定期优化性能
5. 记录遇到的问题和解决方案

---

如有问题，请查看主README或联系开发团队！
