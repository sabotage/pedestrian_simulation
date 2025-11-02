// Pedestrian Simulation Web Application
const socket = io();

// Canvas and rendering
const canvas = document.getElementById('simulationCanvas');
const ctx = canvas.getContext('2d');

// State
let currentTool = 'wall';
let environment = {
    width: 50,
    height: 50,
    walls: [],
    entrances: [],
    exits: [],
    trafficLights: [],
    crossingLanes: [],
    roads: [],
    decorations: []
};

let drawingWall = false;
let wallStart = null;

// Traffic light state
let trafficLightStates = {}; // id -> {state: 'red'|'green', timer: number}
let trafficLightCycle = 20; // seconds per cycle (changed to 20)
let greenLightDuration = 10; // seconds (half of cycle)

// Event selection mode
let eventSelectionMode = false;
let selectedEventPosition = null;
let eventPreviewRadius = 10;

// Current simulation state
let currentSimulationState = {
    time: 0,
    pedestrians: [],
    stats: {}
};

// Preset scenarios data
let scenariosData = {};

// Isometric view settings
let isometricView = true; // Toggle for isometric view
const isoAngle = Math.PI / 6; // 30 degrees for isometric
const isoScale = 0.86; // Isometric scaling factor

// Helper function to calculate proper scale for isometric view
function calculateScale() {
    if (isometricView) {
        // For isometric view, we need more space due to diagonal projection
        return Math.min(
            canvas.width / (environment.width * 1.8),
            canvas.height / (environment.height * 1.2)
        );
    }
    return canvas.width / environment.width;
}

// Scale factor for canvas rendering
let scale = calculateScale();

// Convert world coordinates to isometric screen coordinates
function toIso(x, y, z = 0) {
    if (!isometricView) {
        return { x: x * scale, y: y * scale };
    }
    
    // Center the map based on environment size
    const centerX = environment.width / 2;
    const centerY = environment.height / 2;
    
    // Isometric projection from world center
    const isoX = ((x - centerX) - (y - centerY)) * Math.cos(isoAngle);
    const isoY = ((x - centerX) + (y - centerY)) * Math.sin(isoAngle) - z;
    
    return {
        x: canvas.width / 2 + isoX * scale * isoScale,
        y: canvas.height / 2 + isoY * scale * isoScale * 0.7
    };
}

// Convert isometric back to world coordinates (for mouse clicks)
function fromIso(screenX, screenY) {
    if (!isometricView) {
        return { x: screenX / scale, y: screenY / scale };
    }
    
    const centerX = environment.width / 2;
    const centerY = environment.height / 2;
    
    const isoX = (screenX - canvas.width / 2) / (scale * isoScale);
    const isoY = (screenY - canvas.height / 2) / (scale * isoScale * 0.7);
    
    const x = (isoX / Math.cos(isoAngle) + isoY / Math.sin(isoAngle)) / 2 + centerX;
    const y = (isoY / Math.sin(isoAngle) - isoX / Math.cos(isoAngle)) / 2 + centerY;
    
    return { x, y };
}

// Load scenarios index on page load
window.addEventListener('DOMContentLoaded', () => {
    fetch('/api/scenarios')
        .then(response => response.json())
        .then(data => {
            scenariosData = data;
            console.log('Loaded scenarios:', Object.keys(scenariosData));
            
            // Populate scenario dropdown dynamically
            const select = document.getElementById('presetScenario');
            if (select) {
                // Clear existing options except the first one
                while (select.options.length > 1) {
                    select.remove(1);
                }
                
                // Add options for each scenario
                Object.keys(scenariosData).forEach(scenarioId => {
                    const scenario = scenariosData[scenarioId];
                    const option = document.createElement('option');
                    option.value = scenarioId;
                    option.textContent = scenario.name_en || scenario.name || scenarioId;
                    select.appendChild(option);
                });
                
                console.log('Populated scenario dropdown with', select.options.length - 1, 'scenarios');
            }
        })
        .catch(error => {
            console.error('Error loading scenarios:', error);
        });
    
    // Setup event input listeners
    const immediateCheckbox = document.getElementById('immediateEvent');
    if (immediateCheckbox) {
        immediateCheckbox.addEventListener('change', updateEventInputs);
    }
    
    const eventRadiusInput = document.getElementById('eventRadius');
    if (eventRadiusInput) {
        eventRadiusInput.addEventListener('change', (e) => {
            eventPreviewRadius = Number.parseFloat(e.target.value);
            updateEventPreview();
            if (selectedEventPosition) {
                drawEnvironment();
                drawEventPreview(selectedEventPosition[0], selectedEventPosition[1]);
            }
        });
    }
    
    const eventTypeSelect = document.getElementById('eventType');
    if (eventTypeSelect) {
        eventTypeSelect.addEventListener('change', (e) => {
            const eventType = e.target.value;
            
            if (eventType === 'fire' || eventType === 'shooting') {
                eventSelectionMode = true;
                eventPreviewRadius = Number.parseFloat(document.getElementById('eventRadius').value);
                canvas.style.cursor = 'crosshair'; // Change cursor to crosshair
            } else {
                eventSelectionMode = false;
                selectedEventPosition = null;
                canvas.style.cursor = 'default'; // Reset cursor
            }
            
            updateEventInputs();
            updateEventPreview();
            drawEnvironment();
        });
        
        // Trigger initial setup
        eventSelectionMode = true; // Enable by default for fire
        canvas.style.cursor = 'crosshair'; // Set cursor for event selection
    }
    
    // Initialize event inputs
    updateEventInputs();
});

// Load preset scenario
function loadPresetScenario() {
    const select = document.getElementById('presetScenario');
    const scenarioId = select.value;
    
    if (!scenarioId) {
        document.getElementById('scenarioInfo').style.display = 'none';
        return;
    }
    
    const scenario = scenariosData[scenarioId];
    if (!scenario) {
        alert('Scenario not found: ' + scenarioId);
        return;
    }
    
    // Display scenario info
    document.getElementById('scenarioDescription').textContent = scenario.description_en || scenario.description;
    document.getElementById('scenarioRecommendedPeds').textContent = scenario.recommended_pedestrians;
    document.getElementById('scenarioInfo').style.display = 'block';
    
    // Auto-fill recommended pedestrian count
    document.getElementById('numPedestrians').value = scenario.recommended_pedestrians;
    
    // Convert scenario environment format to our format
    const scenarioEnv = scenario.environment;
    environment = {
        width: scenarioEnv.width,
        height: scenarioEnv.height,
        walls: scenarioEnv.walls.map(w => ({ start: w[0], end: w[1] })),
        entrances: scenarioEnv.entrances || [],
        exits: scenarioEnv.exits || [],
        roads: scenarioEnv.roads || [],
        decorations: scenarioEnv.decorations || [],
        trafficLights: scenarioEnv.trafficLights || [],
        crossingLanes: scenarioEnv.crossingLanes || []
    };
    
    scale = calculateScale();
    
    // Update width/height inputs
    document.getElementById('envWidth').value = environment.width;
    document.getElementById('envHeight').value = environment.height;
    
    // Draw the environment immediately
    drawEnvironment();
    
    // Notify server to create simulator with this scenario
    socket.emit('load_scenario', { scenario_id: scenarioId });
    
    console.log(`Loaded scenario: ${scenario.name_en || scenario.name}`);
    console.log(`Environment loaded: ${environment.walls.length} walls, ${environment.entrances.length} entrances, ${environment.exits.length} exits, ${environment.roads?.length || 0} roads, ${environment.decorations?.length || 0} decorations`);
}

// Socket.IO event handlers
socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('environment_created', (data) => {
    if (data.status === 'success') {
        console.log('Environment created successfully');
        environment = data.environment;
        scale = calculateScale();
        drawEnvironment();
    } else {
        alert('Error creating environment: ' + data.message);
    }
});

socket.on('simulation_update', (state) => {
    currentSimulationState = state; // Save current state
    console.log('Received state:', {
        time: state.time,
        pedestrianCount: state.pedestrians ? state.pedestrians.length : 0,
        firstPed: state.pedestrians && state.pedestrians[0] ? state.pedestrians[0] : null
    });
    updateTrafficLights(state.time);
    updateVisualization(state);
    updateStatistics(state);
});

socket.on('simulation_started', (data) => {
    console.log('Simulation started');
    document.getElementById('btn-start').disabled = true;
    document.getElementById('btn-stop').disabled = false;
});

socket.on('simulation_stopped', (data) => {
    console.log('Simulation stopped:', data.reason);
    document.getElementById('btn-start').disabled = false;
    document.getElementById('btn-stop').disabled = true;
    if (data.stats) {
        alert(`Simulation stopped: ${data.reason}\nTotal spawned: ${data.stats.spawned}\nExited: ${data.stats.exited}`);
    }
});

socket.on('simulation_reset', (data) => {
    console.log('Simulation reset');
    drawEnvironment();
    resetStatistics();
});

socket.on('event_added', (data) => {
    console.log('Event added:', data.type, 'at time', data.trigger_time);
    alert(`Event "${data.type}" scheduled for ${data.trigger_time.toFixed(1)}s`);
});

socket.on('export_complete', (data) => {
    alert(`Export successful!\nFile saved to: ${data.filepath}`);
});

socket.on('simulation_error', (data) => {
    console.error('Simulation error:', data.message);
    alert(`Simulation Error: ${data.message}`);
    document.getElementById('btn-start').disabled = false;
    document.getElementById('btn-stop').disabled = true;
});

socket.on('scenario_loaded', (data) => {
    if (data.status === 'success') {
        console.log('Scenario loaded on server');
        
        // Convert environment from server to our format
        const serverEnv = data.environment;
        environment = {
            width: serverEnv.width,
            height: serverEnv.height,
            walls: serverEnv.walls.map(w => ({ start: w[0], end: w[1] })),
            entrances: serverEnv.entrances || [],
            exits: serverEnv.exits || [],
            roads: serverEnv.roads || [],
            decorations: serverEnv.decorations || [],
            trafficLights: serverEnv.trafficLights || [],
            crossingLanes: serverEnv.crossingLanes || []
        };
        
        // Initialize traffic light states from scenario (FROZEN for debugging)
        trafficLightStates = {};
        if (environment.trafficLights) {
            environment.trafficLights.forEach(light => {
                trafficLightStates[light.id] = {
                    state: light.state || 'red',  // Use initial state from scenario
                    lastChange: 0
                };
                console.log(`Initialized traffic light ${light.id} to ${light.state}`);
            });
        }
        
        scale = calculateScale();
        
        // Redraw the environment
        drawEnvironment();
        
        // Enable start button
        document.getElementById('btn-start').disabled = false;
        
        // Show success message
        const scenario = data.scenario;
        alert(`✅ Scenario Ready!\n\n${scenario.name_en || scenario.name}\n\n${scenario.description_en || scenario.description}\n\nRecommended: ${scenario.recommended_pedestrians} pedestrians\n\nClick START to begin simulation!`);
        
        console.log(`Server confirmed: ${environment.walls.length} walls, ${environment.entrances.length} entrances, ${environment.exits.length} exits, ${environment.roads?.length || 0} roads, ${environment.decorations?.length || 0} decorations`);
    } else {
        alert('Error loading scenario');
    }
});

socket.on('scenario_error', (data) => {
    alert(`Error loading scenario: ${data.message}`);
});

