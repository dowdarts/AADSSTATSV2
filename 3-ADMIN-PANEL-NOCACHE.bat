@echo off
echo ===============================================
echo AADS Admin Panel - Cache Clearing Mode
echo ===============================================
echo.
echo IMPORTANT: To ensure you see the latest version:
echo 1. Close ALL browser windows completely
echo 2. Wait 3 seconds
echo 3. Press any key to open admin panel
echo.
echo If you still see errors after opening:
echo - Press Ctrl+Shift+R (hard refresh)
echo - Or press F12, then right-click refresh and select "Empty Cache and Hard Reload"
echo.
pause

REM Open with cache disabled flag - use PowerShell Start-Process
powershell -Command "Start-Process chrome -ArgumentList '--disable-application-cache','--disable-cache','--incognito','file:///%CD:\=/%/aads-stats-v2/admin/control-panel.html'"

echo.
echo Browser opened with cache disabled!
echo.
echo If errors persist:
echo 1. Close browser completely
echo 2. Clear all browsing data (Ctrl+Shift+Delete)
echo 3. Run this batch file again
echo.
pause
