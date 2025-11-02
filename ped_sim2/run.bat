@echo off
REM Pedestrian Simulation Launcher for Windows

echo ======================================
echo Pedestrian Simulation System
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
) else (
    echo Dependencies already installed.
)

echo.
echo Select an option:
echo 1. Run Web Application (Interactive)
echo 2. Run Simple Example (Command Line)
echo 3. Run Emergency Scenario (Command Line)
echo 4. Run Tests
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo.
    echo Starting web application...
    echo Open http://localhost:5000 in your browser
    echo.
    cd src\web
    python app.py
) else if "%choice%"=="2" (
    echo.
    echo Running simple corridor example...
    echo.
    python examples\run_simulation.py --mode simple
    pause
) else if "%choice%"=="3" (
    echo.
    echo Running emergency evacuation scenario...
    echo.
    python examples\run_simulation.py --mode emergency
    pause
) else if "%choice%"=="4" (
    echo.
    echo Running test suite...
    echo.
    python tests\test_all.py
    pause
) else if "%choice%"=="5" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Please run again.
    pause
    exit /b 1
)
