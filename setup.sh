#!/bin/bash
# UFC Predictor SaaS - Quick Start Script
# Run this from the project root directory

echo "🥊 UFC Predictor SaaS - Quick Start"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Error: Run this from the project root directory (UFC PREDICTIONS)"
    exit 1
fi

echo -e "${BLUE}Step 1: Setting up Backend${NC}"
echo "Creating virtual environment..."
cd backend

if [ ! -d "venv" ]; then
    python -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate venv based on OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
echo "✅ Dependencies installed"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Edit .env with your Stripe keys:"
    echo "   - STRIPE_SECRET_KEY (from Stripe Dashboard)"
    echo "   - STRIPE_PUBLISHABLE_KEY (from Stripe Dashboard)"
    echo ""
fi

cd ..

echo ""
echo -e "${BLUE}Step 2: Setting up Frontend${NC}"
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install > /dev/null 2>&1
    echo "✅ Node dependencies installed"
fi

# Check if .env.local exists
if [ ! -f ".env.local" ]; then
    echo "Creating .env.local file..."
    cat > .env.local << 'EOF'
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_STRIPE_KEY=pk_test_your_key_here
EOF
    echo "⚠️  Update .env.local with your Stripe publishable key (pk_test_...)"
fi

cd ..

echo ""
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo ""
echo "To start the development servers:"
echo ""
echo "Terminal 1 - Backend:"
echo "  cd backend"
echo "  source venv/bin/activate  (or: venv\\Scripts\\activate on Windows)"
echo "  python -m uvicorn app.main:app --reload --port 8000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Then visit: http://localhost:3000"
echo ""
echo "📚 Documentation:"
echo "  - FREEMIUM_SAAS_GUIDE.md - Complete implementation guide"
echo "  - TEST_GUIDE.md - Testing instructions"
echo "  - IMPLEMENTATION_SUMMARY.md - File changes summary"
echo ""
