@echo off
REM Resume Checker - Start All Services Script (Windows)

echo =========================================
echo   Resume Checker - Starting Services
echo =========================================
echo.

echo Starting Backend...
cd backend
start /B python app.py
echo [OK] Backend started on port 5000

cd ..
timeout /t 2 /nobreak

echo.
echo Starting Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing npm dependencies...
    call npm install
)

start /B cmd /k npm run dev
echo [OK] Frontend started on port 3000

cd ..

echo.
echo =========================================
echo Services are running!
echo =========================================
echo.
echo Frontend:  http://localhost:3000
echo Backend:   http://localhost:5000
echo.
echo Close the command prompts to stop the services
echo.

pause
