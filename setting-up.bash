#!/bin/bash

# Get the path to python3
PYTHON_PATH=$(which python3)

# Check if python3 is installed
if [ -z "$PYTHON_PATH" ]; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Create the virtual environment
echo "Creating virtual environment..."
$PYTHON_PATH -m venv venv 

# Check if venv was successfully created
if [ ! -d "venv" ]; then
    echo "Failed to create the virtual environment."
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Check if activation was successful
if [ "$VIRTUAL_ENV" == "" ]; then
    echo "Failed to activate the virtual environment."
    exit 1
fi

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Skipping dependency installation."
fi

# Ensure that setting-up.bash has executable permissions
if [ -f "setting-up.bash" ]; then
    if [ ! -x "setting-up.bash" ]; then
        echo "Setting executable permissions on setting-up.bash..."
        chmod +x setting-up.bash
    fi
else
    echo "setting-up.bash not found. Skipping permission setting."
fi

echo "Setup complete."