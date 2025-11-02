# 🎬 预置场景系统更新说明 / Preset Scenarios Update Notes

## 📅 更新日期 / Update Date
2024-10-30

## ✨ 新增功能 / New Features

### 1. 5个预置城市场景 / 5 Preset Urban Scenarios

已成功创建并集成5个完整的城市场景，每个场景都有详细的环境设计和推荐的突发事件配置：

#### 🏙️ 场景1：繁忙街道 (Downtown Street)
- **环境尺寸**: 100m × 40m
- **推荐行人数**: 1000 (范围: 500-1500)
- **结构特征**:
  - 双向马路 + 中央隔离带
  - 两侧人行道 (5-8米宽)
  - 人行横道 × 3
  - 地铁站出口 × 2 (高流量: 8 peds/sec)
  - 公交站 × 1
  - 商店入口 × 4
  - 障碍物: 12棵树木
- **预设事件**:
  - 15秒: 火灾 (公交站附近, 半径8m)
  - 可选: 交通信号异常、道路施工
- **文件**: `scenarios/downtown_street.json`

#### 🎓 场景2：大学校园 (Campus)
- **环境尺寸**: 120m × 100m
- **推荐行人数**: 2000 (范围: 500-3000)
- **结构特征**:
  - 十字主干道网络
  - 教学楼A/B × 2
  - 宿舍楼 × 1
  - 图书馆 × 1
  - 食堂 × 1
  - 校门 × 4 (正门流量最高: 10 peds/sec)
- **预设事件**:
  - 10秒: 火灾 (教学楼A, 半径15m)
  - 25秒: 正门封闭
- **文件**: `scenarios/campus.json`

#### 🏥 场景3：医院 (Hospital)
- **环境尺寸**: 90m × 80m
- **推荐行人数**: 800 (范围: 500-1000)
- **结构特征**:
  - 急诊楼、门诊楼、住院楼 × 3
  - 连接通道
  - 救护车专用通道
  - 急诊入口 (高优先级: 5 peds/sec)
  - 正门、住院部入口、后勤入口
- **预设事件**:
  - 12秒: 火灾 (门诊楼, 半径12m)
  - 20秒: 急救通道封闭
- **文件**: `scenarios/hospital.json`

#### 🏬 场景4：购物中心 (Shopping Mall)
- **环境尺寸**: 100m × 80m
- **推荐行人数**: 3000 (范围: 1000-5000)
- **结构特征**:
  - 中庭广场 (中央开放区)
  - 商铺 × 8 (围绕中庭)
  - 休息区 × 4
  - 主门 (最高流量: 15 peds/sec)
  - 停车场入口 × 2
  - 安全疏散出口 × 8
- **预设事件**:
  - 15秒: 大规模火灾 (中庭, 半径20m)
  - 25秒: 枪击/惊恐事件 (商铺区, 半径15m)
- **文件**: `scenarios/shopping_mall.json`

#### 🌳 场景5：城市公园 (Urban Park)
- **环境尺寸**: 100m × 100m
- **推荐行人数**: 1500 (范围: 500-2000)
- **结构特征**:
  - 中央湖泊 (不规则形状)
  - 树木 × 21 (散布)
  - 活动舞台 (聚集区)
  - 餐车区 × 3
  - 公园大门 × 5
- **预设事件**:
  - 20秒: 枪击事件 (湖泊附近, 半径25m - 大范围Panic)
- **文件**: `scenarios/urban_park.json`

---

## 🔧 技术实现 / Technical Implementation

### 新增文件 / New Files

1. **场景生成器** (`examples/generate_preset_scenarios.py`)
   - `ScenarioGenerator` 类
   - 5个静态方法，每个生成一个场景
   - `generate_all_scenarios()` 函数批量生成JSON文件
   - 自动创建场景索引 (`scenarios_index.json`)

2. **场景演示脚本** (`examples/demo_preset_scenarios.py`)
   - `ScenarioDemonstration` 类
   - 自动添加典型突发事件
   - 可视化输出 (PNG图像)
   - 支持单场景或全部场景演示

3. **测试脚本** (`tests/test_preset_scenarios.py`)
   - 验证场景文件完整性
   - 测试Web API加载
   - 测试Environment.from_dict()
   - 综合测试报告

