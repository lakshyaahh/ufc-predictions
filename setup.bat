@echo off
REM UFC Predictor SaaS - Quick Start Script for Windows
REM Run this from the project root directory

echo.
echo  ========================================
echo  ^^ UFC Predictor SaaS - Quick Start
echo  ========================================
echo.

REM Check if we're in the right directory
if not exist "backend" (
    echo Error: Run this from the project root directory
    pause
    exit /b 1
)

echo Step 1: Setting up Backend
echo.

cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo + Virtual environment created
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1
echo + Dependencies installed

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env > nul
    echo.
    echo ^! IMPORTANT: Edit .env with your Stripe keys:
    echo    - STRIPE_SECRET_KEY ^(from Stripe Dashboard^)
    echo    - STRIPE_PUBLISHABLE_KEY ^(from Stripe Dashboard^)
    echo.
)

cd ..

echo.
echo Step 2: Setting up Frontend
echo.

cd frontend

if not exist "node_modules" (
    echo Installing Node dependencies...
    call npm install > nul 2>&1
    echo + Node dependencies installed
)

REM Check if .env.local exists
if not exist ".env.local" (
    echo Creating .env.local file...
    (
        echo NEXT_PUBLIC_API_URL=http://localhost:8000
        echo NEXT_PUBLIC_STRIPE_KEY=pk_test_your_key_here
    ) > .env.local
    echo.
    echo ^! Update .env.local with your Stripe publishable key
)

cd ..

echo.
echo ========================================
echo + Setup Complete!
echo ========================================
echo.
echo To start the development servers:
echo.
echo Terminal 1 - Backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python -m uvicorn app.main:app --reload --port 8000
echo.
echo Terminal 2 - Frontend:
echo   cd frontend
echo   npm run dev
echo.
echo Then visit: http://localhost:3000
echo.
echo Documentation:
echo   - FREEMIUM_SAAS_GUIDE.md - Complete implementation guide
echo   - TEST_GUIDE.md - Testing instructions
echo   - IMPLEMENTATION_SUMMARY.md - File changes summary
echo.
echo.
pause
