# Isometric View Fixes / 等距视图修复

**Date:** October 30, 2025  
**Issues Fixed:** Complete map visibility + Roads not showing

## Problems Identified / 发现的问题

### 1. **Map Not Fully Visible in Isometric View**
The 45-degree isometric view was not centered properly, causing larger maps (like Urban Park 100x100) to be partially off-screen.

地图在等距视图中不完全可见。45度等距视图没有正确居中，导致较大的地图（如城市公园100x100）部分超出屏幕。

### 2. **Roads Not Rendering on Urban Park Map**
Roads and decorations (trees, ponds) were not appearing because the frontend wasn't loading these properties from the scenario data.

道路未在城市公园地图上渲染。道路和装饰（树木、池塘）没有出现，因为前端没有从场景数据中加载这些属性。

## Solutions Implemented / 实施的解决方案

### Fix 1: Centered Isometric Projection / 居中等距投影

**File:** `src/web/static/app.js`

**Changes to `toIso()` function:**
```javascript
// OLD - Fixed offset from canvas corner
return {
    x: canvas.width / 2 + isoX * scale * isoScale,
    y: canvas.height / 4 + isoY * scale * isoScale
};

// NEW - Centered based on environment size
const centerX = environment.width / 2;
const centerY = environment.height / 2;
const isoX = ((x - centerX) - (y - centerY)) * Math.cos(isoAngle);
const isoY = ((x - centerX) + (y - centerY)) * Math.sin(isoAngle) - z;

return {
    x: canvas.width / 2 + isoX * scale * isoScale,
    y: canvas.height / 2 + isoY * scale * isoScale * 0.7
};
```

**Key Improvements:**
- Centers projection around environment midpoint (width/2, height/2)
- Uses vertical offset of 0.7 instead of positioning at 1/4 canvas height
- Works for any environment size (50x50, 100x100, etc.)

**主要改进：**
- 围绕环境中点（宽度/2，高度/2）居中投影
- 使用0.7的垂直偏移而不是定位在1/4画布高度
- 适用于任何环境尺寸（50x50、100x100等）

**Corresponding `fromIso()` update:**
```javascript
const centerX = environment.width / 2;
const centerY = environment.height / 2;

const isoX = (screenX - canvas.width / 2) / (scale * isoScale);
const isoY = (screenY - canvas.height / 2) / (scale * isoScale * 0.7);

const x = (isoX / Math.cos(isoAngle) + isoY / Math.sin(isoAngle)) / 2 + centerX;
const y = (isoY / Math.sin(isoAngle) - isoX / Math.cos(isoAngle)) / 2 + centerY;
```

### Fix 2: Load Roads and Decorations / 加载道路和装饰

**File:** `src/web/static/app.js`

**Three locations updated:**

#### A. Default environment initialization:
```javascript
let environment = {
    width: 50,
    height: 50,
    walls: [],
    entrances: [],
    exits: [],
    trafficLights: [],
    crossingLanes: [],
    roads: [],          // ADDED
    decorations: []     // ADDED
};
```

#### B. `loadPresetScenario()` function:
```javascript
environment = {
    width: scenarioEnv.width,
    height: scenarioEnv.height,
    walls: scenarioEnv.walls.map(w => ({ start: w[0], end: w[1] })),
    entrances: scenarioEnv.entrances || [],
    exits: scenarioEnv.exits || [],
    roads: scenarioEnv.roads || [],                   // ADDED
    decorations: scenarioEnv.decorations || [],       // ADDED
    trafficLights: scenarioEnv.trafficLights || [],   // ADDED
    crossingLanes: scenarioEnv.crossingLanes || []    // ADDED
};

console.log(`Environment loaded: ${environment.walls.length} walls, 
    ${environment.entrances.length} entrances, 
    ${environment.exits.length} exits, 
    ${environment.roads?.length || 0} roads,                    // ADDED
    ${environment.decorations?.length || 0} decorations`);      // ADDED
```

