#!/bin/bash
#
# Capstone Agents - Cursor IDE Import Script
#
# This script generates a .cursorrules file with all Capstone agents
# for use in Cursor IDE.
#
# Usage:
#   ./import.sh /path/to/your/project
#   ./import.sh /path/to/your/project --roles coordinator,frontend,backend
#   ./import.sh /path/to/your/project --planning-only
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GENERATOR="$SCRIPT_DIR/generate_cursorrules.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}"
    echo "╔═══════════════════════════════════════════════════════════════╗"
    echo "║         Capstone Agents - Cursor IDE Integration              ║"
    echo "╚═══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_usage() {
    echo "Usage: $0 <workspace> [options]"
    echo ""
    echo "Arguments:"
    echo "  <workspace>          Path to your project workspace"
    echo ""
    echo "Options:"
    echo "  --roles <list>       Comma-separated roles (e.g., coordinator,frontend,backend)"
    echo "  --planning-only      Only include planning agents"
    echo "  --impl-only          Only include implementation agents"
    echo "  --dry-run            Preview without writing file"
    echo "  --help               Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 /path/to/your/project"
    echo "  $0 . --roles coordinator,frontend,backend"
    echo "  $0 ~/my-app --planning-only"
    echo ""
}

# Check for help flag first
for arg in "$@"; do
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        print_header
        print_usage
        exit 0
    fi
done

print_header

# Check if workspace argument provided
if [ -z "$1" ]; then
    echo -e "${RED}Error: Workspace path is required${NC}"
    echo ""
    print_usage
    exit 1
fi

WORKSPACE="$1"
shift  # Remove workspace from arguments

# Check if workspace exists
if [ ! -d "$WORKSPACE" ]; then
    echo -e "${RED}Error: Workspace does not exist: $WORKSPACE${NC}"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is required but not found${NC}"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Use python3 if available, otherwise python
PYTHON="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON="python"
fi

# Check if generator script exists
if [ ! -f "$GENERATOR" ]; then
    echo -e "${RED}Error: Generator script not found: $GENERATOR${NC}"
    exit 1
fi

# Run the generator
echo -e "${YELLOW}Generating .cursorrules for: $WORKSPACE${NC}"
echo ""

$PYTHON "$GENERATOR" --workspace "$WORKSPACE" "$@"

EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Success! Capstone agents are ready to use in Cursor IDE${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo ""
    echo "Quick Start:"
    echo "  1. Open workspace in Cursor:"
    echo -e "     ${BLUE}cursor $WORKSPACE${NC}"
    echo ""
    echo "  2. Start chatting with agents:"
    echo "     @Coordinator - Project planning and task delegation"
    echo "     @Frontend    - UI development"
    echo "     @Backend     - API and server-side logic"
    echo "     @DevOps      - Infrastructure and CI/CD"
    echo ""
    echo "  3. For implementation agents, add 'impl':"
    echo "     @Frontend impl - Frontend implementation"
    echo "     @Backend impl  - Backend implementation"
    echo ""
else
    echo -e "${RED}Error: Failed to generate .cursorrules${NC}"
    exit $EXIT_CODE
fi