// Tool selection
function setTool(tool) {
    currentTool = tool;
    
    // Update button states
    document.querySelectorAll('.tool-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const btnId = 'btn-' + tool;
    const btn = document.getElementById(btnId);
    if (btn) {
        btn.classList.add('active');
    }
}

// Canvas mouse events
canvas.addEventListener('mousedown', (e) => {
    const rect = canvas.getBoundingClientRect();
    const screenX = e.clientX - rect.left;
    const screenY = e.clientY - rect.top;
    const worldCoords = fromIso(screenX, screenY);
    const x = worldCoords.x;
    const y = worldCoords.y;
    
    // Event selection mode - select position for event
    if (eventSelectionMode) {
        selectedEventPosition = [x, y];
        document.getElementById('eventX').value = x.toFixed(1);
        document.getElementById('eventY').value = y.toFixed(1);
        
        // Update preview
        updateEventPreview();
        
        // Redraw with preview
        drawEnvironment();
        drawEventPreview(x, y);
        
        return;
    }
    
    if (currentTool === 'wall') {
        if (!drawingWall) {
            wallStart = [x, y];
            drawingWall = true;
        } else {
            environment.walls.push({
                start: wallStart,
                end: [x, y]
            });
            drawingWall = false;
            wallStart = null;
            drawEnvironment();
        }
    } else if (currentTool === 'entrance') {
        const radius = parseFloat(document.getElementById('entranceRadius').value);
        const flowRate = parseFloat(document.getElementById('flowRate').value);
        environment.entrances.push({
            position: [x, y],
            radius: radius,
            flow_rate: flowRate
        });
        drawEnvironment();
    } else if (currentTool === 'exit') {
        environment.exits.push({
            position: [x, y],
            radius: 1.5
        });
        drawEnvironment();
    } else if (currentTool === 'clear') {
        // Find and remove nearest element
        clearNearest(x, y);
    }
});

canvas.addEventListener('mousemove', (e) => {
    const rect = canvas.getBoundingClientRect();
    const screenX = e.clientX - rect.left;
    const screenY = e.clientY - rect.top;
    const worldCoords = fromIso(screenX, screenY);
    
    if (drawingWall && wallStart) {
        // Redraw with temporary wall
        drawEnvironment();
        const p1 = toIso(wallStart[0], wallStart[1], 0);
        const p2 = toIso(worldCoords.x, worldCoords.y, 0);
        ctx.strokeStyle = '#667eea';
        ctx.lineWidth = 3;
        ctx.setLineDash([5, 5]);
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.stroke();
        ctx.setLineDash([]);
    } else if (eventSelectionMode) {
        // Show preview of event position while hovering
        drawEnvironment();
        if (selectedEventPosition) {
            drawEventPreview(selectedEventPosition[0], selectedEventPosition[1]);
        }
        // Draw hover preview
        drawEventPreview(worldCoords.x, worldCoords.y);
    }
});

function clearNearest(x, y) {
    let minDist = Infinity;
    let toRemove = null;
    let type = null;
    
    // Check walls
    environment.walls.forEach((wall, idx) => {
        const midX = (wall.start[0] + wall.end[0]) / 2;
        const midY = (wall.start[1] + wall.end[1]) / 2;
        const dist = Math.sqrt((x - midX)**2 + (y - midY)**2);
        if (dist < minDist) {
            minDist = dist;
            toRemove = idx;
            type = 'wall';
        }
    });
    
    // Check entrances
    environment.entrances.forEach((ent, idx) => {
        const dist = Math.sqrt((x - ent.position[0])**2 + (y - ent.position[1])**2);
        if (dist < minDist) {
            minDist = dist;
            toRemove = idx;
            type = 'entrance';
        }
    });
    
    // Check exits
    environment.exits.forEach((exit, idx) => {
        const dist = Math.sqrt((x - exit.position[0])**2 + (y - exit.position[1])**2);
        if (dist < minDist) {
            minDist = dist;
            toRemove = idx;
            type = 'exit';
        }
    });
    
    // Remove if close enough (within 2 meters)
    if (minDist < 2.0 && toRemove !== null) {
        if (type === 'wall') {
            environment.walls.splice(toRemove, 1);
        } else if (type === 'entrance') {
            environment.entrances.splice(toRemove, 1);
        } else if (type === 'exit') {
            environment.exits.splice(toRemove, 1);
        }
        drawEnvironment();
    }
}

// Drawing helper functions for beautiful 2D game-like graphics
function drawGrass(x, y, size) {
    // Draw grass pattern
    const grassColors = ['#6b9244', '#7ba34e', '#8ab558'];
    ctx.fillStyle = grassColors[Math.floor(Math.random() * grassColors.length)];
    for (let i = 0; i < 3; i++) {
        const offsetX = (Math.random() - 0.5) * size;
        const offsetY = (Math.random() - 0.5) * size;
        ctx.fillRect(x + offsetX, y + offsetY, 2, 6);
    }
}

function drawTree(x, y, size) {
    // Draw trunk
    const trunkWidth = size * 0.3;
    const trunkHeight = size * 0.6;
    ctx.fillStyle = '#8B4513';
    ctx.fillRect(x - trunkWidth/2, y - trunkHeight/2, trunkWidth, trunkHeight);
    
    // Draw foliage (3 circles for leafy effect)
    const foliageRadius = size * 0.5;
    const gradient = ctx.createRadialGradient(x, y - size * 0.4, 0, x, y - size * 0.4, foliageRadius);
    gradient.addColorStop(0, '#4a9d4f');
    gradient.addColorStop(0.7, '#3d8b40');
    gradient.addColorStop(1, '#2d6b30');
    ctx.fillStyle = gradient;
    
    ctx.beginPath();
    ctx.arc(x - foliageRadius * 0.3, y - size * 0.5, foliageRadius * 0.8, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x + foliageRadius * 0.3, y - size * 0.5, foliageRadius * 0.8, 0, Math.PI * 2);
    ctx.fill();
    ctx.beginPath();
    ctx.arc(x, y - size * 0.7, foliageRadius, 0, Math.PI * 2);
    ctx.fill();
}

function drawRoad(x1, y1, x2, y2, width) {
    // Calculate perpendicular for road width
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.sqrt(dx * dx + dy * dy);
    const perpX = -dy / len * width / 2;
    const perpY = dx / len * width / 2;
    
    // Draw road base
    const gradient = ctx.createLinearGradient(x1 + perpX, y1 + perpY, x1 - perpX, y1 - perpY);
    gradient.addColorStop(0, '#505050');
    gradient.addColorStop(0.5, '#606060');
    gradient.addColorStop(1, '#505050');
    ctx.fillStyle = gradient;
    
    ctx.beginPath();
    ctx.moveTo(x1 + perpX, y1 + perpY);
    ctx.lineTo(x2 + perpX, y2 + perpY);
    ctx.lineTo(x2 - perpX, y2 - perpY);
    ctx.lineTo(x1 - perpX, y1 - perpY);
    ctx.closePath();
    ctx.fill();
    
    // Draw center line (dashed)
    ctx.strokeStyle = '#ffeb3b';
    ctx.lineWidth = 2;
    ctx.setLineDash([10, 10]);
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
    ctx.setLineDash([]);
}

function drawBrickWall(x1, y1, x2, y2, thickness) {
    const dx = x2 - x1;
    const dy = y2 - y1;
    const len = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx);
    
    ctx.save();
    ctx.translate(x1, y1);
    ctx.rotate(angle);
    
    // Draw wall base with gradient
    const gradient = ctx.createLinearGradient(0, -thickness/2, 0, thickness/2);
    gradient.addColorStop(0, '#8B4513');
    gradient.addColorStop(0.5, '#A0522D');
    gradient.addColorStop(1, '#8B4513');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, -thickness/2, len, thickness);
    
    // Draw brick pattern
    ctx.strokeStyle = '#654321';
    ctx.lineWidth = 1;
    const brickWidth = 20;
    const brickHeight = thickness / 2;
    
    for (let x = 0; x < len; x += brickWidth) {
        for (let y = -thickness/2; y < thickness/2; y += brickHeight) {
            ctx.strokeRect(x, y, brickWidth, brickHeight);
        }
    }
    
    // Add 3D effect
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.lineWidth = 2;
    ctx.strokeRect(0, -thickness/2, len, thickness);
    
    ctx.restore();
}

function drawPool(x, y, width, height) {
    // Draw pool with water effect
    const gradient = ctx.createRadialGradient(x + width/2, y + height/2, 0, x + width/2, y + height/2, width/2);
    gradient.addColorStop(0, '#4fc3f7');
    gradient.addColorStop(0.5, '#29b6f6');
    gradient.addColorStop(1, '#039be5');
    
    ctx.fillStyle = gradient;
    ctx.fillRect(x, y, width, height);
    
    // Add water ripples
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 2;
    for (let i = 0; i < 3; i++) {
        const offset = i * 10;
        ctx.beginPath();
        ctx.arc(x + width/2, y + height/2, 20 + offset, 0, Math.PI * 2);
        ctx.stroke();
    }
    
    // Pool border
    ctx.strokeStyle = '#0277bd';
    ctx.lineWidth = 3;
    ctx.strokeRect(x, y, width, height);
}

function drawFlower(x, y, size) {
    // Draw flower petals
    const petalColors = ['#ff69b4', '#ff1493', '#ff6eb4', '#ffc0cb'];
    ctx.fillStyle = petalColors[Math.floor(Math.random() * petalColors.length)];
    
    for (let i = 0; i < 5; i++) {
        const angle = (i / 5) * Math.PI * 2;
        const petalX = x + Math.cos(angle) * size * 0.5;
        const petalY = y + Math.sin(angle) * size * 0.5;
        ctx.beginPath();
        ctx.arc(petalX, petalY, size * 0.3, 0, Math.PI * 2);
        ctx.fill();
    }
    
    // Draw center
    ctx.fillStyle = '#ffd700';
    ctx.beginPath();
    ctx.arc(x, y, size * 0.25, 0, Math.PI * 2);
    ctx.fill();
}

function drawBush(x, y, size) {
    // Draw decorative bush
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, size);
    gradient.addColorStop(0, '#90c695');
    gradient.addColorStop(0.7, '#6ba56a');
    gradient.addColorStop(1, '#4a8049');
    ctx.fillStyle = gradient;
    
    // Multiple circles for bushy effect
    for (let i = 0; i < 3; i++) {
        const offsetX = (Math.random() - 0.5) * size * 0.5;
        const offsetY = (Math.random() - 0.5) * size * 0.5;
        ctx.beginPath();
        ctx.arc(x + offsetX, y + offsetY, size * 0.6, 0, Math.PI * 2);
        ctx.fill();
    }
}

