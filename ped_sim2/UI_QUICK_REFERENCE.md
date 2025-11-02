# UI Quick Reference Guide

## CSS Variables Reference

Use these CSS variables throughout the project for consistency:

```css
/* Background Colors */
var(--primary-bg)    /* #1a1a2e - Main dark background */
var(--secondary-bg)  /* #16213e - Sidebars, panels */
var(--tertiary-bg)   /* #0f3460 - Canvas area background */

/* Accent Colors */
var(--accent-color)  /* #e94560 - Primary accent (pink-red) */
var(--success-color) /* #00d4aa - Success actions (teal) */
var(--danger-color)  /* #ff6b6b - Danger/stop (coral red) */
var(--warning-color) /* #ffa500 - Warning/events (orange) */

/* Text Colors */
var(--text-primary)   /* #eee - Main text color */
var(--text-secondary) /* #aaa - Secondary text, labels */

/* Borders & Shadows */
var(--border-color)   /* #2a2a3e - Borders, separators */
var(--card-shadow)    /* 0 4px 20px rgba(0,0,0,0.5) - Card shadows */
```

## Common Component Classes

### Buttons
```html
<!-- Primary action -->
<button class="btn btn-primary">Primary Action</button>

<!-- Success (start, confirm) -->
<button class="btn btn-success">Start / Confirm</button>

<!-- Danger (stop, delete) -->
<button class="btn btn-danger">Stop / Delete</button>

<!-- Warning (reset, caution) -->
<button class="btn btn-warning">Reset / Warning</button>

<!-- Secondary (load, alternative) -->
<button class="btn btn-secondary">Load / Secondary</button>
```

### Input Groups
```html
<div class="input-group">
    <label for="myInput">Label Text:</label>
    <input type="number" id="myInput" value="0">
</div>

<!-- Side-by-side inputs -->
<div class="input-row">
    <div class="input-group">
        <label for="width">Width:</label>
        <input type="number" id="width">
    </div>
    <div class="input-group">
        <label for="height">Height:</label>
        <input type="number" id="height">
    </div>
</div>
```

### Checkboxes
```html
<div class="input-group">
    <label class="checkbox-label">
        <input type="checkbox" id="myCheck">
        <span>Checkbox Label Text</span>
    </label>
</div>
```

### Control Sections
```html
<section class="control-section">
    <h3>🎯 Section Title</h3>
    <!-- Section content here -->
</section>
```

### Info Boxes
```html
<!-- General info box -->
<div class="info-box">
    <p>Information message</p>
    <p><strong>Important:</strong> Details here</p>
</div>

<!-- Event hint (orange) -->
<div class="event-hint">
    📍 <strong>Click to select</strong><br>
    Additional instruction
</div>

<!-- Event preview -->
<div class="event-preview">
    <strong>Preview:</strong> <span id="previewText"></span>
</div>
```

### Statistics Cards
```html
<div class="stat-card">
    <div class="stat-icon">⏱️</div>
    <div class="stat-content">
        <div class="stat-label">Time</div>
        <div class="stat-value"><span id="stat-time">0.0</span>s</div>
    </div>
</div>

<!-- Active card (green border) -->
<div class="stat-card active">...</div>

<!-- Panic card (orange border) -->
<div class="stat-card panic">...</div>
```

### Mode Selector (Drawing Tools)
```html
<div class="mode-selector">
    <button class="mode-btn active" onclick="setMode('wall')">
        🧱 墙体<br><span class="small">Wall</span>
    </button>
    <button class="mode-btn" onclick="setMode('entrance')">
        📥 入口<br><span class="small">Entrance</span>
    </button>
</div>
```

### Legend Items
```html
<div class="legend">
    <div class="legend-item">
        <div class="legend-color" style="background: #10b981;"></div>
        <span>入口 Entrance</span>
    </div>
    <div class="legend-item">
        <div class="legend-color" style="background: linear-gradient(135deg, #ef4444, #dc2626);"></div>
        <span>出口 Exit</span>
    </div>
</div>
```

## Bilingual Text Format

Always include both Chinese and English:

```html
<!-- Headers -->
<h3>🎬 预置场景 Preset Scenarios</h3>

<!-- Labels -->
<label>宽度 Width (m):</label>

<!-- Buttons -->
<button>▶️ 开始 Start</button>

<!-- Options -->
<option value="random">🎲 随机 Random</option>
```

## Icon Usage

Use emoji icons consistently:

```
🚶 Pedestrian/General
🎬 Scenarios
🗺️ Scene/Map
🎨 Drawing/Tools
🧱 Wall
📥 Entrance (In)
📤 Exit (Out)
🗑️ Clear/Delete
⚙️ Settings/Control
⚡ Emergency/Event
🔥 Fire
🔫 Shooting
🚫 Block
📊 Statistics
⏱️ Time
👥 People/Active
➕ Add/Spawned
✅ Complete/Exited
😱 Panic
💾 Save/Export
📦 Package/Unity
ℹ️ Information
📍 Location
```

## Layout Structure

