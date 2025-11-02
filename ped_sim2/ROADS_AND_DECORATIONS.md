# Roads and Decorations Guide / 道路和装饰指南

## Overview / 概述

This document describes the new roads and decorations system for pedestrian simulation scenarios.

本文档描述了行人模拟场景的新道路和装饰系统。

## Features / 功能

### Roads System / 道路系统

The roads system constrains pedestrian movement to designated pathways, making simulations more realistic for outdoor environments like parks.

道路系统将行人移动限制在指定路径上，使公园等户外环境的模拟更加真实。

**Configuration / 配置:**

```json
"roads": [
  {
    "points": [[x1, y1], [x2, y2], [x3, y3]],
    "width": 4
  }
]
```

- `points`: Array of coordinates defining the road path / 定义道路路径的坐标数组
- `width`: Road width in meters (default: 4) / 道路宽度（米，默认：4）

**Visual Rendering / 视觉渲染:**
- Gray asphalt surface with darker edges / 灰色沥青表面，边缘较深
- Yellow dashed center line / 黄色虚线中心线
- Isometric 3D perspective / 等距3D透视图

**Movement Constraints / 移动限制:**
- When roads are present, pedestrians can ONLY move on road surfaces / 当存在道路时，行人只能在道路表面移动
- Pathfinding automatically adapts to road-only mode / 路径寻找自动适应仅道路模式
- Pedestrians will find shortest path along roads / 行人将沿道路寻找最短路径

### Decorations System / 装饰系统

Decorations add visual interest and environmental context to scenarios.

装饰为场景增添视觉趣味和环境背景。

**Types / 类型:**

#### Trees / 树木

```json
{"type": "tree", "position": [x, y]}
```

**Visual Features / 视觉特征:**
- Brown trunk with vertical cylinder shape / 棕色树干，垂直圆柱形
- Three-layer green foliage with highlights / 三层绿色树叶，带高光
- Isometric 3D appearance with depth / 等距3D外观，有深度感
- Height: ~2.5 meters / 高度：约2.5米

#### Ponds / 池塘

```json
{"type": "pond", "position": [x, y], "radius": 5}
```

**Visual Features / 视觉特征:**
- Blue water with gradient from light to dark / 蓝色水面，由浅到深渐变
- Concentric ripple effects / 同心圆涟漪效果
- Shimmer/highlight on surface / 表面光泽/高光
- Isometric ellipse perspective / 等距椭圆透视图

## Urban Park Example / 城市公园示例

The Urban Park scenario has been enhanced with:

城市公园场景已增强：

**Roads / 道路:**
- Main paths connecting all entrances/exits / 连接所有出入口的主要道路
- Grid pattern for easy navigation / 网格图案，便于导航
- 4-meter wide pedestrian paths / 4米宽的步行道

**Decorations / 装饰:**
- 30+ trees distributed throughout the park / 30多棵树分布在整个公园
- 3 ponds of varying sizes / 3个不同大小的池塘
- Trees clustered near ponds for realism / 树木聚集在池塘附近，增加真实感

## Implementation Details / 实现细节

### Backend / 后端

**PathFinder enhancements:**
- `set_roads_only_mode(enabled)`: Enable/disable road constraints / 启用/禁用道路限制
- `add_road_segment(points, width)`: Add walkable road paths / 添加可行走的道路路径
- `_mark_road_segment()`: Mark grid cells as walkable / 将网格单元标记为可行走
- `_is_valid_cell()`: Validates cells are on roads when in roads-only mode / 在仅道路模式下验证单元格在道路上

**Environment properties:**
- `roads`: List of road segment configurations / 道路段配置列表
- `decorations`: List of decoration objects / 装饰对象列表

### Frontend / 前端

**Rendering functions:**
- `drawIsoRoad(points, width)`: Draws road with perspective / 绘制透视道路
- `drawIsoTree(x, y)`: Draws 3D tree with foliage / 绘制带树叶的3D树
- `drawIsoPond(x, y, radius)`: Draws water with ripples / 绘制带涟漪的水面

**Rendering order:**
1. Background (sky + grass) / 背景（天空+草地）
2. Roads (ground level) / 道路（地面层）
3. Decorations (trees, ponds) / 装饰（树木、池塘）
4. Walls / 墙壁
5. Crossing lanes / 人行横道
6. Entrances/Exits / 出入口
7. Traffic lights / 交通灯
8. Pedestrians / 行人

## Creating Custom Scenarios / 创建自定义场景

To add roads and decorations to a scenario:

要向场景添加道路和装饰：

1. **Design road network / 设计道路网络:**
   - Plan main paths connecting key points / 规划连接关键点的主要道路
   - Use grid or organic patterns / 使用网格或有机图案
   - Ensure all entrances/exits are accessible / 确保所有出入口可达

2. **Add decorations / 添加装饰:**
   - Trees for natural areas / 树木用于自然区域
   - Ponds for water features / 池塘用于水景
   - Cluster decorations for realistic appearance / 聚集装饰物以获得真实外观

3. **Test pathfinding / 测试路径寻找:**
   - Verify pedestrians can reach all exits / 验证行人可以到达所有出口
   - Check for bottlenecks in road network / 检查道路网络中的瓶颈
   - Ensure decorations don't block paths / 确保装饰不会阻挡道路

## Best Practices / 最佳实践

- **Road Width / 道路宽度:** 3-6 meters for pedestrian paths / 步行道3-6米
- **Tree Spacing / 树木间距:** 3-5 meters apart for natural look / 相距3-5米，外观自然
- **Pond Placement / 池塘位置:** Away from main paths / 远离主要道路
- **Network Design / 网络设计:** Multiple routes to prevent congestion / 多条路线以防止拥堵

## Troubleshooting / 故障排除

**Pedestrians not moving:**
- Ensure roads connect entrance to exit / 确保道路连接出入口
- Check road width is sufficient (min 2m) / 检查道路宽度是否足够（最小2米）
- Verify pathfinding grid is updated / 验证路径寻找网格已更新

**Decorations not visible:**
- Check decoration type spelling / 检查装饰类型拼写
- Verify position is within environment bounds / 验证位置在环境范围内
- Ensure JSON syntax is correct / 确保JSON语法正确

**Visual glitches:**
- Trees or ponds may overlap - adjust positions / 树木或池塘可能重叠 - 调整位置
- Use isometric view for best visual effect / 使用等距视图以获得最佳视觉效果

## Future Enhancements / 未来增强

Potential additions:
- Benches and streetlights / 长椅和路灯
- Flower beds and bushes / 花坛和灌木丛
- Bridges over ponds / 池塘上的桥梁
- Seasonal variations (autumn leaves, snow) / 季节变化（秋叶、雪）
- Weather effects (rain on ponds) / 天气效果（池塘上的雨）

---

**File Modified / 修改的文件:**
- `scenarios/urban_park.json` - Enhanced with roads and decorations / 增强了道路和装饰
- `src/simulation/pathfinding.py` - Added roads-only movement / 添加了仅道路移动
- `src/simulation/environment.py` - Store roads and decorations / 存储道路和装饰
- `src/simulation/simulator.py` - Load roads into pathfinding / 将道路加载到路径寻找
- `src/web/static/app.js` - Visual rendering of roads and decorations / 道路和装饰的视觉渲染

**Created / 创建日期:** October 30, 2025
**Version / 版本:** 1.0