#### C. `scenario_loaded` event handler:
```javascript
socket.on('scenario_loaded', (data) => {
    const serverEnv = data.environment;
    environment = {
        width: serverEnv.width,
        height: serverEnv.height,
        walls: serverEnv.walls.map(w => ({ start: w[0], end: w[1] })),
        entrances: serverEnv.entrances || [],
        exits: serverEnv.exits || [],
        roads: serverEnv.roads || [],                   // ADDED
        decorations: serverEnv.decorations || [],       // ADDED
        trafficLights: serverEnv.trafficLights || [],   // ADDED
        crossingLanes: serverEnv.crossingLanes || []    // ADDED
    };
    
    console.log(`Server confirmed: ${environment.walls.length} walls, 
        ${environment.entrances.length} entrances, 
        ${environment.exits.length} exits, 
        ${environment.roads?.length || 0} roads,                    // ADDED
        ${environment.decorations?.length || 0} decorations`);      // ADDED
});
```

### Fix 3: Debug Logging / 调试日志

**Added console logging in `drawEnvironment()`:**
```javascript
if (environment.roads) {
    console.log('Drawing', environment.roads.length, 'roads');
    environment.roads.forEach(road => {
        console.log('Road:', road.points.length, 'points, width:', road.width);
        drawIsoRoad(road.points, road.width || 4);
    });
}
```

This helps verify that roads are being loaded and rendered.

这有助于验证道路是否被加载和渲染。

## Testing / 测试

**To verify the fixes:**

1. **Start the server:**
   ```bash
   cd c:\ymq\projects\ped_sim2
   python src/web/app.py
   ```

2. **Open browser:** http://localhost:5000

3. **Load Urban Park scenario:**
   - Select "Urban Park" from preset dropdown
   - Click dropdown to load

4. **Check browser console (F12):**
   Should see:
   ```
   Loaded scenarios: ['downtown_street', 'campus', 'hospital', 'shopping_mall', 'urban_park']
   Environment loaded: ... 14 roads, 33 decorations
   Drawing 14 roads
   Road: 2 points, width: 4
   Road: 2 points, width: 4
   ... (14 total)
   ```

5. **Visual verification:**
   - ✅ Full map visible in isometric view
   - ✅ Gray roads with yellow center lines
   - ✅ Green trees with foliage
   - ✅ Blue ponds with ripples
   - ✅ All elements properly centered

**验证修复：**

1. 启动服务器
2. 打开浏览器 http://localhost:5000
3. 加载城市公园场景
4. 检查浏览器控制台 - 应该看到14条道路，33个装饰
5. 视觉验证 - 完整地图可见，道路、树木、池塘都正确显示

## Urban Park Scenario Details / 城市公园场景详情

**Environment Size:** 100m x 100m  
**Roads:** 14 segments forming a grid network  
**Decorations:**
- 30 trees (type: "tree")
- 3 ponds (type: "pond", radii: 5m, 6m, 8m)

**Road Network Layout:**
- North-South main path through center (x=50)
- East-West main path through center (y=50)
- Connecting paths at y=20 and y=80
- Grid junctions at (20,20), (50,20), (80,20), etc.
- Total path coverage: ~400 meters

## Technical Notes / 技术说明

**Isometric Projection Math:**
- Angle: 30° (π/6 radians)
- Scale factor: 0.86
- Vertical compression: 0.7
- Center offset: environment.width/2, environment.height/2

**Rendering Order:**
1. Sky background
2. Ground grid
3. Roads
4. Decorations (trees, ponds)
5. Walls
6. Crossing lanes
7. Entrances/Exits
8. Traffic lights
9. Pedestrians

## Files Modified / 修改的文件

- ✅ `src/web/static/app.js` - Fixed projection + load roads/decorations
- ✅ `scenarios/urban_park.json` - Already contains roads and decorations (from previous update)
- ✅ `src/simulation/environment.py` - Already supports roads/decorations (from previous update)
- ✅ `src/simulation/pathfinding.py` - Already implements road constraints (from previous update)

## Known Limitations / 已知限制

- Roads currently only work with scenario presets (not manually drawable in UI)
- Isometric view cannot be toggled off (always enabled)
- Mouse interaction in isometric view may have slight offset at extreme corners

未来可能的改进：
- Add UI controls to draw roads manually
- Toggle between 2D and isometric views
- Adjust camera zoom/pan in isometric mode
- Add more decoration types (benches, fountains, etc.)

---

**Status:** ✅ FIXED  
**Tested:** Urban Park scenario  
**Browser:** Chrome/Edge (Simple Browser)  
**Server:** Flask 3.0 + SocketIO 4.5.4
