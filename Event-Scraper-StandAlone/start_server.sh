#!/bin/bash
# Event Scraper Startup Script for Linux/Mac
# This script starts the Event Scraper API server

echo "========================================"
echo "Event Scraper API Server"
echo "========================================"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "WARNING: Virtual environment not found"
    echo "Run: python3 -m venv venv"
    echo "     source venv/bin/activate"
    echo "     pip install -r requirements.txt"
    echo ""
fi

# Check if dependencies are installed
python -c "import flask" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "ERROR: Flask not found"
    echo "Please install dependencies: pip install -r requirements.txt"
    exit 1
fi

echo "Starting API server..."
echo "Server will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python api_server.py
