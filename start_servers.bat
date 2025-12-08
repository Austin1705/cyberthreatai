@echo off
echo Starting Website Security Scanner Servers...
echo.

cd /d "%~dp0"

echo [1/2] Starting Dashboard Server on port 8000...
start "Dashboard Server" python server.py

timeout /t 2 /nobreak

echo [2/2] Starting API Server on port 5001...
start "API Server" python app/app.py

timeout /t 2 /nobreak

echo.
echo ==================================================
echo Servers started successfully!
echo.
echo Dashboard: http://localhost:8000
echo API:       http://localhost:5001
echo Scanner:   http://localhost:8000/scanner.html
echo ==================================================
echo.
echo Press any key to close this window...
pause
