# 新功能说明 | New Features

## 最新更新 | Latest Updates

本次更新包含两个主要新功能：
This update includes two major new features:

---

## 1. 繁忙十字路口场景 | Busy Intersection Scenario

### 概述 | Overview

将原有的"繁忙街道"场景升级为更真实的**十字路口**场景。

Upgraded the original "Downtown Street" scenario to a more realistic **intersection** scenario.

### 场景特点 | Scenario Features

#### 地图尺寸 | Map Size
- **80×80米**（原100×40米线性街道）
- 80×80 meters (previously 100×40m linear street)

#### 核心区域 | Core Areas

1. **中央交叉路口** (Central Intersection)
   - 30×30米开放空间
   - 四个方向的人行横道（zebra crossings）
   - 交通信号区域

2. **四个角落建筑** (Four Corner Buildings)
   - **西北角 (NW)**: 商店 (Shop) - 15×15m
   - **东北角 (NE)**: 办公楼 (Office) - 20×18m
   - **西南角 (SW)**: 餐厅 (Restaurant) - 18×15m
   - **东南角 (SE)**: 银行 (Bank) - 20×20m

3. **道路网络** (Road Network)
   - 北向道路 (North Road)
   - 南向道路 (South Road)
   - 东向道路 (East Road)
   - 西向道路 (West Road)

#### 入口和出口 | Entrances and Exits

**8个入口** (8 Entrances):
- 主干道入口（北、南、东、西）- Main road entrances
- 建筑入口（4个角落建筑）- Building entrances

**4个主要出口** (4 Main Exits):
- 对应四个方向的道路出口

#### 推荐参数 | Recommended Parameters

- **行人数量** (Pedestrians): 1000
- **模拟速度** (Speed): 1.0
- **适合场景** (Suitable for):
  - 城市交通流测试
  - 人群密度分析
  - 交叉路口行人动态研究
  - 突发事件疏散演练

### 使用方法 | How to Use

```bash
# 1. 生成预置场景（如需重新生成）
python examples/generate_preset_scenarios.py

# 2. 启动Web界面
python -m src.web.app

# 3. 在浏览器中加载场景
# Load Scenario → 选择 scenarios/downtown_street.json
```

### 可视化特征 | Visual Features

- ✅ 人行横道标记（短墙段模拟斑马线）
- ✅ 四个角落的建筑障碍物
- ✅ 多向行人流动模式
- ✅ 真实的城市交叉路口布局

---

## 2. 手动事件触发系统 | Manual Event Triggering System

### 概述 | Overview

全新的**交互式事件触发**系统，允许用户通过点击地图直接选择事件位置，并支持立即触发或定时触发。

Brand new **interactive event triggering** system that allows users to select event positions by clicking on the map, with support for immediate or scheduled triggering.

### 核心功能 | Core Features

#### 2.1 地图点击选择位置 | Map Click Position Selection

**适用事件类型**:
- 🔥 Fire（火灾）
- 🔫 Shooting（枪击）

**功能说明**:
- 选择Fire或Shooting事件后，自动进入地图选择模式
- 在可视化地图上直接点击选择事件发生位置
- X、Y坐标自动填充，无需手动输入
- 实时显示橙色预览圆圈，直观显示事件影响范围

**视觉反馈**:
```
📍 橙色圆圈 - 事件影响范围预览
📍 中心点 - 事件精确位置
📍 虚线边框 - 半径范围指示
```

#### 2.2 立即触发 vs 定时触发 | Immediate vs Scheduled Trigger

**立即触发模式** (Immediate Trigger):
- ✅ 默认模式
- 事件在当前模拟时间立即发生
- 无需设置触发时间
- 适合：
  - 交互式演示
  - 实时干预测试
  - 即时响应验证

**定时触发模式** (Scheduled Trigger):
- 取消勾选"Trigger Immediately"
- 设置未来的触发时间（秒）
- 事件会在指定时间自动发生
- 适合：
  - 场景预设
  - 时间序列分析
  - 多事件协同测试

#### 2.3 可调节事件半径 | Adjustable Event Radius

**功能说明**:
- 范围：3-30米
- 默认值：10米
- 实时预览更新
- 影响事件的作用范围