4. **场景配置文件** (6个JSON文件)
   - `scenarios/downtown_street.json`
   - `scenarios/campus.json`
   - `scenarios/hospital.json`
   - `scenarios/shopping_mall.json`
   - `scenarios/urban_park.json`
   - `scenarios/scenarios_index.json`

5. **文档** (`PRESET_SCENARIOS.md`)
   - 详细的中英文双语文档
   - 每个场景的结构图 (ASCII)
   - 使用方法 (3种方式)
   - 性能建议
   - 常见应用场景

### 代码修改 / Code Changes

#### Web后端 (`src/web/app.py`)
```python
# 新增API端点
@app.route('/api/scenarios', methods=['GET'])
def get_scenarios():
    # 从scenarios/目录加载所有场景JSON文件
    # 返回场景字典供前端使用

# 新增Socket.IO事件处理
@socketio.on('load_scenario')
def handle_load_scenario(data):
    # 加载指定ID的场景
    # 使用Environment.from_dict()创建环境
    # 创建新的Simulator实例
```

#### Web前端 - HTML (`src/web/templates/index.html`)
```html
<!-- 新增预置场景选择器 -->
<div class="control-section">
    <h3>🎬 Preset Scenarios / 预置场景</h3>
    <select id="presetScenario" onchange="loadPresetScenario()">
        <option value="">-- Choose a Scenario --</option>
        <option value="downtown_street">🏙️ Downtown Street / 繁忙街道</option>
        <option value="campus">🎓 Campus / 大学校园</option>
        <option value="hospital">🏥 Hospital / 医院</option>
        <option value="shopping_mall">🏬 Shopping Mall / 购物中心</option>
        <option value="urban_park">🌳 Urban Park / 城市公园</option>
    </select>
    <div id="scenarioInfo" class="scenario-info">
        <!-- 动态显示场景描述和推荐行人数 -->
    </div>
</div>
```

#### Web前端 - JavaScript (`src/web/static/app.js`)
```javascript
// 新增全局变量
let scenariosData = {};

// 页面加载时获取场景数据
window.addEventListener('DOMContentLoaded', () => {
    fetch('/api/scenarios')
        .then(response => response.json())
        .then(data => {
            scenariosData = data;
        });
});

// 新增场景加载函数
function loadPresetScenario() {
    const scenarioId = select.value;
    const scenario = scenariosData[scenarioId];
    
    // 显示场景信息
    document.getElementById('scenarioDescription').textContent = scenario.description;
    document.getElementById('scenarioRecommendedPeds').textContent = scenario.recommended_pedestrians;
    
    // 加载环境
    environment = scenario.environment;
    scale = canvas.width / environment.width;
    
    // 通知服务器
    socket.emit('load_scenario', { scenario_id: scenarioId });
    drawEnvironment();
}
```

#### Web前端 - CSS (`src/web/static/style.css`)
```css
/* 新增场景信息样式 */
.scenario-info {
    background: #f0f8ff;
    border-left: 4px solid #667eea;
    padding: 12px;
    margin-top: 10px;
    border-radius: 5px;
}
```

---

## 📊 测试结果 / Test Results

### 自动化测试
```
✅ PASS - Scenario Files (场景文件验证)
   - 5个场景JSON文件完整性检查
   - 1个场景索引文件验证
   - 所有必需字段存在
   - 墙体、入口、出口数据正确

✅ PASS - Web API (Web API测试)
   - 成功加载5个场景
   - 数据格式正确
   - 双语信息完整

✅ PASS - Environment Loading (环境加载测试)
   - Environment.from_dict() 工作正常
   - Simulator创建成功
   - 行人生成和模拟运行正常
```

### 手动测试
- ✅ 场景生成脚本运行成功
- ✅ 演示脚本可视化输出正确
- ✅ Web界面场景选择器正常工作
- ✅ 场景加载后地图正确显示

---

## 📖 使用方法 / Usage Guide

### 方法1: Web界面 (最简单)
```bash
# 1. 启动服务器
python run.bat  # Windows
./run.sh        # Linux/Mac

# 2. 打开浏览器
http://localhost:5000

# 3. 选择场景
在 "🎬 Preset Scenarios" 下拉菜单中选择:
  - 🏙️ Downtown Street / 繁忙街道
  - 🎓 Campus / 大学校园
  - 🏥 Hospital / 医院
  - 🏬 Shopping Mall / 购物中心
  - 🌳 Urban Park / 城市公园

# 4. 开始模拟
点击 "▶️ Start" 按钮
```

