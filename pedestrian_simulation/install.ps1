# Pedestrian Simulation System - PowerShell Installation Script
# Supports Windows 10/11

# Set error handling
$ErrorActionPreference = "Stop"

# Color functions
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

function Write-Step {
    param([string]$Text)
    Write-ColorText "`n$Text" "Cyan"
}

function Write-Success {
    param([string]$Text)
    Write-ColorText "✓ $Text" "Green"
}

function Write-Error-Custom {
    param([string]$Text)
    Write-ColorText "✗ $Text" "Red"
}

function Write-Info {
    param([string]$Text)
    Write-ColorText "ℹ $Text" "Yellow"
}

# Title
Clear-Host
Write-ColorText "========================================" "Cyan"
Write-ColorText "Pedestrian Simulation System - Windows Installer" "Cyan"
Write-ColorText "========================================" "Cyan"
Write-Host ""

# Step 1: Check Python
Write-Step "[1/6] Checking Python..."
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "Python installed: $pythonVersion"
    } else {
        throw "Python not found"
    }
} catch {
    Write-Error-Custom "Python not found"
    Write-Host ""
    Write-ColorText "Please install Python 3.8 or higher" "Yellow"
    Write-ColorText "Download from: https://www.python.org/downloads/" "Cyan"
    Write-ColorText "Make sure to check 'Add Python to PATH' during installation" "Yellow"
    Read-Host "`nPress Enter to exit"
    exit 1
}

# Step 2: Check pip
Write-Step "[2/6] Checking pip..."
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Success "pip installed"
    } else {
        throw "pip not found"
    }
} catch {
    Write-Error-Custom "pip not found"
    Read-Host "`nPress Enter to exit"
    exit 1
}

# Step 3: Check project files
Write-Step "[3/6] Checking project files..."
if (!(Test-Path "requirements.txt")) {
    Write-Error-Custom "requirements.txt not found"
    Write-ColorText "Make sure you run this script from the pedestrian_simulation directory" "Yellow"
    Read-Host "`nPress Enter to exit"
    exit 1
}

$requiredFiles = @(
    "core\pedestrian_model.py",
    "server\app.py",
    "visualization\visualizer.py",
    "start.py",
    "init_project.py"
)

$missingFiles = @()
foreach ($file in $requiredFiles) {
    if (!(Test-Path $file)) {
        $missingFiles += $file
    }
}

if ($missingFiles.Count -gt 0) {
    Write-Error-Custom "Missing files:"
    foreach ($file in $missingFiles) {
        Write-Host "  - $file" -ForegroundColor Red
    }
    Read-Host "`nPress Enter to exit"
    exit 1
}

Write-Success "Project files complete"

# Step 4: Virtual environment setup (optional)
Write-Step "[4/6] Virtual environment setup..."
$useVenv = Read-Host "Create virtual environment? (Recommended) [Y/n]"
if ($useVenv -eq "" -or $useVenv -eq "Y" -or $useVenv -eq "y") {
    if (Test-Path "venv") {
        Write-Info "Virtual environment already exists"
    } else {
        Write-Host "Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
        if ($LASTEXITCODE -eq 0) {
            Write-Success "Virtual environment created successfully"
        } else {
            Write-Error-Custom "Virtual environment creation failed"
        }
    }
    
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# Step 5: Install dependencies
Write-Step "[5/6] Installing Python dependencies..."
Write-Info "This may take a few minutes..."
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

# Try using Tsinghua mirror
Write-Host "Installing dependency packages..." -ForegroundColor Yellow
$installSuccess = $false

# Try 1: Tsinghua mirror
try {
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --quiet
    if ($LASTEXITCODE -eq 0) {
        $installSuccess = $true
        Write-Success "Dependencies installed successfully (using Tsinghua mirror)"
    }
} catch {
    Write-Info "Tsinghua mirror failed, trying official source..."
}

# Try 2: Official source
if (-not $installSuccess) {
    try {
        pip install -r requirements.txt --quiet
        if ($LASTEXITCODE -eq 0) {
            $installSuccess = $true
            Write-Success "Dependencies installed successfully"
        }
    } catch {
        Write-Error-Custom "Dependency installation failed"
        Read-Host "`nPress Enter to exit"
        exit 1
    }
}

# Step 6: Initialize project
Write-Step "[6/6] Initializing project..."
python init_project.py
if ($LASTEXITCODE -eq 0) {
    Write-Success "Project initialized successfully"
} else {
    Write-Error-Custom "Project initialization failed"
}

# Run tests
Write-Host ""
$runTest = Read-Host "Run system tests? [Y/n]"
if ($runTest -eq "" -or $runTest -eq "Y" -or $runTest -eq "y") {
    Write-Step "Running system tests..."
    python test_system.py
}

# Complete
Write-Host ""
Write-ColorText "========================================" "Green"
Write-ColorText "✓ Installation Complete!" "Green"
Write-ColorText "========================================" "Green"
Write-Host ""

Write-ColorText "Quick Start:" "Cyan"
Write-Host ""
Write-ColorText "1. Start Web Editor:" "Yellow"
Write-Host "   python start.py --web"
Write-ColorText "   Then visit: http://localhost:5000" "Gray"
Write-Host ""

Write-ColorText "2. Run Examples:" "Yellow"
Write-Host "   python start.py --example 1    # Basic evacuation"
Write-Host "   python start.py --example 2    # Fire emergency"
Write-Host ""

Write-ColorText "3. View Documentation:" "Yellow"
Write-Host "   start README.md"
Write-Host "   start QUICK_REFERENCE.md"
Write-Host ""

Write-ColorText "4. Python Programming:" "Yellow"
Write-Host "   python"
Write-Host "   >>> from core.pedestrian_model import SimulationEnvironment"
Write-Host ""

if ($useVenv -eq "" -or $useVenv -eq "Y" -or $useVenv -eq "y") {
    Write-ColorText "Note: When using virtual environment, activate it first:" "Yellow"
    Write-Host "   .\venv\Scripts\Activate.ps1"
    Write-Host ""
}

Write-ColorText "Enjoy! 🎉" "Green"
Write-Host ""

Read-Host "Press Enter to exit"
