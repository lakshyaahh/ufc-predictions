"""
Automated Production Deployment Verification Script
Checks all requirements before deployment
"""
import os
import sys
from pathlib import Path

def check_file_exists(path, description):
    """Check if a file exists"""
    if Path(path).exists():
        print(f"✓ {description}")
        return True
    else:
        print(f"✗ {description} - MISSING")
        return False

def check_requirements():
    """Check all deployment requirements"""
    print("=" * 60)
    print("🚀 UFC PREDICTIONS - DEPLOYMENT READINESS CHECK")
    print("=" * 60)
    print()
    
    all_good = True
    
    # Backend checks
    print("BACKEND FILES:")
    all_good &= check_file_exists("backend/app/main.py", "FastAPI main app")
    all_good &= check_file_exists("backend/app/models.py", "Database models")
    all_good &= check_file_exists("backend/app/crud.py", "CRUD operations")
    all_good &= check_file_exists("backend/app/auth.py", "Authentication module")
    all_good &= check_file_exists("backend/app/config.py", "Configuration")
    all_good &= check_file_exists("backend/app/database.py", "Database setup")
    all_good &= check_file_exists("backend/requirements.txt", "Python dependencies")
    all_good &= check_file_exists("backend/Procfile", "Heroku/Render startup config")
    all_good &= check_file_exists("backend/Dockerfile", "Docker container config")
    all_good &= check_file_exists("backend/.env.production", "Production environment template")
    
    # Check if model exists
    if Path("backend/models/ufc_prediction_model.pkl").exists():
        print("✓ ML model file")
    else:
        print("⚠ ML model file - Will be trained on first run")
    
    print()
    print("FRONTEND FILES:")
    all_good &= check_file_exists("frontend/package.json", "Node.js dependencies")
    all_good &= check_file_exists("frontend/next.config.js", "Next.js configuration")
    all_good &= check_file_exists("frontend/pages/index.js", "Home page")
    all_good &= check_file_exists("frontend/pages/auth.js", "Auth page")
    all_good &= check_file_exists("frontend/pages/history.js", "History page")
    all_good &= check_file_exists("frontend/.env.production", "Production environment template")
    
    print()
    print("DEPLOYMENT CONFIG:")
    all_good &= check_file_exists(".gitignore", "Git ignore file")
    all_good &= check_file_exists("QUICK_DEPLOY.md", "Deployment guide")
    
    print()
    print("=" * 60)
    
    if all_good:
        print("✅ ALL CHECKS PASSED - READY FOR DEPLOYMENT!")
        print()
        print("Next steps:")
        print("1. Run: setup_github.bat (Windows) or ./setup_github.sh (macOS/Linux)")
        print("2. Follow QUICK_DEPLOY.md instructions")
        print("3. Deploy to Render (backend) and Vercel (frontend)")
        return 0
    else:
        print("❌ SOME FILES ARE MISSING - CANNOT DEPLOY")
        print()
        print("Please ensure all files exist before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(check_requirements())
