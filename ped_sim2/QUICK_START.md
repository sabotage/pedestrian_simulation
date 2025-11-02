# 快速开始 | Quick Start Guide

## 🚀 启动系统 | Launch System

```bash
# 进入项目目录
cd c:\ymq\projects\ped_sim2

# 启动Web服务器
python -m src.web.app
```

**重要**: 使用 **HTTP** 而不是 HTTPS！
**Important**: Use **HTTP** not HTTPS!

✅ 正确地址: **http://localhost:5000**  
❌ 错误地址: ~~https://localhost:5000~~

---

## 🎬 使用预置场景 | Using Preset Scenarios

打开浏览器访问 http://localhost:5000 后，你会看到5个预置场景：

### 1. 🚦 繁忙十字路口 (Busy Intersection)
**推荐行人数**: 1000

**特点**:
- 80×80米城市十字路口
- 4个方向的道路和人行横道
- 4个角落建筑（商店、办公楼、餐厅、银行）
- 8个入口，4个出口
- 适合测试多向人流和突发事件疏散

**快速测试**:
```
1. Select Scenario → Busy Intersection
2. Click "Load Selected Scenario"
3. Number of Pedestrians → 1000
4. Click "Start"
5. 观察四个方向的行人流动
```

---

### 2. 🎓 大学校园 (Campus)
**推荐行人数**: 800

**特点**:
- 100×80米校园场景
- 教学楼、图书馆、食堂、宿舍
- 多个内部通道和广场
- 适合测试复杂建筑群人流

---

### 3. 🏥 医院 (Hospital)
**推荐行人数**: 500

**特点**:
- 80×60米医院场景
- 急诊室、门诊部、住院楼
- 适合应急疏散演练

---

### 4. 🏬 购物中心 (Shopping Mall)
**推荐行人数**: 1500

**特点**:
- 120×80米大型购物中心
- 主通道、商铺、美食广场
- 高密度人流场景

---

### 5. 🌳 城市公园 (Urban Park)
**推荐行人数**: 600

**特点**:
- 100×80米开放公园
- 湖泊、步道、休息区
- 低密度休闲场景

---

## 🎮 基本操作流程 | Basic Workflow

### 步骤1：加载场景
```
1. 在"Preset Scenarios"下拉菜单中选择一个场景
2. 点击"Load Selected Scenario"按钮
3. 系统会自动加载地图、入口、出口等设置
4. 会弹出场景信息提示框
```

### 步骤2：设置行人数量
```
在"Simulation Control"面板中：
- Number of Pedestrians: 输入推荐数量（如1000）
- Speed: 保持默认1.0（可调节0.1-2.0）
```

### 步骤3：开始模拟
```
点击"Start"按钮
- 绿色圆点 = 行人
- 红色圆点 = 目标出口
- 蓝色圆点 = 入口
- 黑色线条 = 墙壁/障碍物
```

### 步骤4：触发突发事件（新功能！）
```
在"Emergency Events"面板中：

方式1：立即触发火灾
1. Event Type → Fire
2. ✅ "Trigger Immediately"已勾选
3. Event Radius → 15
4. 直接在地图上点击位置（会显示橙色预览圆圈）
5. 点击"Add Event"
6. 行人立即开始避开火灾区域

方式2：定时触发枪击
1. Event Type → Shooting
2. ❌ 取消勾选"Trigger Immediately"
3. Event Time → 30（30秒后）
4. Event Radius → 20
5. 在地图上点击位置
6. 点击"Add Event"
7. 等待30秒观察效果
```

---

## 🔥 推荐测试场景 | Recommended Test Scenarios

### 场景A：十字路口火灾疏散

```
场景: Busy Intersection
行人: 1000
事件: 中心火灾

步骤:
1. 加载"Busy Intersection"场景
2. 设置1000行人，启动模拟
3. 等待10秒让行人分散
4. Fire事件，立即触发，半径15米
5. 在地图中心(40, 40)点击
6. Add Event
7. 观察行人绕行路径

预期效果:
- 行人避开中心区域
- 选择四个方向的外围道路
- 部分行人改变目标出口
```

---

### 场景B：购物中心多事件协同

```
场景: Shopping Mall
行人: 1500
事件: 火灾 + 枪击 + 出口封闭

步骤:
1. 加载"Shopping Mall"场景
2. 设置1500行人，启动模拟
3. T=15s: Fire，立即触发，半径10米，美食广场位置
4. T=15s: Shooting，定时30s，半径20米，主通道位置
5. T=15s: Block Exit，定时40s，封闭出口0
6. 连续观察15s-40s的人流变化

预期效果:
- 15s: 美食广场行人疏散
- 30s: 主通道恐慌，大量行人改道
- 40s: 出口0封闭，行人拥堵后重新选择路径
```

