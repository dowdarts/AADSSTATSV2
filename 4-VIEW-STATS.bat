@echo off
title STEP 4 - View Public Stats Display
echo ========================================
echo   STEP 4: Opening Stats Display
echo ========================================
echo.
echo This will open the Professional Stats Display.
echo.
echo FEATURES:
echo   - Series Leaderboard
echo   - Event Standings
echo   - Champions History
echo   - Top Performers
echo   - Player Directory
echo.
echo Opening in 3 seconds...
echo.
timeout /t 3 /nobreak >nul

start "" "%~dp0aads-stats-v2\public\index.html"

echo.
echo Stats Display opened in your browser!
echo You can close this window.
echo.
pause
