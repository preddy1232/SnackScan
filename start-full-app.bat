@echo off
echo Starting SnackScan Full Application...
echo.

echo This will start both the Python backend and React frontend.
echo Make sure you have Python 3.8+ and Node.js installed.
echo.
pause

REM Start backend in a new window
echo Starting Python Backend...
start "SnackScan Backend" cmd /k "%~dp0start-backend.bat"

REM Wait a bit for backend to start
timeout /t 3 /nobreak >nul

REM Start frontend in a new window  
echo Starting React Frontend...
start "SnackScan Frontend" cmd /k "%~dp0start-frontend.bat"

echo.
echo Both services are starting in separate windows:
echo - Backend API: http://127.0.0.1:5000
echo - Frontend App: http://localhost:3000
echo.
echo Close this window or press any key to exit...
pause >nul