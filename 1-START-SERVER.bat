@echo off
title STEP 1 - Starting Event Scraper API Server
echo ========================================
echo   STEP 1: Starting API Server
echo ========================================
echo.
echo Server will start on http://localhost:5000
echo.
echo IMPORTANT: Keep this window open!
echo Press CTRL+C to stop the server when done.
echo.
echo ========================================
echo.

cd Event-Scraper-StandAlone
python api_server.py

pause
