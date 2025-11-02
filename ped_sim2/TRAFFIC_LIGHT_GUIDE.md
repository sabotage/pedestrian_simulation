# 🚦 Traffic Light System Guide
## 交通灯系统使用指南

## Overview / 概述

The traffic light system allows you to control pedestrian crossing behavior in busy road scenarios. Pedestrians will wait for green lights before crossing designated crossing lanes.

交通灯系统允许您在繁忙道路场景中控制行人过马路的行为。行人会等待绿灯才能通过指定的人行横道。

---

## Features / 功能特性

### ✨ Key Features / 主要功能

1. **Automated Traffic Lights** / **自动化交通灯**
   - Red and green light cycles / 红绿灯循环
   - Configurable cycle duration / 可配置的周期时长
   - Visual traffic light poles / 可视化的交通灯柱

2. **Pedestrian Crossing Lanes** / **人行横道**
   - Zebra crossing stripes / 斑马线条纹
   - Associated with traffic lights / 与交通灯关联
   - Width-configurable lanes / 可配置宽度的车道

3. **Smart Pedestrian Behavior** / **智能行人行为**
   - Wait at red lights / 红灯时等待
   - Cross on green lights / 绿灯时通过
   - Automatic traffic light detection / 自动检测交通灯

---

## Configuration / 配置

### Traffic Light Parameters / 交通灯参数

Located in `app.js`:
```javascript
let trafficLightCycle = 10;    // Total cycle time in seconds / 总周期时间（秒）
let greenLightDuration = 5;    // Green light duration in seconds / 绿灯持续时间（秒）
```

**Calculation** / **计算方式**:
- Red light duration = `trafficLightCycle - greenLightDuration`
- 红灯持续时间 = 总周期时间 - 绿灯持续时间

### JSON Structure / JSON 结构

#### Traffic Light Object / 交通灯对象
```json
{
  "id": "light_north",
  "position": [26, 27],
  "orientation": "vertical"
}
```

**Fields** / **字段说明**:
- `id`: Unique identifier / 唯一标识符
- `position`: [x, y] coordinates / [x, y] 坐标
- `orientation`: "vertical" or "horizontal" / "vertical"（垂直）或 "horizontal"（水平）

#### Crossing Lane Object / 人行横道对象
```json
{
  "start": [26, 30],
  "end": [26, 50],
  "width": 4,
  "trafficLightId": "light_north"
}
```

**Fields** / **字段说明**:
- `start`: Starting point [x, y] / 起点坐标 [x, y]
- `end`: Ending point [x, y] / 终点坐标 [x, y]
- `width`: Lane width in meters / 车道宽度（米）
- `trafficLightId`: Associated traffic light ID / 关联的交通灯ID

---

## Example Scenario / 示例场景

The **Busy Intersection** (`downtown_street.json`) includes:
**繁忙十字路口** (`downtown_street.json`) 包含：

### Traffic Lights / 交通灯
- 4 traffic lights at intersection corners / 路口四角的4个交通灯
- 2 orientations (vertical & horizontal) / 2种方向（垂直和水平）
- Synchronized timing / 同步计时

### Crossing Lanes / 人行横道
- 4 zebra crossings / 4条斑马线
- North-South and East-West directions / 南北和东西方向
- 4-meter wide lanes / 4米宽的车道

---

## How It Works / 工作原理

### 1. Traffic Light Cycle / 交通灯周期

```
Red Phase:   [0 - 5 seconds]   / 红灯阶段
Green Phase: [5 - 10 seconds]  / 绿灯阶段
[Repeat] / [循环重复]
```

### 2. Pedestrian Behavior / 行人行为

**When Approaching Crossing** / **接近人行横道时**:
1. Check nearby traffic light / 检查附近的交通灯
2. If RED → Stop and wait / 如果是红灯 → 停下等待
3. If GREEN → Continue crossing / 如果是绿灯 → 继续通过

**Visual Indicators** / **视觉指示**:
- 🟢 Green pedestrians = Can cross / 绿色行人 = 可以通过
- ⏸ Pause icon = Stopped/waiting / 暂停图标 = 停下/等待

### 3. Detection Logic / 检测逻辑

The system automatically detects:
系统自动检测：

- If pedestrian is near a crossing lane / 行人是否靠近人行横道
- Which traffic light controls that crossing / 哪个交通灯控制该横道
- Current state of traffic light (red/green) / 交通灯的当前状态（红/绿）

---

## Customization / 自定义

### Adjusting Timing / 调整时间

Edit `app.js` lines 20-21:
编辑 `app.js` 第20-21行：

```javascript
// Example: Longer cycle for heavy traffic
let trafficLightCycle = 15;    // 15 second cycle
let greenLightDuration = 7;    // 7 seconds green, 8 seconds red

// Example: Quick cycle for testing
let trafficLightCycle = 6;     // 6 second cycle
let greenLightDuration = 3;    // 3 seconds each
```

### Adding New Traffic Lights / 添加新交通灯

Add to scenario JSON file:
添加到场景JSON文件：

