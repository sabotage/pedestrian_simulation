#!/bin/bash
# Pedestrian Simulation Launcher for Linux/Mac

echo "======================================"
echo "Pedestrian Simulation System"
echo "======================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.9 or higher"
    exit 1
fi

echo "Python found!"
echo

# Check if dependencies are installed
echo "Checking dependencies..."
if ! python3 -c "import flask" &> /dev/null; then
    echo "Installing required packages..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "ERROR: Failed to install dependencies"
        exit 1
    fi
else
    echo "Dependencies already installed."
fi

echo
echo "Select an option:"
echo "1. Run Web Application (Interactive)"
echo "2. Run Simple Example (Command Line)"
echo "3. Run Emergency Scenario (Command Line)"
echo "4. Run Tests"
echo "5. Exit"
echo

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        echo
        echo "Starting web application..."
        echo "Open http://localhost:5000 in your browser"
        echo
        cd src/web
        python3 app.py
        ;;
    2)
        echo
        echo "Running simple corridor example..."
        echo
        python3 examples/run_simulation.py --mode simple
        ;;
    3)
        echo
        echo "Running emergency evacuation scenario..."
        echo
        python3 examples/run_simulation.py --mode emergency
        ;;
    4)
        echo
        echo "Running test suite..."
        echo
        python3 tests/test_all.py
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice. Please run again."
        exit 1
        ;;
esac
