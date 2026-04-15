#!/bin/bash

# Resume Checker - Start All Services Script

echo "========================================="
echo "  Resume Checker - Starting Services"
echo "========================================="

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if ports are available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo -e "${YELLOW}Warning: Port $1 is already in use${NC}"
        return 1
    fi
    return 0
}

# Check backend port
echo "Checking port 5000..."
check_port 5000

# Check frontend port
echo "Checking port 3000..."
check_port 3000

echo ""
echo -e "${GREEN}Starting Backend...${NC}"
cd backend

# Check if models exist
if [ ! -f "models/svm_model.pkl" ] || [ ! -f "models/tfidf_vectorizer.pkl" ]; then
    echo -e "${YELLOW}Warning: Models not found. Please train them first using the Jupyter notebook.${NC}"
fi

# Start backend in background
python app.py &
BACKEND_PID=$!
echo -e "${GREEN}✓ Backend started (PID: $BACKEND_PID)${NC}"

cd ..

# Wait for backend to start
sleep 2

echo ""
echo -e "${GREEN}Starting Frontend...${NC}"
cd frontend

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install
fi

# Start frontend in background
npm run dev &
FRONTEND_PID=$!
echo -e "${GREEN}✓ Frontend started (PID: $FRONTEND_PID)${NC}"

echo ""
echo "========================================="
echo -e "${GREEN}Both services are running!${NC}"
echo "========================================="
echo ""
echo "Frontend:  http://localhost:3000"
echo "Backend:   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap "kill $BACKEND_PID $FRONTEND_PID; echo 'Services stopped'" EXIT

wait