```html
<div class="app-container">
    <header>
        <div class="header-content">
            <h1>Title</h1>
            <p class="subtitle">Subtitle</p>
        </div>
    </header>
    
    <div class="main-content">
        <!-- Left Sidebar -->
        <aside class="sidebar left-sidebar">
            <section class="control-section">...</section>
        </aside>
        
        <!-- Canvas Area -->
        <div class="canvas-area">
            <div class="toolbar">...</div>
            <div class="canvas-wrapper">
                <canvas id="simulationCanvas"></canvas>
            </div>
        </div>
        
        <!-- Right Sidebar -->
        <aside class="sidebar right-sidebar">
            <section class="control-section">...</section>
        </aside>
    </div>
</div>
```

## Responsive Breakpoints

```css
/* Large screens (default): 1600px+ */
.left-sidebar { width: 340px; }
.right-sidebar { width: 300px; }
#simulationCanvas { width: 800px; height: 800px; }

/* Medium screens: ≤1600px */
@media (max-width: 1600px) {
    .left-sidebar { width: 300px; }
    .right-sidebar { width: 280px; }
    #simulationCanvas { width: 700px; height: 700px; }
}

/* Smaller screens: ≤1400px */
@media (max-width: 1400px) {
    .left-sidebar { width: 280px; }
    .right-sidebar { width: 260px; }
    #simulationCanvas { width: 600px; height: 600px; }
}
```

## Common Patterns

### Button Group (3 columns)
```html
<div class="button-group">
    <button class="btn btn-success">Start</button>
    <button class="btn btn-danger">Stop</button>
    <button class="btn btn-warning">Reset</button>
</div>
```

### Styled Select
```html
<select class="styled-select">
    <option value="">-- Choose --</option>
    <option value="1">Option 1</option>
</select>
```

### Readonly Input
```html
<input type="number" id="eventX" readonly>
/* Automatically styled with readonly state */
```

## JavaScript Integration

The CSS is designed to work seamlessly with existing JavaScript:

```javascript
// Toggle active state on mode buttons
function setTool(tool) {
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    event.target.classList.add('active');
}

// Show/hide sections
element.style.display = 'none';  // Hide
element.style.display = 'block'; // Show

// Update stat values
document.getElementById('stat-time').textContent = time.toFixed(1);
```

## Color Combinations Guide

### Success Actions
```css
background: linear-gradient(135deg, #00d4aa, #00a884);
color: white;
```

### Danger Actions
```css
background: linear-gradient(135deg, #ff6b6b, #ee5a52);
color: white;
```

### Warning Actions
```css
background: linear-gradient(135deg, #ffa500, #ff8c00);
color: white;
```

### Primary Actions
```css
background: linear-gradient(135deg, #e94560, #c13854);
color: white;
```

## Spacing System

```css
/* Consistent spacing */
.control-section { margin-bottom: 25px; padding-bottom: 20px; }
.input-group { margin-bottom: 15px; }
.sidebar { padding: 20px; }
.toolbar { padding: 15px 20px; }
.canvas-wrapper { padding: 20px; }

/* Gaps */
.mode-selector { gap: 10px; }
.stats-panel { gap: 12px; }
.legend { gap: 12px; }
```

## Border Radius System

```css
/* Small: 6px - inputs, buttons */
border-radius: 6px;

/* Medium: 8px - canvas, mode buttons, cards */
border-radius: 8px;

/* Large: 10px - stat cards */
border-radius: 10px;
```

## Transition Guidelines

```css
/* Standard transition for most elements */
transition: all 0.3s;

/* Hover transforms */
.btn:hover { transform: translateY(-2px); }
.stat-card:hover { transform: translateX(5px); }
.mode-btn.active { transform: scale(1.05); }
```

## Debugging Tips

1. **Check variable usage**: Ensure all colors use CSS variables
2. **Verify bilingual text**: Both languages should be present
3. **Test responsiveness**: Check at 1400px and 1600px breakpoints
4. **Validate contrast**: Ensure text is readable on backgrounds
5. **Check hover states**: All interactive elements should have feedback

## Common Customizations

### Change accent color globally
```css
:root {
    --accent-color: #your-color;
}
```

### Adjust sidebar width
```css
.left-sidebar {
    width: 360px; /* Your preferred width */
}
```

### Modify stat card size
```css
.stat-value {
    font-size: 32px; /* Larger values */
}
```

## Best Practices

1. ✅ Always use CSS variables for colors
2. ✅ Include bilingual text (Chinese + English)
3. ✅ Add emoji icons for visual clarity
4. ✅ Use semantic HTML5 elements
5. ✅ Maintain consistent spacing
6. ✅ Apply proper hover/focus states
7. ✅ Test on different screen sizes
8. ✅ Keep accessibility in mind

## File Organization

```
ped_sim2/
├── src/
│   └── web/
│       ├── templates/
│       │   └── index.html        (Main HTML structure)
│       └── static/
│           ├── style.css         (All styling - redesigned)
│           └── app.js            (JavaScript - unchanged)
└── UI_REDESIGN.md               (This documentation)
```

## Quick Start for Developers

1. **Reference the HTML**: Use `index.html` as template for structure
2. **Use CSS variables**: Never hardcode colors
3. **Follow patterns**: Copy existing component patterns
4. **Test responsively**: Check multiple screen sizes
5. **Maintain bilingual**: Always include both languages

## Need Help?

- Check `UI_REDESIGN.md` for detailed changes
- See `UI_COMPARISON.md` for before/after comparisons
- Reference `pedestrian_simulation/server/templates/editor.html` for inspiration
