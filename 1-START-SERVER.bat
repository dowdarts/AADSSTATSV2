@echo off
title AADS Stats - API Server Running
color 0A
echo ========================================
echo   AADS STATS V2 - API SERVER
echo ========================================
echo.
echo Server Status: STARTING...
echo Server URL: http://localhost:5000
echo.
echo ========================================
echo   IMPORTANT - KEEP THIS WINDOW OPEN!
echo ========================================
echo.
echo This server must stay running for:
echo   - Event Scraper (Step 2)
echo   - Admin Panel (Step 3)
echo   - Stats Display (Step 4)
echo.
echo To STOP the server:
echo   - Close this window, OR
echo   - Press CTRL+C
echo.
echo ========================================
echo.

cd Event-Scraper-StandAlone
python api_server.py

echo.
echo ========================================
echo   SERVER STOPPED
echo ========================================
pause
