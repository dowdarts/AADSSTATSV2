@echo off
title STEP 2 - Event Scraper
echo ========================================
echo   STEP 2: Opening Event Scraper
echo ========================================
echo.
echo This will open the Event Scraper in your browser.
echo.
echo WORKFLOW:
echo   1. Select Event Number (1-6)
echo   2. Enter DartConnect URL
echo   3. Click "Find Matches"
echo   4. Click "Scrape Match Results" (Stage 1)
echo   5. Click "Scrape Match Details" (Stage 2)
echo   6. Review stats and click "Send to Admin"
echo.
echo Opening in 3 seconds...
echo.
timeout /t 3 /nobreak >nul

start http://localhost:5000/event_scraper.html

echo.
echo Event Scraper opened in your browser!
echo You can close this window.
echo.
pause
