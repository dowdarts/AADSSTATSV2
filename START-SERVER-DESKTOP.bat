@echo off
title AADS Stats - Server Launcher
echo ========================================
echo   LAUNCHING API SERVER
echo ========================================
echo.
echo Opening server in new window...
echo The server window will stay open.
echo.
echo Close the GREEN server window to stop.
echo.

start "AADS API Server - KEEP OPEN" /D "%~dp0Event-Scraper-StandAlone" cmd /k "color 0A && echo ======================================== && echo   AADS STATS V2 - API SERVER RUNNING && echo ======================================== && echo. && echo Server URL: http://localhost:5000 && echo. && echo KEEP THIS WINDOW OPEN! && echo Close this window to stop the server. && echo. && echo ======================================== && echo. && python api_server.py"

echo.
echo Server launched in separate window!
echo.
timeout /t 3 /nobreak >nul
exit