**应用场景**:
- 小范围火灾（3-10米）
- 中等火灾（10-20米）
- 大范围枪击事件（20-30米）

#### 2.4 事件预览系统 | Event Preview System

**显示信息**:
```
事件预览：
类型：火灾
位置：(40.5, 42.3)
半径：15m
```

**实时更新**:
- 选择位置时更新
- 修改半径时更新
- 切换事件类型时更新

### 技术实现 | Technical Implementation

#### 前端交互 | Frontend Interaction

**JavaScript状态管理**:
```javascript
let eventSelectionMode = false;      // 事件选择模式标志
let selectedEventPosition = null;    // 选中的事件位置
let eventPreviewRadius = 10;         // 预览半径
```

**Canvas事件处理**:
```javascript
canvas.addEventListener('mousedown', (e) => {
    if (eventSelectionMode) {
        // 捕获点击坐标
        selectedEventPosition = [x, y];
        // 更新输入框
        document.getElementById('eventX').value = x.toFixed(1);
        document.getElementById('eventY').value = y.toFixed(1);
        // 显示预览
        drawEventPreview(x, y);
    }
});
```

**实时预览渲染**:
```javascript
function drawEventPreview(x, y) {
    // 绘制预览圆圈（橙色，虚线）
    ctx.beginPath();
    ctx.arc(x * scale, y * scale, radius * scale, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255, 165, 0, 0.8)';
    ctx.setLineDash([5, 5]);
    ctx.stroke();
}
```

#### 后端处理 | Backend Processing

**事件数据结构**:
```python
{
    "type": "fire",              # 事件类型
    "trigger_time": 42.5,        # 触发时间（立即或定时）
    "position": [40.5, 42.3],    # 事件位置
    "radius": 15.0               # 影响半径
}
```

**立即触发逻辑**:
```javascript
const triggerTime = immediateEvent ? 
    (simulatorState.time || 0) :  // 立即：当前时间
    parseFloat(eventTime.value);   // 定时：指定时间
```

### 使用示例 | Usage Examples

#### 示例1：立即触发火灾事件

**步骤**:
1. 加载`downtown_street.json`场景
2. 启动模拟（1000行人）
3. Emergency Events面板：
   - Event Type → "Fire"
   - ✅ "Trigger Immediately"（已勾选）
   - Event Radius → 15
4. 在地图十字路口中心点击
5. 观察橙色预览圆圈
6. 点击"Add Event"
7. **立即效果**：行人开始避开火灾区域

#### 示例2：定时触发枪击事件

**步骤**:
1. 继续上述模拟
2. Emergency Events面板：
   - Event Type → "Shooting"
   - ❌ 取消"Trigger Immediately"
   - Event Time → 30（30秒后）
   - Event Radius → 20
3. 在地图商店区域点击
4. 观察预览信息显示
5. 点击"Add Event"
6. **等待30秒**：枪击事件触发，行人恐慌逃离

#### 示例3：多事件协同测试

**场景**：模拟复杂突发状况

```
T=0s:   开始模拟（1000行人）
T=10s:  十字路口中心火灾（立即触发，半径15m）
T=20s:  西北商店区域枪击（定时触发，半径20m）
T=35s:  封闭东侧出口（定时触发）
```

**操作**:
1. T=0s：启动模拟
2. T=10s：
   - 立即触发模式
   - Fire，半径15m
   - 点击中心(40, 40)
   - Add Event
3. T=10s（继续）：
   - 切换到定时模式
   - Shooting，时间20s，半径20m
   - 点击商店(15, 65)
   - Add Event
4. T=10s（继续）：
   - Block Exit，时间35s
   - 选择出口索引0
   - Add Event

**观察效果**:
- 10s：行人避开中心火灾
- 20s：行人从商店区域恐慌逃离
- 35s：东侧出口关闭，行人改变路线

### 界面更新 | UI Updates

#### HTML控件 | HTML Controls

**新增元素**:
```html
<!-- 立即触发复选框 -->
<input type="checkbox" id="immediateEvent" checked>
<label for="immediateEvent">Trigger Immediately (立即触发)</label>

<!-- 事件半径控制 -->
<label for="eventRadius">Event Radius (m):</label>
<input type="number" id="eventRadius" value="10" min="3" max="30">

<!-- 只读位置输入框 -->
<input type="number" id="eventX" readonly 
       style="background-color: #f0f0f0;">
<input type="number" id="eventY" readonly 
       style="background-color: #f0f0f0;">

<!-- 预览区域 -->
<div id="eventPreview" style="display: none;">
    <!-- 动态生成预览信息 -->
</div>
```