function drawTrafficLight(x, y, state, orientation = 'vertical') {
    const width = 20;
    const height = 50;
    
    // Traffic light pole
    ctx.fillStyle = '#424242';
    if (orientation === 'vertical') {
        ctx.fillRect(x - 3, y, 6, height + 20);
        // Light box
        ctx.fillStyle = '#212121';
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.fillRect(x - width/2, y, width, height);
        ctx.strokeRect(x - width/2, y, width, height);
    } else {
        ctx.fillRect(x, y - 3, height + 20, 6);
        // Light box
        ctx.fillStyle = '#212121';
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.fillRect(x, y - width/2, height, width);
        ctx.strokeRect(x, y - width/2, height, width);
    }
    
    // Lights
    const redY = orientation === 'vertical' ? y + 10 : y;
    const redX = orientation === 'vertical' ? x : x + 10;
    const greenY = orientation === 'vertical' ? y + 35 : y;
    const greenX = orientation === 'vertical' ? x : x + 35;
    
    // Red light
    if (state === 'red') {
        const redGradient = ctx.createRadialGradient(redX, redY, 0, redX, redY, 6);
        redGradient.addColorStop(0, '#ff0000');
        redGradient.addColorStop(0.5, '#cc0000');
        redGradient.addColorStop(1, '#990000');
        ctx.fillStyle = redGradient;
    } else {
        ctx.fillStyle = '#4d0000';
    }
    ctx.beginPath();
    ctx.arc(redX, redY, 6, 0, Math.PI * 2);
    ctx.fill();
    
    // Green light
    if (state === 'green') {
        const greenGradient = ctx.createRadialGradient(greenX, greenY, 0, greenX, greenY, 6);
        greenGradient.addColorStop(0, '#00ff00');
        greenGradient.addColorStop(0.5, '#00cc00');
        greenGradient.addColorStop(1, '#009900');
        ctx.fillStyle = greenGradient;
    } else {
        ctx.fillStyle = '#004d00';
    }
    ctx.beginPath();
    ctx.arc(greenX, greenY, 6, 0, Math.PI * 2);
    ctx.fill();
}

function drawCrossingLane(x1, y1, x2, y2, width) {
    // Draw zebra crossing stripes
    const dx = x2 - x1;
    const dy = y2 - y1;
    const length = Math.sqrt(dx * dx + dy * dy);
    const angle = Math.atan2(dy, dx);
    
    ctx.save();
    ctx.translate(x1, y1);
    ctx.rotate(angle);
    
    // Background
    ctx.fillStyle = '#e0e0e0';
    ctx.fillRect(0, -width/2, length, width);
    
    // White stripes
    ctx.fillStyle = '#ffffff';
    const stripeWidth = 8;
    const stripeGap = 8;
    for (let i = 0; i < length; i += stripeWidth + stripeGap) {
        ctx.fillRect(i, -width/2, stripeWidth, width);
    }
    
    // Border lines
    ctx.strokeStyle = '#424242';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, -width/2);
    ctx.lineTo(length, -width/2);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(0, width/2);
    ctx.lineTo(length, width/2);
    ctx.stroke();
    
    ctx.restore();
}

// Isometric drawing functions
function drawIsoWall(x1, y1, x2, y2, height) {
    const p1 = toIso(x1, y1, 0);
    const p2 = toIso(x2, y2, 0);
    const p3 = toIso(x2, y2, height);
    const p4 = toIso(x1, y1, height);
    
    // Draw wall face with gradient for 3D effect
    const gradient = ctx.createLinearGradient(p1.x, p1.y, p4.x, p4.y);
    gradient.addColorStop(0, '#8b6f47');
    gradient.addColorStop(0.5, '#a0826d');
    gradient.addColorStop(1, '#6b5744');
    ctx.fillStyle = gradient;
    
    ctx.beginPath();
    ctx.moveTo(p1.x, p1.y);
    ctx.lineTo(p2.x, p2.y);
    ctx.lineTo(p3.x, p3.y);
    ctx.lineTo(p4.x, p4.y);
    ctx.closePath();
    ctx.fill();
    
    // Add brick texture
    ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.lineWidth = 1;
    const steps = Math.sqrt(Math.pow(x2 - x1, 2) + Math.pow(y2 - y1, 2)) / 2;
    for (let i = 0; i < steps; i++) {
        const t = i / steps;
        const px1 = toIso(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, height * 0.5);
        const px2 = toIso(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t, 0);
        ctx.beginPath();
        ctx.moveTo(px1.x, px1.y);
        ctx.lineTo(px2.x, px2.y);
        ctx.stroke();
    }
    
    // Top edge highlight
    ctx.strokeStyle = '#b8a894';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(p4.x, p4.y);
    ctx.lineTo(p3.x, p3.y);
    ctx.stroke();
}

