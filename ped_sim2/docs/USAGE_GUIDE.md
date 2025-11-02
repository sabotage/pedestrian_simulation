# 使用指南 | Usage Guide

## 启动系统 | Starting the System

### 1. 安装依赖 | Install Dependencies
```bash
cd c:\ymq\projects\ped_sim2
pip install -r requirements.txt
```

### 2. 启动Web界面 | Start Web Interface
```bash
python -m src.web.app
```

然后在浏览器中打开：http://localhost:5000

Then open in browser: http://localhost:5000

---

## 使用预置场景 | Using Preset Scenarios

系统提供5个预置场景：
The system provides 5 preset scenarios:

1. **繁忙的十字路口** (Busy Intersection) - `downtown_street.json`
   - 80×80米的城市十字路口
   - 4个方向的道路和人行横道
   - 4个角落的建筑物（商店、办公楼、餐厅、银行）
   - 推荐行人数：1000

2. **大学校园** (University Campus) - `campus.json`
   - 100×80米的校园场景
   - 教学楼、图书馆、食堂、宿舍
   - 推荐行人数：800

3. **医院** (Hospital) - `hospital.json`
   - 80×60米的医院场景
   - 急诊室、门诊部、住院楼
   - 推荐行人数：500

4. **购物中心** (Shopping Mall) - `shopping_mall.json`
   - 120×80米的购物中心
   - 主通道、商铺、美食广场
   - 推荐行人数：1500

5. **城市公园** (Urban Park) - `urban_park.json`
   - 100×80米的公园场景
   - 开放空间、湖泊、步道
   - 推荐行人数：600

### 加载预置场景 | Load Preset Scenario

1. 点击"Load Scenario"按钮
2. 选择JSON文件（在`scenarios/`文件夹中）
3. 系统会自动加载地图、入口、出口等设置

---

## 编辑地图 | Editing Map

### 工具说明 | Tool Descriptions

- **Wall** (墙) - 绘制障碍物/墙壁
- **Entrance** (入口) - 添加行人入口
- **Exit** (出口) - 添加行人出口
- **Clear** (清除) - 删除最近的元素

### 操作方法 | How to Use

1. **绘制墙壁**：
   - 选择Wall工具
   - 在地图上点击起点
   - 再点击终点，完成墙壁绘制

2. **添加入口**：
   - 选择Entrance工具
   - 设置半径（Radius）和流量（Flow Rate）
   - 在地图上点击位置

3. **添加出口**：
   - 选择Exit工具
   - 在地图上点击位置

4. **删除元素**：
   - 选择Clear工具
   - 点击要删除的元素附近

---

## 运行模拟 | Running Simulation

### 基本操作 | Basic Operations

1. **设置参数**：
   - Number of Pedestrians（行人数量）：建议100-2000
   - Speed：控制模拟速度（0.1-2.0）

2. **开始模拟**：
   - 点击"Start"按钮开始
   - 点击"Pause"暂停
   - 点击"Reset"重置

### 实时信息 | Real-time Information

- **Time**：当前模拟时间（秒）
- **Active Pedestrians**：当前场景中的行人数量
- **Total Exits**：已离开的行人数量

---

## 触发突发事件 | Triggering Emergency Events

### 事件类型 | Event Types

1. **Fire** (火灾)
   - 需要选择位置和影响半径
   - 行人会避开火灾区域

2. **Shooting** (枪击)
   - 需要选择位置和影响半径
   - 行人会恐慌逃离

3. **Block/Unblock Entrance** (入口封闭/开放)
   - 选择入口编号
   - 控制入口的开关状态

4. **Block/Unblock Exit** (出口封闭/开放)
   - 选择出口编号
   - 控制出口的开关状态

### 新功能：手动触发事件 | New Feature: Manual Event Triggering

#### 在地图上选择事件位置 | Select Event Position on Map

**适用事件**：Fire（火灾）、Shooting（枪击）

**操作步骤**：

1. **选择事件类型**
   - 在"Event Type"下拉菜单中选择"Fire"或"Shooting"
   - 系统会自动进入地图选择模式

2. **在地图上点击选择位置**
   - 直接在可视化地图上点击
   - 系统会自动填充X和Y坐标
   - 地图上会显示橙色预览圆圈