### 方法2: 演示脚本
```bash
# 演示所有场景
python examples/demo_preset_scenarios.py

# 演示单个场景
python examples/demo_preset_scenarios.py downtown_street
python examples/demo_preset_scenarios.py campus
python examples/demo_preset_scenarios.py hospital
python examples/demo_preset_scenarios.py shopping_mall
python examples/demo_preset_scenarios.py urban_park
```

### 方法3: Python代码
```python
from examples.generate_preset_scenarios import ScenarioGenerator
from src.simulation.simulator import Simulator

# 创建场景
generator = ScenarioGenerator()
env = generator.create_downtown_street()

# 创建模拟器
sim = Simulator(env, dt=0.1)

# 生成行人
for _ in range(1000):
    sim.spawn_pedestrian()

# 运行模拟
for _ in range(600):  # 60秒
    sim.step()
```

---

## 📈 性能指标 / Performance Metrics

| 场景 | 地图尺寸 | 推荐行人数 | 墙体数 | 入口数 | 出口数 | 内存占用 | 推荐FPS |
|------|---------|-----------|-------|-------|-------|---------|--------|
| 🏙️ 繁忙街道 | 100×40m | 1000 | 75 | 7 | 4 | ~200MB | 30 |
| 🎓 大学校园 | 120×100m | 2000 | 32 | 9 | 4 | ~400MB | 20 |
| 🏥 医院 | 90×80m | 800 | 45 | 4 | 4 | ~150MB | 30 |
| 🏬 购物中心 | 100×80m | 3000 | 72 | 7 | 8 | ~600MB | 15 |
| 🌳 城市公园 | 100×100m | 1500 | 112 | 6 | 5 | ~300MB | 25 |

---

## 🎯 应用场景 / Application Scenarios

### 1. 城市规划 (Urban Planning)
- **适用场景**: 繁忙街道、城市公园
- **分析目标**: 人行道宽度、出入口设置、交通流量
- **关键指标**: 拥堵率、通行时间、瓶颈位置

### 2. 建筑设计 (Architecture Design)
- **适用场景**: 购物中心、医院
- **分析目标**: 出口布局、疏散路线、容量设计
- **关键指标**: 疏散时间、出口利用率、安全距离

### 3. 应急演练 (Emergency Drills)
- **适用场景**: 全部5个场景
- **分析目标**: 应急预案效果、疏散效率、救援路线
- **关键指标**: 完成时间、伤亡预测、路径优化

### 4. 科研教学 (Research & Education)
- **适用场景**: 大学校园、城市公园
- **分析目标**: 行人动力学、社会力模型、群体行为
- **关键指标**: 模型参数、行为模式、统计特征

---

## 📝 未来改进计划 / Future Improvements

### 短期 (Short-term)
- [ ] 添加更多场景变体 (机场、火车站等)
- [ ] 支持多楼层场景 (楼梯、电梯)
- [ ] 优化大规模场景性能 (5000+行人)
- [ ] 增加场景编辑器 (在线修改预置场景)

### 中期 (Mid-term)
- [ ] 添加天气影响模拟 (雨雪天)
- [ ] 实现行人社交分组 (家庭、朋友)
- [ ] 支持障碍物动态移动 (车辆、临时障碍)
- [ ] 增加更多事件类型 (地震、洪水)

### 长期 (Long-term)
- [ ] 3D场景可视化 (Three.js)
- [ ] AI学习最优疏散策略
- [ ] 实时传感器数据集成
- [ ] 与城市数字孪生系统对接

---

## 🙏 致谢 / Acknowledgments

本预置场景系统的设计参考了以下研究和标准：
- Helbing, D., & Molnár, P. (1995). Social force model for pedestrian dynamics.
- GB 50016-2014 建筑设计防火规范
- ISO 16730-1:2015 Fire safety engineering
- 城市公共空间设计标准

---

## 📧 联系方式 / Contact

如有问题或建议，请通过以下方式联系：
- 项目文档: `README.md`, `PRESET_SCENARIOS.md`
- 技术支持: 查看 `DOCUMENTATION.md`
- 快速开始: 查看 `QUICKSTART.md`

---

**版本**: 1.0  
**发布日期**: 2024-10-30  
**维护状态**: 活跃维护中