```json
"trafficLights": [
  {
    "id": "your_light_id",
    "position": [x, y],
    "orientation": "vertical"
  }
]
```

### Adding New Crossings / 添加新人行横道

```json
"crossingLanes": [
  {
    "start": [x1, y1],
    "end": [x2, y2],
    "width": 4,
    "trafficLightId": "your_light_id"
  }
]
```

---

## Tips & Best Practices / 提示和最佳实践

### 🎯 Placement Tips / 放置建议

1. **Traffic Lights** / **交通灯**
   - Place near intersection corners / 放置在路口拐角附近
   - Use vertical for N-S roads / 南北向道路使用垂直方向
   - Use horizontal for E-W roads / 东西向道路使用水平方向

2. **Crossing Lanes** / **人行横道**
   - Align perpendicular to road / 垂直于道路对齐
   - 4-6 meter width recommended / 推荐4-6米宽度
   - Connect sidewalks on both sides / 连接两侧的人行道

### ⚙️ Performance Tips / 性能建议

- Limit to 4-8 traffic lights per scenario / 每个场景限制4-8个交通灯
- Keep crossing lanes under 100 meters / 人行横道长度保持在100米以内
- Use reasonable timing (5-15 second cycles) / 使用合理的时间（5-15秒周期）

### 🧪 Testing Tips / 测试建议

1. Start with small number of pedestrians / 从少量行人开始
2. Observe waiting behavior at red lights / 观察红灯时的等待行为
3. Check crossing flow during green / 检查绿灯时的通过流量
4. Adjust timing based on congestion / 根据拥堵情况调整时间

---

## Visual Elements / 视觉元素

### Traffic Light Appearance / 交通灯外观

- **Pole**: Dark gray (#424242) / **灯柱**: 深灰色
- **Light Box**: Black (#212121) / **灯箱**: 黑色
- **Red Light**: Bright red gradient (when on) / **红灯**: 明亮的红色渐变（亮起时）
- **Green Light**: Bright green gradient (when on) / **绿灯**: 明亮的绿色渐变（亮起时）
- **Inactive Lights**: Dark red/green / **未激活灯**: 深红/深绿

### Crossing Lane Appearance / 人行横道外观

- **Background**: Light gray (#e0e0e0) / **背景**: 浅灰色
- **Stripes**: White (#ffffff) / **条纹**: 白色
- **Pattern**: 8px stripe, 8px gap / **图案**: 8像素条纹，8像素间隔
- **Border**: Dark gray lines / **边框**: 深灰色线条

---

## Troubleshooting / 故障排除

### Issue: Pedestrians not stopping at red light
### 问题：行人在红灯时不停止

**Solution** / **解决方案**:
- Check `trafficLightId` matches in JSON / 检查JSON中的`trafficLightId`是否匹配
- Verify traffic light position is near crossing / 验证交通灯位置是否靠近横道
- Ensure crossing lane has correct coordinates / 确保人行横道坐标正确

### Issue: Traffic lights not visible
### 问题：交通灯不可见

**Solution** / **解决方案**:
- Check position coordinates are within environment bounds / 检查位置坐标是否在环境范围内
- Verify `trafficLights` array is in environment object / 验证`trafficLights`数组在环境对象中
- Load scenario after creating environment / 创建环境后加载场景

### Issue: Crossing lanes not showing
### 问题：人行横道不显示

**Solution** / **解决方案**:
- Verify `crossingLanes` array exists / 验证`crossingLanes`数组存在
- Check start and end coordinates / 检查起点和终点坐标
- Ensure width parameter is reasonable (2-10) / 确保宽度参数合理（2-10）

---

## Future Enhancements / 未来增强

Planned features / 计划中的功能:
- [ ] Pedestrian countdown timers / 行人倒计时
- [ ] Yellow/amber warning phase / 黄灯/琥珀色警告阶段
- [ ] Adjustable timing per light / 每个灯的可调时间
- [ ] Manual light control mode / 手动灯光控制模式
- [ ] Traffic light synchronization groups / 交通灯同步组

---

## Code Reference / 代码参考

### Key Functions / 关键函数

1. `updateTrafficLights(currentTime)` - Updates all traffic light states / 更新所有交通灯状态
2. `drawTrafficLight(x, y, state, orientation)` - Renders a traffic light / 渲染交通灯
3. `drawCrossingLane(x1, y1, x2, y2, width)` - Renders zebra crossing / 渲染斑马线
4. `canCrossCrossing(pedPosition, crossingLane)` - Checks if pedestrian can cross / 检查行人是否可以通过

### State Management / 状态管理

```javascript
trafficLightStates = {
  "light_north": {
    state: "red",        // Current state / 当前状态
    lastChange: 0        // Last change time / 上次变化时间
  }
}
```

---

## Contact & Support / 联系与支持

For questions or issues:
如有问题或疑问：

- Check this guide first / 先查看本指南
- Review example scenario: `downtown_street.json`
- Inspect browser console for errors / 检查浏览器控制台的错误

---

**Happy Simulating! / 祝模拟愉快！** 🚦🚶‍♂️🚶‍♀️
