@echo off
REM Quick deployment script for local network

echo.
echo ============================================
echo  Threat Detection System - Quick Deploy
echo ============================================
echo.

REM Get IP address
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /C:"IPv4"') do set "ip=%%a"
set "ip=%ip: =%"

echo Your Local Network IP: %ip%
echo.
echo Access the application at:
echo   http://%ip%:8000
echo.

REM Check if servers are running
tasklist /FI "IMAGENAME eq python.exe" 2>NUL | find /I /N "python.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] Servers are running
) else (
    echo [WARNING] Servers are not running
    echo Starting servers...
    cd /d C:\Users\Austinsraj\OneDrive\Documents\myproject
    start /B C:/Users/Austinsraj/AppData/Local/Programs/Python/Python314/python.exe app/app.py
    start /B C:/Users/Austinsraj/AppData/Local/Programs/Python/Python314/python.exe server.py
    timeout /t 3
    echo [OK] Servers started
)

echo.
echo ============================================
echo To stop servers: taskkill /F /IM python.exe
echo ============================================
echo.

pause
