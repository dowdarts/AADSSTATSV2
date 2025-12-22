@echo off
REM Event Scraper Startup Script for Windows
REM This script starts the Event Scraper API server

echo ========================================
echo Event Scraper API Server
echo ========================================
echo.

REM Check if virtual environment exists
if exist venv\ (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo WARNING: Virtual environment not found
    echo Run: python -m venv venv
    echo      venv\Scripts\activate
    echo      pip install -r requirements.txt
    echo.
)

REM Check if dependencies are installed
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ERROR: Flask not found
    echo Please install dependencies: pip install -r requirements.txt
    pause
    exit /b 1
)

echo Starting API server...
echo Server will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python api_server.py

pause
