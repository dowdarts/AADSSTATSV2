@echo off
title STEP 3 - Admin Control Panel
echo ========================================
echo   STEP 3: Opening Admin Control Panel
echo ========================================
echo.
echo This will open the Admin Panel in your browser.
echo.
echo WORKFLOW:
echo   1. Review scraped data in staging table
echo   2. Click any cell to edit (if needed)
echo   3. Click "Approve" to move to production
echo   4. Click "Reject" to delete
echo.
echo Opening in 3 seconds...
echo.
timeout /t 3 /nobreak >nul

start "" "%~dp0aads-stats-v2\admin\control-panel.html"

echo.
echo Admin Panel opened in your browser!
echo You can close this window.
echo.
pause
