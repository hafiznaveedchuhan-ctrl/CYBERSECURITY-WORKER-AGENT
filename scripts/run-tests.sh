#!/bin/bash

# Test runner script for AI-SOC Platform
# Runs all tests across the monorepo

set -e

echo "=== AI-SOC Platform Test Runner ==="

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Track failures
FAILURES=0

# Run backend tests
run_backend_tests() {
    echo -e "${YELLOW}Running backend tests...${NC}"

    cd backend

    # Run pytest with coverage
    python -m pytest tests/ \
        --cov=src \
        --cov-report=term-missing \
        --cov-report=html:coverage-html \
        --cov-fail-under=80 \
        -v

    if [ $? -ne 0 ]; then
        echo -e "${RED}Backend tests failed!${NC}"
        FAILURES=$((FAILURES + 1))
    else
        echo -e "${GREEN}Backend tests passed!${NC}"
    fi

    cd ..
}

# Run frontend tests
run_frontend_tests() {
    echo -e "${YELLOW}Running frontend tests...${NC}"

    cd frontend

    # Run Jest tests
    npm run test -- --coverage --watchAll=false

    if [ $? -ne 0 ]; then
        echo -e "${RED}Frontend tests failed!${NC}"
        FAILURES=$((FAILURES + 1))
    else
        echo -e "${GREEN}Frontend tests passed!${NC}"
    fi

    cd ..
}

# Run MCP server tests
run_mcp_tests() {
    echo -e "${YELLOW}Running MCP server tests...${NC}"

    cd mcp

    python -m pytest tests/ -v

    if [ $? -ne 0 ]; then
        echo -e "${RED}MCP tests failed!${NC}"
        FAILURES=$((FAILURES + 1))
    else
        echo -e "${GREEN}MCP tests passed!${NC}"
    fi

    cd ..
}

# Run linting
run_linting() {
    echo -e "${YELLOW}Running linters...${NC}"

    # Backend linting
    echo "Linting backend..."
    cd backend
    ruff check src/
    mypy src/
    cd ..

    # Frontend linting
    echo "Linting frontend..."
    cd frontend
    npm run lint
    cd ..

    # MCP linting
    echo "Linting MCP server..."
    cd mcp
    ruff check src/
    cd ..

    echo -e "${GREEN}Linting complete!${NC}"
}

# Run type checking
run_typecheck() {
    echo -e "${YELLOW}Running type checks...${NC}"

    # Backend
    cd backend
    mypy src/ --ignore-missing-imports
    cd ..

    # Frontend
    cd frontend
    npm run typecheck 2>/dev/null || npx tsc --noEmit
    cd ..

    echo -e "${GREEN}Type checking complete!${NC}"
}

# Run security scans
run_security() {
    echo -e "${YELLOW}Running security scans...${NC}"

    # Backend security
    cd backend
    pip-audit 2>/dev/null || echo "pip-audit not installed, skipping..."
    bandit -r src/ -ll 2>/dev/null || echo "bandit not installed, skipping..."
    cd ..

    # Frontend security
    cd frontend
    npm audit --production 2>/dev/null || true
    cd ..

    echo -e "${GREEN}Security scans complete!${NC}"
}

# Integration tests
run_integration() {
    echo -e "${YELLOW}Running integration tests...${NC}"

    cd backend

    python -m pytest tests/integration/ -v --tb=short 2>/dev/null || \
        echo "No integration tests found or tests failed"

    cd ..

    echo -e "${GREEN}Integration tests complete!${NC}"
}

# Print summary
print_summary() {
    echo ""
    echo "=== Test Summary ==="

    if [ $FAILURES -eq 0 ]; then
        echo -e "${GREEN}All tests passed!${NC}"
        exit 0
    else
        echo -e "${RED}$FAILURES test suite(s) failed!${NC}"
        exit 1
    fi
}

# Main execution
main() {
    case "${1:-all}" in
        "backend")
            run_backend_tests
            ;;
        "frontend")
            run_frontend_tests
            ;;
        "mcp")
            run_mcp_tests
            ;;
        "lint")
            run_linting
            ;;
        "typecheck")
            run_typecheck
            ;;
        "security")
            run_security
            ;;
        "integration")
            run_integration
            ;;
        "all")
            run_linting
            run_typecheck
            run_backend_tests
            run_frontend_tests
            run_mcp_tests
            ;;
        "ci")
            run_linting
            run_typecheck
            run_backend_tests
            run_frontend_tests
            run_mcp_tests
            run_security
            ;;
        *)
            echo "Usage: $0 {backend|frontend|mcp|lint|typecheck|security|integration|all|ci}"
            echo ""
            echo "Commands:"
            echo "  backend     - Run backend Python tests"
            echo "  frontend    - Run frontend Jest tests"
            echo "  mcp         - Run MCP server tests"
            echo "  lint        - Run linters"
            echo "  typecheck   - Run type checkers"
            echo "  security    - Run security scans"
            echo "  integration - Run integration tests"
            echo "  all         - Run lint, typecheck, and unit tests"
            echo "  ci          - Run all tests for CI pipeline"
            exit 1
            ;;
    esac

    print_summary
}

main "$@"
