@echo off
echo Starting SnackScan React Frontend...
echo.

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo Installing Node.js dependencies...
    npm install
)

REM Start the React development server
echo.
echo Starting React development server...
echo Frontend will be available at: http://localhost:3000
echo.
npm start

pause