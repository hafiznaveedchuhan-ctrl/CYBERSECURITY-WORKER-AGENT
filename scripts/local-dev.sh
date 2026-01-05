#!/bin/bash

# Local development script for AI-SOC Platform
# This script starts all services for local development

set -e

echo "=== AI-SOC Platform Local Development ==="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check prerequisites
check_prerequisites() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"

    # Check Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
        exit 1
    fi

    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}Docker Compose is not installed. Please install Docker Compose first.${NC}"
        exit 1
    fi

    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}Node.js is not installed. Please install Node.js first.${NC}"
        exit 1
    fi

    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}Python 3 is not installed. Please install Python 3 first.${NC}"
        exit 1
    fi

    echo -e "${GREEN}All prerequisites met!${NC}"
}

# Setup environment
setup_env() {
    echo -e "${YELLOW}Setting up environment...${NC}"

    # Create .env file if it doesn't exist
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            echo -e "${YELLOW}Created .env from .env.example. Please update with your values.${NC}"
        else
            echo -e "${RED}.env.example not found. Please create .env file.${NC}"
            exit 1
        fi
    fi

    echo -e "${GREEN}Environment setup complete!${NC}"
}

# Start infrastructure services
start_infra() {
    echo -e "${YELLOW}Starting infrastructure services...${NC}"

    docker-compose up -d postgres qdrant redis

    # Wait for services to be ready
    echo "Waiting for services to be ready..."
    sleep 10

    echo -e "${GREEN}Infrastructure services started!${NC}"
}

# Install dependencies
install_deps() {
    echo -e "${YELLOW}Installing dependencies...${NC}"

    # Frontend
    echo "Installing frontend dependencies..."
    cd frontend && npm install && cd ..

    # Backend
    echo "Installing backend dependencies..."
    cd backend && pip install -e ".[dev]" && cd ..

    # Docs
    echo "Installing docs dependencies..."
    cd docs && npm install && cd ..

    # MCP
    echo "Installing MCP server dependencies..."
    cd mcp && pip install -e ".[dev]" && cd ..

    echo -e "${GREEN}Dependencies installed!${NC}"
}

# Run database migrations
run_migrations() {
    echo -e "${YELLOW}Running database migrations...${NC}"

    cd backend
    alembic upgrade head
    cd ..

    echo -e "${GREEN}Migrations complete!${NC}"
}

# Start all services
start_services() {
    echo -e "${YELLOW}Starting all services...${NC}"

    # Start backend
    echo "Starting backend..."
    cd backend
    uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload &
    BACKEND_PID=$!
    cd ..

    # Start frontend
    echo "Starting frontend..."
    cd frontend
    npm run dev &
    FRONTEND_PID=$!
    cd ..

    # Start docs
    echo "Starting docs..."
    cd docs
    npm run start &
    DOCS_PID=$!
    cd ..

    # Start MCP server
    echo "Starting MCP server..."
    cd mcp
    python -m src.main &
    MCP_PID=$!
    cd ..

    echo -e "${GREEN}All services started!${NC}"
    echo ""
    echo "=== Service URLs ==="
    echo "Frontend: http://localhost:3000"
    echo "Backend API: http://localhost:8000"
    echo "API Docs: http://localhost:8000/docs"
    echo "Textbook: http://localhost:3001"
    echo ""
    echo "Press Ctrl+C to stop all services"

    # Wait for interrupt
    trap cleanup SIGINT SIGTERM
    wait
}

# Cleanup function
cleanup() {
    echo -e "${YELLOW}Stopping services...${NC}"

    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    kill $DOCS_PID 2>/dev/null || true
    kill $MCP_PID 2>/dev/null || true

    echo -e "${GREEN}Services stopped!${NC}"
    exit 0
}

# Main execution
main() {
    case "${1:-}" in
        "prereq")
            check_prerequisites
            ;;
        "setup")
            setup_env
            install_deps
            ;;
        "infra")
            start_infra
            ;;
        "migrate")
            run_migrations
            ;;
        "start")
            start_services
            ;;
        "all"|"")
            check_prerequisites
            setup_env
            start_infra
            install_deps
            run_migrations
            start_services
            ;;
        *)
            echo "Usage: $0 {prereq|setup|infra|migrate|start|all}"
            echo ""
            echo "Commands:"
            echo "  prereq  - Check prerequisites"
            echo "  setup   - Setup environment and install dependencies"
            echo "  infra   - Start infrastructure services (Docker)"
            echo "  migrate - Run database migrations"
            echo "  start   - Start all application services"
            echo "  all     - Run all steps (default)"
            exit 1
            ;;
    esac
}

main "$@"