**提示文本**:
```
📍 Click on map to select position / 点击地图选择位置
```

### 优势和应用 | Advantages and Applications

#### 用户体验改进 | UX Improvements

✅ **直观交互**：点击地图比手动输入坐标更自然
✅ **实时预览**：立即看到事件影响范围
✅ **灵活触发**：支持立即和定时两种模式
✅ **可视化反馈**：橙色圆圈清晰显示事件位置和范围

#### 应用场景 | Use Cases

1. **应急演练**
   - 模拟火灾、枪击等突发事件
   - 测试疏散路线和响应时间
   - 验证应急预案有效性

2. **城市规划**
   - 分析人流密集区域
   - 评估突发事件影响范围
   - 优化疏散通道设计

3. **科研分析**
   - 行人行为研究
   - 恐慌扩散模型验证
   - 社会力模型参数调优

4. **教学演示**
   - 交互式课堂演示
   - 学生实验操作
   - 可视化教学案例

### 扩展可能 | Future Extensions

**计划功能**:
- [ ] 事件历史记录和回放
- [ ] 自定义事件类型
- [ ] 事件强度调节（低/中/高）
- [ ] 多事件模板保存/加载
- [ ] 事件影响热力图显示

---

## 测试建议 | Testing Recommendations

### 快速测试流程 | Quick Test Workflow

**5分钟快速验证**:

```bash
# 1. 启动系统
python -m src.web.app

# 2. 打开浏览器 http://localhost:5000

# 3. 测试十字路口场景
- Load Scenario → downtown_street.json
- Number of Pedestrians → 1000
- Click Start

# 4. 测试立即触发
- Event Type → Fire
- ✅ Trigger Immediately
- Event Radius → 15
- 点击地图中心
- Add Event
- 观察行人立即反应

# 5. 测试定时触发
- Event Type → Shooting
- ❌ Trigger Immediately
- Event Time → 20
- Event Radius → 20
- 点击地图角落
- Add Event
- 等待20秒观察效果
```

### 性能测试 | Performance Testing

**推荐配置**:
- 行人数量：100-2000
- 事件半径：3-30米
- 同时事件：最多5个

**压力测试**:
- 2000行人 + 3个同时事件
- 观察帧率和响应时间
- 检查内存使用情况

---

## 文件变更清单 | File Changes

### 修改的文件 | Modified Files

1. **examples/generate_preset_scenarios.py**
   - 重写`create_downtown_street()`方法
   - 从线性街道改为十字路口布局
   - 添加人行横道和4个角落建筑

2. **scenarios/downtown_street.json**
   - 新的80×80米地图配置
   - 8个入口，4个出口
   - ~60个墙壁元素

3. **src/web/templates/index.html**
   - 添加"Trigger Immediately"复选框
   - 位置输入框改为只读
   - 添加事件半径控制
   - 添加预览区域

4. **src/web/static/app.js**
   - 添加事件选择模式状态
   - 实现Canvas点击处理器
   - 添加事件预览绘制函数
   - 添加立即/定时触发逻辑
   - 添加半径调节事件监听器

### 新增的文件 | New Files

1. **docs/USAGE_GUIDE.md**
   - 完整的使用指南
   - 包含新功能详细说明

2. **docs/NEW_FEATURES.md**
   - 本文档
   - 新功能技术说明

---

## 总结 | Summary

本次更新通过两个核心功能显著提升了系统的实用性和交互性：

1. **十字路口场景**提供了更真实的城市环境模拟
2. **手动事件触发系统**使用户能够更直观、灵活地控制突发事件

这些改进使系统更适合：
- ✅ 城市应急演练
- ✅ 行人行为研究
- ✅ 交互式教学演示
- ✅ 复杂场景测试

**立即体验新功能：**
```bash
python -m src.web.app
```
然后访问 http://localhost:5000

---

**更新日期** | Update Date: 2024
**版本** | Version: 2.0
