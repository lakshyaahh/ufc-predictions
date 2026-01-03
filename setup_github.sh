#!/bin/bash
# GitHub Setup Script for UFC Predictions (macOS/Linux)

echo ""
echo "===== UFC PREDICTIONS - GITHUB SETUP ====="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "ERROR: Git is not installed. Please install Git from https://git-scm.com"
    exit 1
fi

# Navigate to project root
cd "$(dirname "$0")"

echo "[1/5] Initializing git repository..."
if [ -d .git ]; then
    echo "Git repo already initialized."
else
    git init
    echo "✓ Git repository initialized"
fi

echo ""
echo "[2/5] Adding files to git..."
git add .
echo "✓ Files staged"

echo ""
echo "[3/5] Creating initial commit..."
git commit -m "Initial commit: UFC Predictions Web App - Ready for deployment"
echo "✓ Initial commit created"

echo ""
echo "[4/5] GitHub Setup Instructions"
echo "=============================="
echo ""
echo "1. Go to https://github.com/new"
echo "2. Create new repository named: ufc-predictions"
echo "3. Copy the repository URL (https://github.com/YOUR_USERNAME/ufc-predictions.git)"
echo "4. Run these commands:"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/ufc-predictions.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "After pushing to GitHub, your repo will be ready for Render/Vercel deployment!"
echo ""

echo ""
echo "[5/5] Repository Status"
echo "======================"
git status
echo ""
echo "✓ Setup complete! Follow the instructions above to push to GitHub."
echo ""
