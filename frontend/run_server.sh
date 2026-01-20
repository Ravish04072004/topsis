#!/bin/bash

# TOPSIS Web Service Startup Script for Mac/Linux

echo ""
echo "========================================"
echo "TOPSIS Web Service"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo "Python version:"
python3 --version

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed"
    exit 1
fi

# Install dependencies if not already installed
echo ""
echo "Checking dependencies..."

if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "Error: Failed to install dependencies"
        exit 1
    fi
fi

echo ""
echo "✓ All dependencies are installed"
echo ""
echo "Starting server..."
echo ""
echo "========================================"
echo "Server will be available at:"
echo "http://localhost:5000"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py