function drawIsoEntrance(x, y, radius, flowRate) {
    const p = toIso(x, y, 0);
    const r = radius * scale * isoScale;
    
    // Draw 3D platform base
    const pts = [];
    for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 8) {
        const px = x + Math.cos(angle) * radius;
        const py = y + Math.sin(angle) * radius;
        pts.push(toIso(px, py, 0));
    }
    
    // Platform shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < pts.length; i++) {
        ctx.lineTo(pts[i].x, pts[i].y);
    }
    ctx.closePath();
    ctx.fill();
    
    // Platform with gradient
    const gradient = ctx.createRadialGradient(p.x, p.y - r * 0.3, 0, p.x, p.y, r);
    gradient.addColorStop(0, '#66bb6a');
    gradient.addColorStop(0.7, '#43a047');
    gradient.addColorStop(1, '#2e7d32');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
    ctx.fill();
    
    // Border
    ctx.strokeStyle = '#1b5e20';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Icon
    ctx.fillStyle = '#fff';
    ctx.font = `bold ${r * 0.8}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('↓', p.x, p.y);
    
    // Flow rate label
    if (flowRate) {
        ctx.fillStyle = '#1b5e20';
        ctx.font = `bold ${r * 0.4}px Arial`;
        ctx.fillText(flowRate.toFixed(1) + '/s', p.x, p.y + r + 10);
    }
}

function drawIsoExit(x, y, radius) {
    const p = toIso(x, y, 0);
    const r = radius * scale * isoScale;
    
    // Draw 3D platform base
    const pts = [];
    for (let angle = 0; angle < Math.PI * 2; angle += Math.PI / 8) {
        const px = x + Math.cos(angle) * radius;
        const py = y + Math.sin(angle) * radius;
        pts.push(toIso(px, py, 0));
    }
    
    // Platform shadow
    ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
    ctx.beginPath();
    ctx.moveTo(pts[0].x, pts[0].y);
    for (let i = 1; i < pts.length; i++) {
        ctx.lineTo(pts[i].x, pts[i].y);
    }
    ctx.closePath();
    ctx.fill();
    
    // Platform with gradient
    const gradient = ctx.createRadialGradient(p.x, p.y - r * 0.3, 0, p.x, p.y, r);
    gradient.addColorStop(0, '#ef5350');
    gradient.addColorStop(0.7, '#e53935');
    gradient.addColorStop(1, '#c62828');
    ctx.fillStyle = gradient;
    ctx.beginPath();
    ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
    ctx.fill();
    
    // Border
    ctx.strokeStyle = '#b71c1c';
    ctx.lineWidth = 2;
    ctx.stroke();
    
    // Icon
    ctx.fillStyle = '#fff';
    ctx.font = `bold ${r * 0.8}px Arial`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('↑', p.x, p.y);
}

function drawIsoCrossingLane(x1, y1, x2, y2, width) {
    // Draw zebra crossing in isometric view
    const segments = 10;
    const dx = (x2 - x1) / segments;
    const dy = (y2 - y1) / segments;
    
    for (let i = 0; i < segments; i++) {
        const wx1 = x1 + dx * i;
        const wy1 = y1 + dy * i;
        const wx2 = x1 + dx * (i + 0.45);
        const wy2 = y1 + dy * (i + 0.45);
        
        // Calculate perpendicular offset
        const angle = Math.atan2(dy, dx);
        const perpX = Math.cos(angle + Math.PI / 2) * width / 2;
        const perpY = Math.sin(angle + Math.PI / 2) * width / 2;
        
        // Draw white stripe
        const p1 = toIso(wx1 + perpX, wy1 + perpY, 0);
        const p2 = toIso(wx2 + perpX, wy2 + perpY, 0);
        const p3 = toIso(wx2 - perpX, wy2 - perpY, 0);
        const p4 = toIso(wx1 - perpX, wy1 - perpY, 0);
        
        ctx.fillStyle = i % 2 === 0 ? '#ffffff' : '#e0e0e0';
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.lineTo(p3.x, p3.y);
        ctx.lineTo(p4.x, p4.y);
        ctx.closePath();
        ctx.fill();
    }
}

function drawIsoTrafficLight(x, y, state, orientation) {
    const poleHeight = 4.5;
    const pBase = toIso(x, y, 0);
    const pTop = toIso(x, y, poleHeight);
    
    // Draw pole shadow on ground
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.beginPath();
    ctx.arc(pBase.x, pBase.y, 8, 0, Math.PI * 2);
    ctx.fill();
    
    // Draw pole (thicker and more visible)
    ctx.strokeStyle = '#2c2c2c';
    ctx.lineWidth = 8;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(pBase.x, pBase.y);
    ctx.lineTo(pTop.x, pTop.y);
    ctx.stroke();
    
    // Draw pole highlight
    ctx.strokeStyle = '#555555';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(pBase.x - 2, pBase.y - 2);
    ctx.lineTo(pTop.x - 2, pTop.y - 2);
    ctx.stroke();
    
    // Draw traffic light housing box (vertical with 3 lights)
    const housingWidth = 1.2;
    const housingHeight = 3.5;
    const housingDepth = 1.0;
    const housingTop = poleHeight;
    
    // Calculate housing corners
    const h1 = toIso(x - housingWidth / 2, y - housingDepth / 2, housingTop);
    const h2 = toIso(x + housingWidth / 2, y - housingDepth / 2, housingTop);
    const h3 = toIso(x + housingWidth / 2, y + housingDepth / 2, housingTop);
    const h4 = toIso(x - housingWidth / 2, y + housingDepth / 2, housingTop);
    const h5 = toIso(x - housingWidth / 2, y - housingDepth / 2, housingTop + housingHeight);
    const h6 = toIso(x + housingWidth / 2, y - housingDepth / 2, housingTop + housingHeight);
    const h7 = toIso(x + housingWidth / 2, y + housingDepth / 2, housingTop + housingHeight);
    const h8 = toIso(x - housingWidth / 2, y + housingDepth / 2, housingTop + housingHeight);
    
    // Housing box - bottom face
    ctx.fillStyle = '#0a0a0a';
    ctx.beginPath();
    ctx.moveTo(h1.x, h1.y);
    ctx.lineTo(h2.x, h2.y);
    ctx.lineTo(h3.x, h3.y);
    ctx.lineTo(h4.x, h4.y);
    ctx.closePath();
    ctx.fill();
    
    // Housing box - left face
    ctx.fillStyle = '#1a1a1a';
    ctx.beginPath();
    ctx.moveTo(h1.x, h1.y);
    ctx.lineTo(h5.x, h5.y);
    ctx.lineTo(h8.x, h8.y);
    ctx.lineTo(h4.x, h4.y);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Housing box - right face
    ctx.fillStyle = '#2d2d2d';
    ctx.beginPath();
    ctx.moveTo(h2.x, h2.y);
    ctx.lineTo(h6.x, h6.y);
    ctx.lineTo(h7.x, h7.y);
    ctx.lineTo(h3.x, h3.y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Housing box - top face
    ctx.fillStyle = '#1f1f1f';
    ctx.beginPath();
    ctx.moveTo(h5.x, h5.y);
    ctx.lineTo(h6.x, h6.y);
    ctx.lineTo(h7.x, h7.y);
    ctx.lineTo(h8.x, h8.y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Draw the three traffic light circles (red on top, yellow middle, green bottom)
    const lightRadius = 0.35;
    const lightSpacing = 1.1;
    
    // Red light (top)
    const redHeight = housingTop + housingHeight - 0.8;
    const redPos = toIso(x, y, redHeight);
    if (state === 'red') {
        // Active red light with glow
        const redGradient = ctx.createRadialGradient(redPos.x, redPos.y, 0, redPos.x, redPos.y, 25);
        redGradient.addColorStop(0, 'rgba(255, 50, 50, 1)');
        redGradient.addColorStop(0.4, 'rgba(255, 0, 0, 0.8)');
        redGradient.addColorStop(1, 'rgba(255, 0, 0, 0)');
        ctx.fillStyle = redGradient;
        ctx.beginPath();
        ctx.arc(redPos.x, redPos.y, 25, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#ff0000';
        ctx.beginPath();
        ctx.arc(redPos.x, redPos.y, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#cc0000';
        ctx.lineWidth = 2;
        ctx.stroke();
    } else {
        // Inactive red light (dark)
        ctx.fillStyle = '#330000';
        ctx.beginPath();
        ctx.arc(redPos.x, redPos.y, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#1a0000';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    
    // Yellow/Amber light (middle) - always off in this simple implementation
    const yellowHeight = housingTop + housingHeight / 2;
    const yellowPos = toIso(x, y, yellowHeight);
    ctx.fillStyle = '#332200';
    ctx.beginPath();
    ctx.arc(yellowPos.x, yellowPos.y, 8, 0, Math.PI * 2);
    ctx.fill();
    ctx.strokeStyle = '#1a1100';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Green light (bottom)
    const greenHeight = housingTop + 0.8;
    const greenPos = toIso(x, y, greenHeight);
    if (state === 'green') {
        // Active green light with glow
        const greenGradient = ctx.createRadialGradient(greenPos.x, greenPos.y, 0, greenPos.x, greenPos.y, 25);
        greenGradient.addColorStop(0, 'rgba(50, 255, 50, 1)');
        greenGradient.addColorStop(0.4, 'rgba(0, 255, 0, 0.8)');
        greenGradient.addColorStop(1, 'rgba(0, 255, 0, 0)');
        ctx.fillStyle = greenGradient;
        ctx.beginPath();
        ctx.arc(greenPos.x, greenPos.y, 25, 0, Math.PI * 2);
        ctx.fill();
        
        ctx.fillStyle = '#00ff00';
        ctx.beginPath();
        ctx.arc(greenPos.x, greenPos.y, 10, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#00cc00';
        ctx.lineWidth = 2;
        ctx.stroke();
    } else {
        // Inactive green light (dark)
        ctx.fillStyle = '#003300';
        ctx.beginPath();
        ctx.arc(greenPos.x, greenPos.y, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = '#001a00';
        ctx.lineWidth = 1;
        ctx.stroke();
    }
    
    // Add shadow text label for identification
    ctx.save();
    ctx.fillStyle = state === 'red' ? '#ff3333' : '#33ff33';
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 3;
    ctx.font = 'bold 14px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const labelPos = toIso(x, y, housingTop + housingHeight + 0.5);
    ctx.strokeText('🚦', labelPos.x, labelPos.y);
    ctx.fillText('🚦', labelPos.x, labelPos.y);
    ctx.restore();
}

// Draw isometric road segment
function drawIsoRoad(points, width, color = '#666666') {
    if (!points || points.length < 2) return;
    
    ctx.save();
    
    // Draw road segments
    for (let i = 0; i < points.length - 1; i++) {
        const start = toIso(points[i][0], points[i][1], 0);
        const end = toIso(points[i + 1][0], points[i + 1][1], 0);
        
        // Calculate perpendicular offset for width
        const dx = end.x - start.x;
        const dy = end.y - start.y;
        const len = Math.sqrt(dx * dx + dy * dy);
        if (len === 0) continue;
        
        const perpX = -dy / len * width * scale * isoScale / 2;
        const perpY = dx / len * width * scale * isoScale / 2;
        
        // Draw road surface with provided color
        ctx.fillStyle = color;
        ctx.strokeStyle = '#555555';
        ctx.lineWidth = 2;
        
        ctx.beginPath();
        ctx.moveTo(start.x + perpX, start.y + perpY);
        ctx.lineTo(end.x + perpX, end.y + perpY);
        ctx.lineTo(end.x - perpX, end.y - perpY);
        ctx.lineTo(start.x - perpX, start.y - perpY);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }
    
    ctx.restore();
}

// Draw isometric tree
function drawIsoTree(x, y) {
    const p = toIso(x, y, 0);
    const baseRadius = 0.5 * scale * isoScale;
    const height = 2.5;
    
    // Tree trunk (brown cylinder)
    const trunkBottom = toIso(x, y, 0);
    const trunkTop = toIso(x, y, 0.8);
    
    ctx.fillStyle = '#8B4513';
    ctx.strokeStyle = '#654321';
    ctx.lineWidth = 1;
    
    // Draw trunk as vertical line with width
    ctx.beginPath();
    ctx.arc(trunkBottom.x, trunkBottom.y, baseRadius * 0.4, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    
    ctx.beginPath();
    ctx.arc(trunkTop.x, trunkTop.y, baseRadius * 0.35, 0, Math.PI * 2);
    ctx.fill();
    
    // Tree foliage (green circles at different heights)
    const foliageColors = ['#2d5016', '#3a6e1f', '#4a8c2a'];
    const foliageHeights = [1.5, 2.0, 2.5];
    const foliageRadii = [1.2, 1.0, 0.8];
    
    for (let i = 0; i < 3; i++) {
        const fp = toIso(x, y, foliageHeights[i]);
        const fr = foliageRadii[i] * scale * isoScale;
        
        // Draw foliage as ellipse
        ctx.fillStyle = foliageColors[i];
        ctx.beginPath();
        ctx.ellipse(fp.x, fp.y, fr, fr * 0.5, 0, 0, Math.PI * 2);
        ctx.fill();
        
        // Highlight
        ctx.fillStyle = 'rgba(144, 238, 144, 0.3)';
        ctx.beginPath();
        ctx.ellipse(fp.x - fr * 0.2, fp.y - fr * 0.2, fr * 0.4, fr * 0.2, 0, 0, Math.PI * 2);
        ctx.fill();
    }
}

// Draw isometric pond
function drawIsoPond(x, y, radius) {
    const p = toIso(x, y, 0);
    const r = radius * scale * isoScale;
    
    // Water surface (blue ellipse)
    const waterGradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r);
    waterGradient.addColorStop(0, '#6eb5ff');
    waterGradient.addColorStop(0.5, '#4a9fd8');
    waterGradient.addColorStop(1, '#2b7ab8');
    
    ctx.fillStyle = waterGradient;
    ctx.strokeStyle = '#1a5f8a';
    ctx.lineWidth = 2;
    
    // Draw pond as isometric ellipse
    ctx.beginPath();
    ctx.ellipse(p.x, p.y, r, r * 0.5, 0, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
    
    // Water ripples
    ctx.strokeStyle = 'rgba(255, 255, 255, 0.3)';
    ctx.lineWidth = 1;
    for (let i = 0; i < 3; i++) {
        const rippleRadius = r * (0.3 + i * 0.2);
        ctx.beginPath();
        ctx.ellipse(p.x, p.y, rippleRadius, rippleRadius * 0.5, 0, 0, Math.PI * 2);
        ctx.stroke();
    }
    
    // Highlight/shimmer
    ctx.fillStyle = 'rgba(255, 255, 255, 0.4)';
    ctx.beginPath();
    ctx.ellipse(p.x - r * 0.3, p.y - r * 0.15, r * 0.3, r * 0.15, 0, 0, Math.PI * 2);
    ctx.fill();
}

// Draw isometric building
function drawIsoBuilding(x, y, width, height) {
    const buildingHeight = Math.max(width, height) * scale * 1.2; // Taller building
    
    // Calculate corners in isometric view
    const corners = [
        toIso(x - width/2, y - height/2, 0),
        toIso(x + width/2, y - height/2, 0),
        toIso(x + width/2, y + height/2, 0),
        toIso(x - width/2, y + height/2, 0)
    ];
    
    // Draw shadow on ground
    ctx.fillStyle = 'rgba(0, 0, 0, 0.15)';
    ctx.beginPath();
    ctx.moveTo(corners[0].x + 10, corners[0].y + 5);
    ctx.lineTo(corners[1].x + 10, corners[1].y + 5);
    ctx.lineTo(corners[2].x + 10, corners[2].y + 5);
    ctx.lineTo(corners[3].x + 10, corners[3].y + 5);
    ctx.closePath();
    ctx.fill();
    
    // Draw front face (lighter) - modern gray/blue
    const frontGradient = ctx.createLinearGradient(
        corners[3].x, corners[3].y,
        corners[3].x, corners[3].y - buildingHeight
    );
    frontGradient.addColorStop(0, '#b8c6db');
    frontGradient.addColorStop(1, '#f5f7fa');
    ctx.fillStyle = frontGradient;
    ctx.strokeStyle = '#7a8c9e';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(corners[2].x, corners[2].y);
    ctx.lineTo(corners[3].x, corners[3].y);
    ctx.lineTo(corners[3].x, corners[3].y - buildingHeight);
    ctx.lineTo(corners[2].x, corners[2].y - buildingHeight);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Draw right face (darker)
    const rightGradient = ctx.createLinearGradient(
        corners[2].x, corners[2].y,
        corners[2].x, corners[2].y - buildingHeight
    );
    rightGradient.addColorStop(0, '#8fa3b8');
    rightGradient.addColorStop(1, '#c5d3e0');
    ctx.fillStyle = rightGradient;
    ctx.beginPath();
    ctx.moveTo(corners[1].x, corners[1].y);
    ctx.lineTo(corners[2].x, corners[2].y);
    ctx.lineTo(corners[2].x, corners[2].y - buildingHeight);
    ctx.lineTo(corners[1].x, corners[1].y - buildingHeight);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Draw top (roof) with gradient
    const roofGradient = ctx.createLinearGradient(
        corners[0].x, corners[0].y - buildingHeight,
        corners[2].x, corners[2].y - buildingHeight
    );
    roofGradient.addColorStop(0, '#d4dce6');
    roofGradient.addColorStop(1, '#e8eff5');
    ctx.fillStyle = roofGradient;
    ctx.beginPath();
    ctx.moveTo(corners[0].x, corners[0].y - buildingHeight);
    ctx.lineTo(corners[1].x, corners[1].y - buildingHeight);
    ctx.lineTo(corners[2].x, corners[2].y - buildingHeight);
    ctx.lineTo(corners[3].x, corners[3].y - buildingHeight);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Add modern windows on front face with isometric parallelograms
    const windowRows = 5;
    const windowCols = 3;
    const faceHeight = buildingHeight;
    const faceWidth = corners[3].x - corners[2].x;
    const windowSpacingY = faceHeight / (windowRows + 1);
    const windowSpacingX = faceWidth / (windowCols + 1);
    
    // Calculate the slope of the front face (from corner[2] to corner[3])
    const frontDx = corners[3].x - corners[2].x;
    const frontDy = corners[3].y - corners[2].y;
    
    for (let row = 1; row <= windowRows; row++) {
        for (let col = 1; col <= windowCols; col++) {
            const wx = corners[2].x + windowSpacingX * col;
            const wy = corners[2].y - faceHeight + windowSpacingY * row;
            
            // Draw isometric window (parallelogram) on front face
            const windowW = 8;
            const windowH = 12;
            
            // Calculate perpendicular direction to the face slope
            const perpDx = -frontDy;
            const perpDy = frontDx;
            const perpLen = Math.sqrt(perpDx * perpDx + perpDy * perpDy);
            const perpNormX = perpDx / perpLen;
            const perpNormY = perpDy / perpLen;
            
            // Half-width offset perpendicular to the face
            const offsetX = perpNormX * windowW / 2;
            const offsetY = perpNormY * windowW / 2;
            
            // Window frame (parallelogram)
            ctx.fillStyle = '#2c3e50';
            ctx.beginPath();
            ctx.moveTo(wx - offsetX, wy - offsetY - windowH/2);  // Top left
            ctx.lineTo(wx + offsetX, wy + offsetY - windowH/2);  // Top right
            ctx.lineTo(wx + offsetX, wy + offsetY + windowH/2);  // Bottom right
            ctx.lineTo(wx - offsetX, wy - offsetY + windowH/2);  // Bottom left
            ctx.closePath();
            ctx.fill();
            
            // Glass with gradient for reflection
            const glassGradient = ctx.createLinearGradient(wx - 3, wy - 5, wx + 3, wy + 5);
            glassGradient.addColorStop(0, '#a8d8ea');
            glassGradient.addColorStop(0.5, '#6db3d4');
            glassGradient.addColorStop(1, '#4a7c8a');
            ctx.fillStyle = glassGradient;
            ctx.beginPath();
            ctx.moveTo(wx - offsetX + 1, wy - offsetY - windowH/2 + 1);
            ctx.lineTo(wx + offsetX - 1, wy + offsetY - windowH/2 + 1);
            ctx.lineTo(wx + offsetX - 1, wy + offsetY + windowH/2 - 1);
            ctx.lineTo(wx - offsetX + 1, wy - offsetY + windowH/2 - 1);
            ctx.closePath();
            ctx.fill();
            
            // Window reflection highlight
            ctx.fillStyle = 'rgba(255, 255, 255, 0.3)';
            ctx.fillRect(wx - 3, wy - 5, 2, 4);
        }
    }
    
    // Add windows on right face - simple rectangles
    const rightWindowRows = 5;
    const rightWindowCols = 2;
    
    for (let row = 1; row <= rightWindowRows; row++) {
        for (let col = 1; col <= rightWindowCols; col++) {
            // Calculate position along the isometric edge
            const t = col / (rightWindowCols + 1);
            const wx = corners[1].x + (corners[2].x - corners[1].x) * t;
            const wy = corners[1].y + (corners[2].y - corners[1].y) * t - buildingHeight + windowSpacingY * row;
            
            // Draw simple rectangular windows on right face
            const windowW = 6;
            const windowH = 10;
            
            // Window frame (simple rectangle)
            ctx.fillStyle = '#2c3e50';
            ctx.fillRect(wx - windowW/2, wy - windowH/2, windowW, windowH);
            
            // Glass with darker gradient for side view
            const glassGradient = ctx.createLinearGradient(wx - windowW/2 + 1, wy - windowH/2 + 1, wx + windowW/2 - 1, wy + windowH/2 - 1);
            glassGradient.addColorStop(0, '#6b9eb5');
            glassGradient.addColorStop(1, '#3d5a6b');
            ctx.fillStyle = glassGradient;
            ctx.fillRect(wx - windowW/2 + 1, wy - windowH/2 + 1, windowW - 2, windowH - 2);
        }
    }
}

// Drawing functions
function drawIsoCarLane(points, width, direction) {
    if (!points || points.length < 2) return;
    
    // Draw car lane with dashed center line
    for (let i = 0; i < points.length - 1; i++) {
        const start = toIso(points[i][0], points[i][1], 0);
        const end = toIso(points[i + 1][0], points[i + 1][1], 0);
        
        // Calculate perpendicular offset
        const dx = end.x - start.x;
        const dy = end.y - start.y;
        const len = Math.sqrt(dx * dx + dy * dy);
        if (len === 0) continue;
        
        const perpX = -dy / len * width * scale * isoScale / 2;
        const perpY = dx / len * width * scale * isoScale / 2;
        
        // Draw lane surface (darker asphalt)
        ctx.fillStyle = '#444444';
        ctx.beginPath();
        ctx.moveTo(start.x + perpX, start.y + perpY);
        ctx.lineTo(end.x + perpX, end.y + perpY);
        ctx.lineTo(end.x - perpX, end.y - perpY);
        ctx.lineTo(start.x - perpX, start.y - perpY);
        ctx.closePath();
        ctx.fill();
        
        // Draw lane markings (dashed white line in center)
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 2;
        ctx.setLineDash([10, 10]);
        ctx.beginPath();
        ctx.moveTo(start.x, start.y);
        ctx.lineTo(end.x, end.y);
        ctx.stroke();
        ctx.setLineDash([]);
    }
}

function drawIsoPedestrianLane(points, width, color = '#cccccc') {
    if (!points || points.length < 2) return;
    
    // Draw pedestrian sidewalk
    for (let i = 0; i < points.length - 1; i++) {
        const start = toIso(points[i][0], points[i][1], 0);
        const end = toIso(points[i + 1][0], points[i + 1][1], 0);
        
        const dx = end.x - start.x;
        const dy = end.y - start.y;
        const len = Math.sqrt(dx * dx + dy * dy);
        if (len === 0) continue;
        
        const perpX = -dy / len * width * scale * isoScale / 2;
        const perpY = dx / len * width * scale * isoScale / 2;
        
        // Sidewalk surface (use provided color)
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.moveTo(start.x + perpX, start.y + perpY);
        ctx.lineTo(end.x + perpX, end.y + perpY);
        ctx.lineTo(end.x - perpX, end.y - perpY);
        ctx.lineTo(start.x - perpX, start.y - perpY);
        ctx.closePath();
        ctx.fill();
        
        // Border
        ctx.strokeStyle = '#999999';
        ctx.lineWidth = 2;
        ctx.stroke();
    }
}

function drawIsoZebraCrossing(x1, y1, x2, y2, width) {
    // Draw zebra crossing with white stripes
    const numStripes = 8;
    const dx = x2 - x1;
    const dy = y2 - y1;
    const segmentLen = 1 / numStripes;
    
    // Calculate perpendicular direction for stripe width
    const angle = Math.atan2(dy, dx);
    const perpX = Math.cos(angle + Math.PI / 2) * width / 2;
    const perpY = Math.sin(angle + Math.PI / 2) * width / 2;
    
    for (let i = 0; i < numStripes; i++) {
        const t1 = i * segmentLen;
        const t2 = t1 + segmentLen * 0.6; // 60% stripe, 40% gap for better visibility
        
        const sx1 = x1 + dx * t1;
        const sy1 = y1 + dy * t1;
        const sx2 = x1 + dx * t2;
        const sy2 = y1 + dy * t2;
        
        // Draw bright white stripe with shadow for visibility
        const p1 = toIso(sx1 + perpX, sy1 + perpY, 0.1);
        const p2 = toIso(sx2 + perpX, sy2 + perpY, 0.1);
        const p3 = toIso(sx2 - perpX, sy2 - perpY, 0.1);
        const p4 = toIso(sx1 - perpX, sy1 - perpY, 0.1);
        
        // Draw shadow first
        ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.beginPath();
        ctx.moveTo(p1.x + 2, p1.y + 2);
        ctx.lineTo(p2.x + 2, p2.y + 2);
        ctx.lineTo(p3.x + 2, p3.y + 2);
        ctx.lineTo(p4.x + 2, p4.y + 2);
        ctx.closePath();
        ctx.fill();
        
        // Draw bright white stripe
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#f0f0f0';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(p1.x, p1.y);
        ctx.lineTo(p2.x, p2.y);
        ctx.lineTo(p3.x, p3.y);
        ctx.lineTo(p4.x, p4.y);
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
    }
}

function drawIsoVehicle(x, y, type, laneId, color) {
    // Draw car in isometric view
    const carWidth = 2;
    const carLength = 4.5;
    const carHeight = 1.5;
    
    // Car corners
    const frontLeft = toIso(x - carWidth/2, y - carLength/2, 0);
    const frontRight = toIso(x + carWidth/2, y - carLength/2, 0);
    const backLeft = toIso(x - carWidth/2, y + carLength/2, 0);
    const backRight = toIso(x + carWidth/2, y + carLength/2, 0);
    
    // Car top corners
    const frontLeftTop = toIso(x - carWidth/2, y - carLength/2, carHeight);
    const frontRightTop = toIso(x + carWidth/2, y - carLength/2, carHeight);
    const backLeftTop = toIso(x - carWidth/2, y + carLength/2, carHeight);
    const backRightTop = toIso(x + carWidth/2, y + carLength/2, carHeight);
    
    // Draw car body (3D box)
    const carColor = color || (laneId !== undefined ? ['#ff3333', '#3333ff', '#ffff33', '#33ff33', '#ff9933'][laneId % 5] : '#ff3333');
    
    // Bottom face (shadow)
    ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
    ctx.beginPath();
    ctx.moveTo(frontLeft.x, frontLeft.y);
    ctx.lineTo(frontRight.x, frontRight.y);
    ctx.lineTo(backRight.x, backRight.y);
    ctx.lineTo(backLeft.x, backLeft.y);
    ctx.closePath();
    ctx.fill();
    
    // Left face
    ctx.fillStyle = shadeColor(carColor, -20);
    ctx.beginPath();
    ctx.moveTo(frontLeft.x, frontLeft.y);
    ctx.lineTo(frontLeftTop.x, frontLeftTop.y);
    ctx.lineTo(backLeftTop.x, backLeftTop.y);
    ctx.lineTo(backLeft.x, backLeft.y);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.stroke();
    
    // Right face
    ctx.fillStyle = shadeColor(carColor, -40);
    ctx.beginPath();
    ctx.moveTo(frontRight.x, frontRight.y);
    ctx.lineTo(frontRightTop.x, frontRightTop.y);
    ctx.lineTo(backRightTop.x, backRightTop.y);
    ctx.lineTo(backRight.x, backRight.y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Top face
    ctx.fillStyle = carColor;
    ctx.beginPath();
    ctx.moveTo(frontLeftTop.x, frontLeftTop.y);
    ctx.lineTo(frontRightTop.x, frontRightTop.y);
    ctx.lineTo(backRightTop.x, backRightTop.y);
    ctx.lineTo(backLeftTop.x, backLeftTop.y);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    // Windshield (front)
    const windshieldFrontLeft = toIso(x - carWidth/3, y - carLength/4, carHeight * 0.7);
    const windshieldFrontRight = toIso(x + carWidth/3, y - carLength/4, carHeight * 0.7);
    ctx.fillStyle = 'rgba(100, 150, 200, 0.6)';
    ctx.beginPath();
    ctx.moveTo(frontLeftTop.x, frontLeftTop.y);
    ctx.lineTo(frontRightTop.x, frontRightTop.y);
    ctx.lineTo(windshieldFrontRight.x, windshieldFrontRight.y);
    ctx.lineTo(windshieldFrontLeft.x, windshieldFrontLeft.y);
    ctx.closePath();
    ctx.fill();
}

function shadeColor(color, percent) {
    // Helper to darken/lighten colors
    const num = parseInt(color.replace("#", ""), 16);
    const amt = Math.round(2.55 * percent);
    const R = (num >> 16) + amt;
    const G = (num >> 8 & 0x00FF) + amt;
    const B = (num & 0x0000FF) + amt;
    return "#" + (0x1000000 + (R < 255 ? R < 1 ? 0 : R : 255) * 0x10000 +
        (G < 255 ? G < 1 ? 0 : G : 255) * 0x100 +
        (B < 255 ? B < 1 ? 0 : B : 255))
        .toString(16).slice(1);
}

function drawEnvironment() {
    // Clear canvas
    ctx.fillStyle = '#87CEEB'; // Sky blue background
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    // Draw ground with gradient (grass/pavement)
    const groundGradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height);
    groundGradient.addColorStop(0, '#9ed99c');
    groundGradient.addColorStop(0.5, '#a8d5a3');
    groundGradient.addColorStop(1, '#b8e5b3');
    ctx.fillStyle = groundGradient;
    
    if (isometricView) {
        // Draw isometric ground grid for depth perception
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.15)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= environment.width; i += 5) {
            const p1 = toIso(i, 0);
            const p2 = toIso(i, environment.height);
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        }
        for (let j = 0; j <= environment.height; j += 5) {
            const p1 = toIso(0, j);
            const p2 = toIso(environment.width, j);
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        }
    } else {
        ctx.fillRect(0, 0, canvas.width, canvas.height);
    }
    
    // Draw roads (under everything)
    if (environment.roads) {
        console.log('Drawing', environment.roads.length, 'roads');
        environment.roads.forEach(road => {
            console.log('Road:', road.points.length, 'points, width:', road.width);
            drawIsoRoad(road.points, road.width || 4, road.color || '#666666');
        });
    }

    // Draw decorations (trees, ponds, etc.) - but NOT buildings yet
    if (environment.decorations) {
        environment.decorations.forEach(deco => {
            if (deco.type === 'tree') {
                drawIsoTree(deco.position[0], deco.position[1]);
            } else if (deco.type === 'pond') {
                drawIsoPond(deco.position[0], deco.position[1], deco.radius || 3);
            }
            // Buildings will be drawn last, skip them here
        });
    }
    
    // Draw walls with 3D isometric blocks
    environment.walls.forEach(wall => {
        drawIsoWall(wall.start[0], wall.start[1], wall.end[0], wall.end[1], 2);
    });
    
    // Draw car lanes (visual guides)
    if (environment.carLanes) {
        environment.carLanes.forEach(lane => {
            drawIsoCarLane(lane.points, lane.width || 3.5, lane.direction);
        });
    }
    
    // Draw pedestrian lanes
    if (environment.pedestrianLanes) {
        environment.pedestrianLanes.forEach(lane => {
            drawIsoPedestrianLane(lane.points, lane.width || 2.5, lane.color || '#cccccc');
        });
    }
    
    // Draw crossing lanes (zebra crossings) - LAST so they're on top and visible
    if (environment.crossingLanes) {
        console.log('Drawing', environment.crossingLanes.length, 'zebra crossings');
        environment.crossingLanes.forEach(lane => {
            drawIsoZebraCrossing(lane.start[0], lane.start[1], lane.end[0], lane.end[1], lane.width || 4);
        });
    }
    
    // Draw entrances with 3D platforms
    environment.entrances.forEach(ent => {
        drawIsoEntrance(ent.position[0], ent.position[1], ent.radius, ent.flow_rate);
    });
    
    // Draw exits with 3D platforms
    environment.exits.forEach(exit => {
        drawIsoExit(exit.position[0], exit.position[1], exit.radius);
    });
    
    // Draw vehicles
    if (environment.vehicles) {
        // Update vehicle positions (move 10x faster than pedestrians)
        const carSpeed = 0.15; // m per frame (10x pedestrian speed of 0.015)
        environment.vehicles.forEach(vehicle => {
            if (!vehicle.velocity) {
                vehicle.velocity = [0, 0];
            }
            
            // Check traffic light for this lane
            let canMove = true;
            const carLane = environment.carLanes ? environment.carLanes.find(l => l.laneId === vehicle.laneId) : null;
            
            if (carLane) {
                // Find relevant traffic light based on direction
                let relevantLight = null;
                if (carLane.direction === 'east' && vehicle.position[0] < 35) {
                    relevantLight = environment.trafficLights.find(tl => tl.id === 'tl_west');
                } else if (carLane.direction === 'west' && vehicle.position[0] > 45) {
                    relevantLight = environment.trafficLights.find(tl => tl.id === 'tl_east');
                } else if (carLane.direction === 'south' && vehicle.position[1] < 35) {
                    relevantLight = environment.trafficLights.find(tl => tl.id === 'tl_north');
                } else if (carLane.direction === 'north' && vehicle.position[1] > 45) {
                    relevantLight = environment.trafficLights.find(tl => tl.id === 'tl_south');
                }
                
                if (relevantLight) {
                    const lightState = trafficLightStates[relevantLight.id];
                    if (lightState && lightState.state === 'red') {
                        canMove = false;
                    }
                }
            }
            
            // Move vehicle if allowed
            if (canMove) {
                vehicle.position[0] += vehicle.velocity[0] * carSpeed;
                vehicle.position[1] += vehicle.velocity[1] * carSpeed;
                
                // Wrap around when vehicle leaves the map
                if (vehicle.position[0] > 80) vehicle.position[0] = 0;
                if (vehicle.position[0] < 0) vehicle.position[0] = 80;
                if (vehicle.position[1] > 80) vehicle.position[1] = 0;
                if (vehicle.position[1] < 0) vehicle.position[1] = 80;
            }
            
            // Draw the vehicle
            drawIsoVehicle(vehicle.position[0], vehicle.position[1], vehicle.type, vehicle.laneId, vehicle.color);
        });
    } else {
        // Original static drawing if no vehicles array
        if (environment.vehicles) {
            environment.vehicles.forEach(vehicle => {
                drawIsoVehicle(vehicle.position[0], vehicle.position[1], vehicle.type, vehicle.laneId);
            });
        }
    }
    
    ctx.textAlign = 'left'; // Reset text align
}

function updateVisualization(state) {
    drawEnvironment();
    
    // Draw hazards with animated effects in isometric view
    if (state.environment && state.environment.hazards) {
        state.environment.hazards.forEach(hazard => {
            const p = toIso(hazard.position[0], hazard.position[1], 0);
            const r = hazard.radius * scale * isoScale;
            
            if (hazard.type === 'fire') {
                // Animated fire effect
                const time = Date.now() / 100;
                
                // Draw large danger zone shadow on ground
                ctx.fillStyle = 'rgba(255, 87, 34, 0.3)';
                ctx.beginPath();
                ctx.ellipse(p.x, p.y, r * 1.2, r * 0.7, Math.PI / 4, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw smoke/heat distortion (dark gray circles rising)
                for (let i = 0; i < 5; i++) {
                    const smokeTime = (time + i * 3) % 15;
                    const smokeR = r * (0.4 + smokeTime * 0.08);
                    const smokeAlpha = Math.max(0, 0.4 - smokeTime / 15);
                    const smokeP = toIso(hazard.position[0], hazard.position[1], smokeTime * 0.5);
                    
                    ctx.fillStyle = `rgba(80, 80, 80, ${smokeAlpha})`;
                    ctx.beginPath();
                    ctx.arc(smokeP.x, smokeP.y, smokeR, 0, Math.PI * 2);
                    ctx.fill();
                }
                
                // Draw animated fire flames with height
                for (let i = 0; i < 8; i++) {
                    const offset = (time + i * 1.5) % 10;
                    const fireR = r * (0.4 + offset * 0.06);
                    const alpha = Math.max(0, 1 - offset / 10);
                    const fireP = toIso(hazard.position[0], hazard.position[1], offset * 0.3);
                    
                    const fireGradient = ctx.createRadialGradient(fireP.x, fireP.y, 0, fireP.x, fireP.y, fireR);
                    fireGradient.addColorStop(0, `rgba(255, 255, 200, ${alpha})`);  // Bright yellow-white core
                    fireGradient.addColorStop(0.3, `rgba(255, 215, 0, ${alpha * 0.9})`);  // Yellow
                    fireGradient.addColorStop(0.5, `rgba(255, 140, 0, ${alpha * 0.7})`);  // Orange
                    fireGradient.addColorStop(0.7, `rgba(255, 69, 0, ${alpha * 0.5})`);   // Red-orange
                    fireGradient.addColorStop(0.9, `rgba(200, 0, 0, ${alpha * 0.3})`);    // Dark red
                    fireGradient.addColorStop(1, `rgba(255, 0, 0, 0)`);
                    
                    ctx.fillStyle = fireGradient;
                    ctx.beginPath();
                    ctx.arc(fireP.x, fireP.y, fireR, 0, Math.PI * 2);
                    ctx.fill();
                }
                
                // Draw fire base (bright glow on ground)
                const baseGradient = ctx.createRadialGradient(p.x, p.y, 0, p.x, p.y, r * 0.8);
                baseGradient.addColorStop(0, 'rgba(255, 200, 0, 0.8)');
                baseGradient.addColorStop(0.5, 'rgba(255, 100, 0, 0.6)');
                baseGradient.addColorStop(1, 'rgba(255, 0, 0, 0)');
                ctx.fillStyle = baseGradient;
                ctx.beginPath();
                ctx.arc(p.x, p.y, r * 0.8, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw fire icon/symbol elevated higher
                const iconP = toIso(hazard.position[0], hazard.position[1], 2);
                ctx.fillStyle = '#ff4500';
                ctx.font = 'bold 32px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('🔥', iconP.x, iconP.y);
                
                // Draw danger text
                ctx.fillStyle = '#ff0000';
                ctx.font = 'bold 14px Arial';
                ctx.fillText('FIRE!', iconP.x, iconP.y + 25);
                
            } else {
                // Shooting/other hazard effect
                ctx.fillStyle = 'rgba(245, 158, 11, 0.25)';
                ctx.beginPath();
                ctx.ellipse(p.x, p.y, r, r * 0.6, Math.PI / 4, 0, Math.PI * 2);
                ctx.fill();
                
                ctx.strokeStyle = '#d97706';
                ctx.lineWidth = 3;
                ctx.setLineDash([10, 5]);
                ctx.stroke();
                ctx.setLineDash([]);
                
                // Warning symbol elevated
                const iconP = toIso(hazard.position[0], hazard.position[1], 0.5);
                ctx.fillStyle = '#f57c00';
                ctx.font = 'bold 28px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('⚠️', iconP.x, iconP.y);
            }
        });
    }
    
    // Calculate density for traffic jam detection
    const areaSize = (environment.width * environment.height);
    const density = state.pedestrians.length / areaSize;
    const densityThreshold = 0.015; // Adjust this value as needed
    const isTrafficJam = density > densityThreshold;
    
    console.log('Drawing pedestrians:', state.pedestrians.length);
    
    // Draw pedestrians as human-like figures in isometric view
    state.pedestrians.forEach((ped, index) => {
        const panic = ped.panic_level || 0;
        const drawRadius = Math.max(ped.radius * scale * isoScale, 4);
        
        // Get isometric position
        const p = toIso(ped.position[0], ped.position[1], 0.5);
        
        // Check if pedestrian is stopped (velocity near zero)
        const velocity = ped.velocity || [0, 0];
        const speed = Math.sqrt(velocity[0] * velocity[0] + velocity[1] * velocity[1]);
        const isStopped = speed < 0.05;  // Near-zero velocity = stopped
        
        // Check if pedestrian is at a red light crossing
        const crossing = isOnZebraCrossing(ped.position);
        const isWaitingAtRedLight = crossing && !canCrossCrossing(ped.position, crossing);
        
        // Check local density around this pedestrian for movement limitation
        let nearbyCount = 0;
        const checkRadius = ped.radius * 3;
        state.pedestrians.forEach(otherPed => {
            if (otherPed !== ped) {
                const dx = ped.position[0] - otherPed.position[0];
                const dy = ped.position[1] - otherPed.position[1];
                const dist = Math.sqrt(dx*dx + dy*dy);
                if (dist < checkRadius) {
                    nearbyCount++;
                }
            }
        });
        const isStuck = nearbyCount > 5; // Too crowded, stop moving
        
        // Color based on state - PRIORITY: stopped at traffic light
        let bodyColor, headColor, borderColor;
        if (isStopped && !isStuck) {
            // Stopped at red traffic light - bright red with white border
            bodyColor = '#ff1744'; // Bright red for STOPPED
            headColor = '#d50000';
            borderColor = '#ffffff'; // White border for high visibility
        } else if (isWaitingAtRedLight) {
            bodyColor = '#ff9800'; // Orange for waiting at red light
            headColor = '#f57c00';
            borderColor = '#e65100';
        } else if (isStuck) {
            bodyColor = '#9e9e9e'; // Gray for stuck
            headColor = '#757575';
            borderColor = '#424242';
        } else if (panic > 0.7) {
            bodyColor = '#ef5350'; // High panic - red
            headColor = '#f44336';
            borderColor = '#c62828';
        } else if (panic > 0.3) {
            bodyColor = '#ffa726'; // Medium panic - orange
            headColor = '#ff9800';
            borderColor = '#f57c00';
        } else {
            bodyColor = '#66bb6a'; // Calm - green
            headColor = '#4caf50';
            borderColor = '#388e3c';
        }
        
        // Draw shadow (ellipse on ground)
        const shadowP = toIso(ped.position[0], ped.position[1], 0);
        ctx.fillStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.beginPath();
        ctx.ellipse(shadowP.x, shadowP.y, drawRadius * 0.8, drawRadius * 0.4, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
        
        // Draw human figure in isometric
        const headRadius = drawRadius * 0.5;
        const bodyHeight = drawRadius * 1.5;
        const bodyWidth = drawRadius * 0.9;
        
        // Head with 3D effect
        const headP = toIso(ped.position[0], ped.position[1], 1.8);
        const headGradient = ctx.createRadialGradient(
            headP.x - headRadius * 0.3, headP.y - headRadius * 0.3, 0,
            headP.x, headP.y, headRadius
        );
        headGradient.addColorStop(0, headColor);
        headGradient.addColorStop(1, borderColor);
        ctx.fillStyle = headGradient;
        ctx.beginPath();
        ctx.arc(headP.x, headP.y, headRadius, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = borderColor;
        ctx.lineWidth = 1.5;
        ctx.stroke();
        
        // Body (simple vertical bar in isometric)
        const bodyTop = toIso(ped.position[0], ped.position[1], 1.5);
        const bodyBottom = toIso(ped.position[0], ped.position[1], 0.6);
        ctx.strokeStyle = bodyColor;
        ctx.lineWidth = bodyWidth;
        ctx.lineCap = 'round';
        ctx.beginPath();
        ctx.moveTo(bodyBottom.x, bodyBottom.y);
        ctx.lineTo(bodyTop.x, bodyTop.y);
        ctx.stroke();
        
        // Legs
        const legBase = toIso(ped.position[0], ped.position[1], 0.5);
        const legTop = toIso(ped.position[0], ped.position[1], 0.6);
        ctx.strokeStyle = bodyColor;
        ctx.lineWidth = bodyWidth * 0.4;
        // Left leg
        ctx.beginPath();
        ctx.moveTo(legTop.x - bodyWidth * 0.2, legTop.y);
        ctx.lineTo(legBase.x - bodyWidth * 0.3, legBase.y + bodyWidth * 0.3);
        ctx.stroke();
        // Right leg
        ctx.beginPath();
        ctx.moveTo(legTop.x + bodyWidth * 0.2, legTop.y);
        ctx.lineTo(legBase.x + bodyWidth * 0.3, legBase.y + bodyWidth * 0.3);
        ctx.stroke();
        
        // Draw direction indicator if moving
        if (ped.velocity && !isStuck) {
            const speed = Math.sqrt(ped.velocity[0]**2 + ped.velocity[1]**2);
            if (speed > 0.1) {
                const targetP = toIso(
                    ped.position[0] + ped.velocity[0] * 0.8,
                    ped.position[1] + ped.velocity[1] * 0.8,
                    0.5
                );
                
                // Arrow
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.9)';
                ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
                ctx.lineWidth = 2;
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(targetP.x, targetP.y);
                ctx.stroke();
                
                // Arrow head
                const angle = Math.atan2(targetP.y - p.y, targetP.x - p.x);
                ctx.beginPath();
                ctx.moveTo(targetP.x, targetP.y);
                ctx.lineTo(
                    targetP.x - Math.cos(angle - 0.5) * 6,
                    targetP.y - Math.sin(angle - 0.5) * 6
                );
                ctx.lineTo(
                    targetP.x - Math.cos(angle + 0.5) * 6,
                    targetP.y - Math.sin(angle + 0.5) * 6
                );
                ctx.closePath();
                ctx.fill();
            }
        }
        
        // Draw stuck indicator if crowded
        if (isStuck) {
            ctx.fillStyle = '#ff9800';
            ctx.font = 'bold 14px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('⏸', headP.x, headP.y - headRadius - 10);
        }
        
        // Draw panic indicator above head if panicked
        if (panic > 0.5 && !isStuck) {
            ctx.fillStyle = '#ff1744';
            ctx.font = 'bold 12px Arial';
            ctx.textAlign = 'center';
            ctx.fillText('!', headP.x, headP.y - headRadius - 10);
        }
    });
    
    // Detect and draw traffic jam zones
    drawTrafficJamAlerts(state.pedestrians);
    
    // Draw buildings before traffic lights (so traffic lights appear on top)
    if (environment.decorations) {
        environment.decorations.forEach(deco => {
            if (deco.type === 'building') {
                drawIsoBuilding(deco.position[0], deco.position[1], deco.width || 5, deco.height || 5);
            }
        });
    }
    
    // Draw traffic lights LAST so they appear on top of everything
    if (environment.trafficLights) {
        console.log('Drawing', environment.trafficLights.length, 'traffic lights');
        environment.trafficLights.forEach(light => {
            const state = trafficLightStates[light.id]?.state || 'red';
            console.log('Traffic light', light.id, 'at', light.position, 'state:', state);
            drawIsoTrafficLight(light.position[0], light.position[1], state, light.orientation);
        });
    }
    
    ctx.textAlign = 'left'; // Reset text align
    ctx.lineCap = 'butt'; // Reset line cap
    
    // Update traffic jam warning in stats
    updateTrafficJamWarning(isTrafficJam, density, densityThreshold);
}

// Detect and draw traffic jam alerts on the map
function drawTrafficJamAlerts(pedestrians) {
    if (!pedestrians || pedestrians.length === 0) return;
    
    // Grid-based density detection
    const gridSize = 5; // meters per grid cell
    const gridCols = Math.ceil(environment.width / gridSize);
    const gridRows = Math.ceil(environment.height / gridSize);
    const densityGrid = Array(gridRows).fill(null).map(() => Array(gridCols).fill(0));
    
    // Count pedestrians in each grid cell
    pedestrians.forEach(ped => {
        const gridX = Math.floor(ped.position[0] / gridSize);
        const gridY = Math.floor(ped.position[1] / gridSize);
        if (gridX >= 0 && gridX < gridCols && gridY >= 0 && gridY < gridRows) {
            densityGrid[gridY][gridX]++;
        }
    });
    
    // Draw alerts for high-density areas
    const jamThreshold = 8; // Number of pedestrians in a 5x5m area
    for (let row = 0; row < gridRows; row++) {
        for (let col = 0; col < gridCols; col++) {
            if (densityGrid[row][col] >= jamThreshold) {
                const centerX = (col + 0.5) * gridSize;
                const centerY = (row + 0.5) * gridSize;
                
                // Draw pulsating warning circle
                const time = Date.now() / 1000;
                const pulse = Math.sin(time * 3) * 0.3 + 1;
                const alertRadius = gridSize * 0.8 * pulse;
                
                const alertPos = toIso(centerX, centerY, 0);
                
                // Draw warning zone with gradient
                const gradient = ctx.createRadialGradient(
                    alertPos.x, alertPos.y, 0,
                    alertPos.x, alertPos.y, alertRadius * scale * isoScale
                );
                gradient.addColorStop(0, 'rgba(255, 152, 0, 0.4)');
                gradient.addColorStop(0.7, 'rgba(255, 152, 0, 0.2)');
                gradient.addColorStop(1, 'rgba(255, 152, 0, 0)');
                
                ctx.fillStyle = gradient;
                ctx.beginPath();
                ctx.arc(alertPos.x, alertPos.y, alertRadius * scale * isoScale, 0, Math.PI * 2);
                ctx.fill();
                
                // Draw warning border
                ctx.strokeStyle = `rgba(255, 152, 0, ${0.6 * pulse})`;
                ctx.lineWidth = 3;
                ctx.setLineDash([10, 5]);
                ctx.beginPath();
                ctx.arc(alertPos.x, alertPos.y, alertRadius * scale * isoScale, 0, Math.PI * 2);
                ctx.stroke();
                ctx.setLineDash([]);
                
                // Draw warning icon and text above the zone
                const iconPos = toIso(centerX, centerY, 3);
                
                // Warning triangle background
                ctx.fillStyle = 'rgba(255, 152, 0, 0.9)';
                ctx.beginPath();
                ctx.moveTo(iconPos.x, iconPos.y - 20);
                ctx.lineTo(iconPos.x - 15, iconPos.y);
                ctx.lineTo(iconPos.x + 15, iconPos.y);
                ctx.closePath();
                ctx.fill();
                
                ctx.strokeStyle = '#ff6f00';
                ctx.lineWidth = 2;
                ctx.stroke();
                
                // Exclamation mark
                ctx.fillStyle = '#000';
                ctx.font = 'bold 16px Arial';
                ctx.textAlign = 'center';
                ctx.textBaseline = 'middle';
                ctx.fillText('!', iconPos.x, iconPos.y - 10);
                
                // "TRAFFIC JAM" text
                ctx.fillStyle = '#fff';
                ctx.strokeStyle = '#ff6f00';
                ctx.lineWidth = 3;
                ctx.font = 'bold 14px Arial';
                ctx.strokeText('TRAFFIC JAM', iconPos.x, iconPos.y + 18);
                ctx.fillText('TRAFFIC JAM', iconPos.x, iconPos.y + 18);
                
                // Pedestrian count
                ctx.font = 'bold 12px Arial';
                ctx.fillStyle = '#fff';
                ctx.strokeStyle = '#ff6f00';
                ctx.lineWidth = 2;
                ctx.strokeText(`${densityGrid[row][col]} people`, iconPos.x, iconPos.y + 35);
                ctx.fillText(`${densityGrid[row][col]} people`, iconPos.x, iconPos.y + 35);
            }
        }
    }
    
    ctx.textAlign = 'left';
    ctx.textBaseline = 'alphabetic';
}

// Traffic light control system
function updateTrafficLights(currentTime) {
    if (!environment.trafficLights || environment.trafficLights.length === 0) {
        return;
    }
    
    // Traffic light cycle: 15 seconds green, 15 seconds red (total 30s cycle)
    const cycleDuration = 30; // Total cycle time in seconds
    const cyclePosition = currentTime % cycleDuration; // Where we are in the cycle
    
    // First 15 seconds: NS=red, EW=green
    // Next 15 seconds: NS=green, EW=red
    const nsState = (cyclePosition < 15) ? 'red' : 'green';
    const ewState = (cyclePosition < 15) ? 'green' : 'red';
    
    // Update all traffic lights
    environment.trafficLights.forEach(light => {
        const newState = (light.controls === 'north-south') ? nsState : ewState;
        
        // Initialize or update state
        if (!trafficLightStates[light.id]) {
            trafficLightStates[light.id] = { state: newState, lastChange: currentTime };
        } else {
            trafficLightStates[light.id].state = newState;
        }
    });
}

// Check if pedestrian can cross based on traffic light
function canCrossCrossing(pedPosition, crossingLane) {
    // Find associated traffic light for this crossing
    if (!environment.trafficLights || !crossingLane.trafficLightId) return true;
    
    const associatedLight = environment.trafficLights.find(light => 
        light.id === crossingLane.trafficLightId
    );
    
    if (!associatedLight) return true;
    
    const lightState = trafficLightStates[associatedLight.id];
    return lightState && lightState.state === 'green';
}

// Check if pedestrian is on a zebra crossing
function isOnZebraCrossing(position) {
    if (!environment.crossingLanes) return false;
    
    for (const crossing of environment.crossingLanes) {
        const x1 = Math.min(crossing.start[0], crossing.end[0]);
        const x2 = Math.max(crossing.start[0], crossing.end[0]);
        const y1 = Math.min(crossing.start[1], crossing.end[1]);
        const y2 = Math.max(crossing.start[1], crossing.end[1]);
        
        const margin = crossing.width || 4;
        
        if (position[0] >= x1 - margin && position[0] <= x2 + margin &&
            position[1] >= y1 - margin && position[1] <= y2 + margin) {
            return crossing;
        }
    }
    return null;
}

// Check if pedestrian is on sidewalk
function isOnSidewalk(position) {
    if (!environment.pedestrianLanes) return false;
    
    for (const lane of environment.pedestrianLanes) {
        for (let i = 0; i < lane.points.length - 1; i++) {
            const p1 = lane.points[i];
            const p2 = lane.points[i + 1];
            
            const x1 = Math.min(p1[0], p2[0]);
            const x2 = Math.max(p1[0], p2[0]);
            const y1 = Math.min(p1[1], p2[1]);
            const y2 = Math.max(p1[1], p2[1]);
            
            const margin = (lane.width || 5) / 2;
            
            if (position[0] >= x1 - margin && position[0] <= x2 + margin &&
                position[1] >= y1 - margin && position[1] <= y2 + margin) {
                return true;
            }
        }
    }
    return false;
}

// Traffic jam warning function
function updateTrafficJamWarning(isTrafficJam, density, threshold) {
    let warningElement = document.getElementById('traffic-jam-warning');
    
    // Create warning element if it doesn't exist
    if (!warningElement) {
        const statsPanel = document.querySelector('.stats-panel');
        if (statsPanel) {
            warningElement = document.createElement('div');
            warningElement.id = 'traffic-jam-warning';
            warningElement.className = 'stat-card warning-card';
            warningElement.style.display = 'none';
            warningElement.innerHTML = `
                <div class="stat-icon">⚠️</div>
                <div class="stat-content">
                    <div class="stat-label">交通拥堵警告 / TRAFFIC JAM</div>
                    <div class="stat-value" id="density-value">0.00</div>
                    <div class="stat-label" style="font-size: 10px; margin-top: 4px;">
                        密度阈值 / Threshold: <span id="density-threshold">0.000</span>
                    </div>
                </div>
            `;
            statsPanel.insertBefore(warningElement, statsPanel.firstChild);
        }
    }
    
    if (warningElement) {
        const densityValue = document.getElementById('density-value');
        const densityThresholdSpan = document.getElementById('density-threshold');
        
        if (densityValue) {
            densityValue.textContent = density.toFixed(4);
        }
        if (densityThresholdSpan) {
            densityThresholdSpan.textContent = threshold.toFixed(4);
        }
        
        if (isTrafficJam) {
            warningElement.style.display = 'flex';
            warningElement.style.borderLeftColor = '#ff9800';
            warningElement.style.animation = 'pulse 1.5s infinite';
        } else {
            warningElement.style.display = 'none';
        }
    }
}

function updateStatistics(state) {
    document.getElementById('stat-time').textContent = state.time.toFixed(1);
    document.getElementById('stat-active').textContent = state.stats.active;
    document.getElementById('stat-spawned').textContent = state.stats.spawned;
    document.getElementById('stat-exited').textContent = state.stats.exited;
    
    const avgPanic = state.stats.active > 0 ? 
        (state.stats.total_panic / state.stats.active).toFixed(2) : '0.00';
    document.getElementById('stat-panic').textContent = avgPanic;
}

function resetStatistics() {
    document.getElementById('stat-time').textContent = '0.0';
    document.getElementById('stat-active').textContent = '0';
    document.getElementById('stat-spawned').textContent = '0';
    document.getElementById('stat-exited').textContent = '0';
    document.getElementById('stat-panic').textContent = '0.0';
}

// Update flow rate display on entrances
function updateFlowRateDisplay() {
    const flowRate = parseFloat(document.getElementById('flowRate').value);
    
    // Update all entrances with new flow rate
    environment.entrances.forEach(entrance => {
        entrance.flow_rate = flowRate;
    });
    
    // Redraw to show updated flow rates
    drawEnvironment();
}

// Control functions
function createEnvironment() {
    const width = parseFloat(document.getElementById('envWidth').value);
    const height = parseFloat(document.getElementById('envHeight').value);
    
    environment.width = width;
    environment.height = height;
    scale = canvas.width / width;
    
    socket.emit('create_environment', environment);
}

function startSimulation() {
    const record = document.getElementById('recordSimulation').checked;
    const numPedestrians = parseInt(document.getElementById('numPedestrians').value);
    const initialPedestrians = parseInt(document.getElementById('initialPedestrians').value);
    const speed = parseFloat(document.getElementById('simSpeed').value);
    const flowRate = parseFloat(document.getElementById('flowRate').value);
    const exitMode = document.getElementById('exitMode').value;
    
    // Update all entrances with current flow rate setting
    environment.entrances.forEach(entrance => {
        entrance.flow_rate = flowRate;
    });
    
    socket.emit('start_simulation', { 
        record: record,
        num_pedestrians: numPedestrians,
        initial_pedestrians: initialPedestrians,
        speed: speed,
        flow_rate: flowRate,
        exit_mode: exitMode
    });
}

function stopSimulation() {
    socket.emit('stop_simulation');
}

function resetSimulation() {
    socket.emit('reset_simulation');
}

function addEvent() {
    const eventType = document.getElementById('eventType').value;
    const immediateEvent = document.getElementById('immediateEvent').checked;
    const triggerTime = immediateEvent ? 
        (currentSimulationState.time || 0) : 
        Number.parseFloat(document.getElementById('eventTime').value);
    
    const eventData = {
        type: eventType,
        trigger_time: triggerTime
    };
    
    if (eventType === 'fire' || eventType === 'shooting') {
        eventData.position = [
            Number.parseFloat(document.getElementById('eventX').value),
            Number.parseFloat(document.getElementById('eventY').value)
        ];
        eventData.radius = Number.parseFloat(document.getElementById('eventRadius').value);
    } else if (eventType.includes('entrance') || eventType.includes('exit')) {
        const indexKey = eventType.includes('entrance') ? 'entrance_idx' : 'exit_idx';
        eventData[indexKey] = Number.parseInt(document.getElementById('eventIndex').value);
    }
    
    console.log('Adding event:', eventData);
    socket.emit('add_event', eventData);
    
    // Show confirmation
    alert(`Event "${eventType}" will trigger at ${triggerTime.toFixed(1)}s\nPosition: [${eventData.position?.[0] || 'N/A'}, ${eventData.position?.[1] || 'N/A'}]`);
    
    // Keep selection mode active for adding more events
    // Redraw to show the preview again
    updateEventPreview();
    drawEnvironment();
    if (selectedEventPosition) {
        drawEventPreview(selectedEventPosition[0], selectedEventPosition[1]);
    }
}

// Update event input fields based on event type
function updateEventInputs() {
    const eventType = document.getElementById('eventType').value;
    const positionInputs = document.getElementById('eventPositionInputs');
    const indexInputs = document.getElementById('eventIndexInputs');
    const immediateCheckbox = document.getElementById('immediateEvent');
    const delayedTimeDiv = document.getElementById('delayedEventTime');
    
    // Show/hide position inputs for fire/shooting
    if (eventType === 'fire' || eventType === 'shooting') {
        positionInputs.style.display = 'block';
        indexInputs.style.display = 'none';
    } else if (eventType.includes('entrance') || eventType.includes('exit')) {
        positionInputs.style.display = 'none';
        indexInputs.style.display = 'block';
    }
    
    // Toggle delayed time input
    if (immediateCheckbox && immediateCheckbox.checked) {
        delayedTimeDiv.style.display = 'none';
    } else {
        delayedTimeDiv.style.display = 'block';
    }
}

// Draw event preview on canvas
function drawEventPreview(x, y) {
    if (!x || !y) return;
    
    const radius = eventPreviewRadius;
    const pos = toIso(x, y, 0);
    
    // Draw preview circle (using isometric projection)
    ctx.save();
    ctx.translate(pos.x, pos.y);
    if (isometricView) {
        ctx.scale(1, 0.5); // Flatten circle for isometric view
    }
    ctx.beginPath();
    ctx.arc(0, 0, radius * scale * isoScale, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(255, 165, 0, 0.8)';
    ctx.lineWidth = 2;
    ctx.setLineDash([5, 5]);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
    
    // Draw center point
    ctx.beginPath();
    ctx.arc(pos.x, pos.y, 3, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255, 165, 0, 0.8)';
    ctx.fill();
}

// Update event preview text
function updateEventPreview() {
    const previewDiv = document.getElementById('eventPreview');
    
    if (selectedEventPosition && eventSelectionMode) {
        const eventType = document.getElementById('eventType').value;
        const eventTypeText = {
            'fire': '火灾',
            'shooting': '枪击',
            'block_entrance': '入口封闭',
            'unblock_entrance': '入口开放',
            'block_exit': '出口封闭',
            'unblock_exit': '出口开放'
        };
        
        const radius = eventPreviewRadius;
        const x = selectedEventPosition[0].toFixed(1);
        const y = selectedEventPosition[1].toFixed(1);
        
        previewDiv.innerHTML = `
            <strong>事件预览：</strong><br>
            类型：${eventTypeText[eventType] || eventType}<br>
            位置：(${x}, ${y})<br>
            半径：${radius}m
        `;
        previewDiv.style.display = 'block';
    } else {
        previewDiv.style.display = 'none';
    }
}

function exportToUnity() {
    socket.emit('export_unity', {});
}

// Event type change handler
// Immediate event checkbox handler
document.getElementById('immediateEvent')?.addEventListener('change', (e) => {
    updateEventInputs();
});

// Initialize
window.onload = () => {
    setTool('wall');
    drawEnvironment();
    
    // Set default event inputs visibility
    document.getElementById('eventType').dispatchEvent(new Event('change'));
    document.getElementById('immediateEvent').dispatchEvent(new Event('change'));
};