3. **设置事件半径**
   - Event Radius：影响范围（3-30米）
   - 默认值：10米
   - 修改半径后，预览圆圈会实时更新

4. **选择触发方式**
   - ✅ **Trigger Immediately（立即触发）**：
     - 默认选项
     - 事件在当前模拟时间立即发生
     - 不需要设置触发时间
   
   - ❌ **Scheduled Trigger（定时触发）**：
     - 取消勾选"Trigger Immediately"
     - 在"Event Time"输入框中设置触发时间（秒）
     - 事件会在指定时间发生

5. **预览事件信息**
   - 系统会显示事件预览信息：
     - 事件类型
     - 选择的位置坐标
     - 影响半径

6. **添加事件**
   - 点击"Add Event"按钮
   - 事件会根据选择立即触发或定时触发

#### 示例操作流程 | Example Workflow

**场景：在十字路口中心立即触发火灾**

1. 加载`downtown_street.json`场景
2. 设置1000个行人，点击Start
3. 在Emergency Events面板：
   - Event Type → 选择"Fire"
   - ✅ 确保"Trigger Immediately"已勾选
   - Event Radius → 设置为15（米）
   - 在地图上点击十字路口中心位置（约40, 40）
   - 观察橙色预览圆圈出现
   - 点击"Add Event"
4. 观察行人立即开始避开火灾区域

**场景：定时触发枪击事件**

1. 继续上述模拟
2. 在Emergency Events面板：
   - Event Type → 选择"Shooting"
   - ❌ 取消勾选"Trigger Immediately"
   - Event Time → 输入"30"（30秒后触发）
   - Event Radius → 设置为20（米）
   - 在地图上点击商店区域
   - 点击"Add Event"
3. 等待模拟时间到达30秒，观察行人恐慌逃离

---

## 导出Unity VR场景 | Export Unity VR Scene

### 导出步骤 | Export Steps

1. 在模拟运行时或运行后
2. 点击"Export Unity VR Scene"按钮
3. 系统会生成：
   - Unity脚本文件
   - 场景配置文件
   - 导出包

### 导出内容 | Export Contents

导出的Unity包包含：
- Environment prefabs（环境预制体）
- Pedestrian models（行人模型）
- Animation controllers（动画控制器）
- VR interaction scripts（VR交互脚本）

详见：[UNITY_EXPORT.md](UNITY_EXPORT.md)

---

## 快捷键 | Keyboard Shortcuts

- **Space** - 开始/暂停模拟
- **R** - 重置模拟
- **1** - 选择Wall工具
- **2** - 选择Entrance工具
- **3** - 选择Exit工具
- **4** - 选择Clear工具

---

## 常见问题 | FAQ

### 1. 地图上看不到行人？
- 检查是否点击了Start按钮
- 检查是否添加了入口（Entrance）
- 检查行人数量设置是否大于0

### 2. 行人不移动？
- 检查是否添加了出口（Exit）
- 检查路径是否被墙壁完全阻挡
- 尝试简化障碍物布局

### 3. 事件没有效果？
- 确认事件类型正确（Fire/Shooting需要位置，Block需要索引）
- 检查事件触发时间是否已到达
- 使用"Trigger Immediately"确保立即生效

### 4. 预览圆圈不显示？
- 确认选择了Fire或Shooting事件类型
- 确认已在地图上点击选择位置
- 检查Event Radius是否在3-30范围内

### 5. 如何测试新的突发事件功能？
推荐测试流程：
1. 加载预置场景（如`downtown_street.json`）
2. 启动模拟（500-1000行人）
3. 选择Fire事件，勾选"Trigger Immediately"
4. 在地图中心点击，观察预览圆圈
5. 设置半径为15米
6. 点击"Add Event"
7. 观察行人立即反应并避开火灾区域

### 6. 性能优化建议
- 推荐行人数量：
  - 测试：100-500
  - 一般场景：500-1000
  - 大型场景：1000-2000
- 降低模拟速度可提高精度
- 减少墙壁数量可提高性能

---

## 技术支持 | Technical Support

遇到问题？请查看：
- [API文档](API.md)
- [架构说明](ARCHITECTURE.md)
- [开发指南](DEVELOPMENT.md)

---

**享受你的行人模拟体验！**
**Enjoy your pedestrian simulation experience!**
