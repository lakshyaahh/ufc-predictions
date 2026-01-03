@echo off
REM GitHub Setup Script for UFC Predictions
REM This script prepares your project for GitHub and deployment

echo.
echo ===== UFC PREDICTIONS - GITHUB SETUP =====
echo.

REM Check if git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Git is not installed. Please install Git from https://git-scm.com
    pause
    exit /b 1
)

REM Navigate to project root
cd /d "%~dp0"

echo [1/5] Initializing git repository...
if exist .git (
    echo Git repo already initialized.
) else (
    git init
    echo ✓ Git repository initialized
)

echo.
echo [2/5] Adding files to git...
git add .
echo ✓ Files staged

echo.
echo [3/5] Creating initial commit...
git commit -m "Initial commit: UFC Predictions Web App - Ready for deployment"
echo ✓ Initial commit created

echo.
echo [4/5] GitHub Setup Instructions
echo ==============================
echo.
echo 1. Go to https://github.com/new
echo 2. Create new repository named: ufc-predictions
echo 3. Copy the repository URL (https://github.com/YOUR_USERNAME/ufc-predictions.git)
echo 4. Run these commands in PowerShell:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/ufc-predictions.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo After pushing to GitHub, your repo will be ready for Render/Vercel deployment!
echo.

echo.
echo [5/5] Repository Status
echo =======================
git status
echo.
echo ✓ Setup complete! Follow the instructions above to push to GitHub.
echo.
pause
