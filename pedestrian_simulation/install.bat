@echo off
chcp 65001 >nul
echo ========================================
echo Pedestrian Simulation System - Windows Install
echo ========================================
echo.

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X Python not found
    echo.
    echo Please install Python 3.8 or higher
    echo Download from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo + Python is installed
python --version
echo.

REM Check pip
echo [2/5] Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo X pip not found
    pause
    exit /b 1
)
echo + pip is available
echo.

REM Check current directory
echo [3/5] Checking project files...
if not exist "requirements.txt" (
    echo X requirements.txt not found
    echo Please make sure you are running this script from the pedestrian_simulation directory
    pause
    exit /b 1
)
echo + Project files are complete
echo.

REM Install dependencies
echo [4/5] Installing Python dependencies...
echo This may take a few minutes...
echo.

REM Try using Tsinghua mirror first
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if %errorlevel% neq 0 (
    echo.
    echo Mirror failed, trying official source...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo X Dependency installation failed
        pause
        exit /b 1
    )
)
echo + Dependencies installed successfully
echo.

REM Initialize project
echo [5/5] Initializing project...
python init_project.py
if %errorlevel% neq 0 (
    echo X Initialization failed
    pause
    exit /b 1
)
echo.

REM Run tests
echo Running system tests...
python test_system.py
echo.

REM Complete
echo ========================================
echo + Installation Complete!
echo ========================================
echo.
echo Quick Start:
echo   1. Start Web Editor:
echo      python start.py --web
echo.
echo   2. Run Examples:
echo      python start.py --example 1
echo.
echo   3. View Documentation:
echo      start README.md
echo.
echo Press any key to exit...
pause >nul
