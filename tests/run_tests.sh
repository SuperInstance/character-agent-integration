#!/bin/bash
# Bash script to run tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running tests for character-agent-integration${NC}\n"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}pytest is not installed. Install with: pip install pytest${NC}"
    exit 1
fi

# Parse command line arguments
TEST_TYPE=${1:-all}

case $TEST_TYPE in
    unit)
        echo -e "${YELLOW}Running unit tests...${NC}"
        pytest -m unit -v
        ;;
    integration)
        echo -e "${YELLOW}Running integration tests...${NC}"
        pytest -m integration -v
        ;;
    coverage)
        echo -e "${YELLOW}Running tests with coverage...${NC}"
        pytest --cov=character_agent_integration --cov-report=term-missing --cov-report=html -v
        echo -e "${GREEN}Coverage report generated in htmlcov/${NC}"
        ;;
    fast)
        echo -e "${YELLOW}Running fast tests only...${NC}"
        pytest -m "not slow" -v
        ;;
    all)
        echo -e "${YELLOW}Running all tests...${NC}"
        pytest -v --cov=character_agent_integration --cov-report=term-missing
        ;;
    *)
        echo -e "${RED}Unknown test type: $TEST_TYPE${NC}"
        echo "Usage: ./run_tests.sh [unit|integration|coverage|fast|all]"
        exit 1
        ;;
esac

echo -e "\n${GREEN}Tests completed!${NC}"