---

### 场景C：医院应急演练

```
场景: Hospital
行人: 500
事件: 急诊室火灾

步骤:
1. 加载"Hospital"场景
2. 设置500行人，启动模拟
3. Fire事件，立即触发，半径8米
4. 点击急诊室位置
5. 观察疏散效率

分析指标:
- 疏散时间（所有行人离开的时间）
- 拥堵点位置
- 出口利用率
```

---

## 🎨 自定义地图（可选）| Custom Map (Optional)

如果你想自己编辑地图：

```
1. 不加载预置场景，或点击"Create Custom Environment"
2. 使用工具栏绘制：
   - Wall: 点击两次绘制墙壁
   - Entrance: 点击添加入口
   - Exit: 点击添加出口
   - Clear: 点击删除元素
3. 设置参数后启动模拟
```

---

## ⚙️ 导出Unity VR场景 | Export to Unity VR

```
1. 运行模拟
2. 点击"Export Unity VR Scene"
3. 文件会保存到exports/文件夹
4. 在Unity中导入并体验VR版本

详细说明请参考: UNITY_EXPORT.md
```

---

## 🐛 常见问题 | Troubleshooting

### Q1: 浏览器显示"无法连接"？
**A**: 确保使用 **http://** 而不是 https://
```
正确: http://localhost:5000
错误: https://localhost:5000
```

### Q2: 点击地图没有反应？
**A**: 检查是否选择了Fire或Shooting事件类型。只有这两种事件支持地图点击选择位置。

### Q3: 行人不移动？
**A**: 
1. 检查是否点击了Start按钮
2. 确认场景中有入口和出口
3. 确认路径没有被墙壁完全阻挡

### Q4: 预览圆圈不显示？
**A**: 
1. 确认Event Type是Fire或Shooting
2. 确认已在地图上点击
3. 检查Event Radius是否在3-30范围内

### Q5: 场景加载后是空白的？
**A**: 
1. 检查scenarios/文件夹中是否有JSON文件
2. 尝试重新生成场景：
   ```bash
   python examples/generate_preset_scenarios.py
   ```
3. 刷新浏览器页面

### Q6: 模拟很卡？
**A**: 
1. 减少行人数量（建议100-1000）
2. 降低模拟速度（Speed设为0.5）
3. 关闭其他浏览器标签页

---

## 📊 性能建议 | Performance Tips

| 场景 | 推荐行人数 | 最大行人数 | 预期帧率 |
|:-----|:----------:|:----------:|:--------:|
| 十字路口 | 1000 | 2000 | 30-60 FPS |
| 校园 | 800 | 1500 | 30-60 FPS |
| 医院 | 500 | 1000 | 60 FPS |
| 购物中心 | 1500 | 3000 | 20-30 FPS |
| 公园 | 600 | 1200 | 60 FPS |

**优化建议**:
- 低配电脑：300-500行人
- 标准配置：500-1500行人
- 高配电脑：1500-3000行人

---

## 🎓 学习路径 | Learning Path

### 初学者（5分钟）
```
1. 加载"Busy Intersection"场景
2. 启动500行人模拟
3. 观察人流模式
4. 尝试立即触发一个火灾事件
```

### 进阶用户（15分钟）
```
1. 测试所有5个预置场景
2. 对比不同场景的人流特点
3. 尝试立即触发和定时触发
4. 调节事件半径观察影响范围
```

### 高级用户（30分钟）
```
1. 设计多事件协同测试
2. 分析不同场景的疏散效率
3. 自定义地图布局
4. 导出Unity VR场景
```

---

## 📚 更多文档 | More Documentation

- **USAGE_GUIDE.md** - 详细使用指南
- **NEW_FEATURES.md** - 新功能技术说明
- **INTERSECTION_LAYOUT.md** - 十字路口布局详解
- **ARCHITECTURE.md** - 系统架构说明
- **API.md** - API文档

---

## 🎉 现在开始体验！| Start Now!

```bash
python -m src.web.app
```

然后访问: **http://localhost:5000**

选择一个预置场景，点击加载，开始你的行人模拟之旅！

---

**祝你使用愉快！**  
**Enjoy your pedestrian simulation!** 🚶‍♂️🚶‍♀️
