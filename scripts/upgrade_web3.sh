#!/usr/bin/env bash
#
# Automated upgrade script for web3.py v7 migration
# 
# This script will:
# 1. Backup current installation
# 2. Upgrade dependencies
# 3. Run migration tests
# 4. Verify functionality
#
# Usage: bash scripts/upgrade_web3.sh

set -e  # Exit on error

echo "================================"
echo "AirdropFarm - Web3.py v7 Upgrade"
echo "================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0;0m' # No Color

# Check if running in virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}WARNING: Not running in a virtual environment${NC}"
    echo "It's recommended to use a virtual environment."
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
fi

# Step 1: Backup current requirements
echo "[1/6] Creating backup of current installation..."
if [ -f "requirements.txt" ]; then
    cp requirements.txt requirements.txt.backup.$(date +%Y%m%d_%H%M%S)
    echo -e "${GREEN}✓ Backup created${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi
echo ""

# Step 2: Upgrade pip and setuptools
echo "[2/6] Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel
echo -e "${GREEN}✓ Pip upgraded${NC}"
echo ""

# Step 3: Install new dependencies
echo "[3/6] Installing updated dependencies..."
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependencies installed${NC}"
echo ""

# Step 4: Verify web3.py version
echo "[4/6] Verifying web3.py version..."
WEB3_VERSION=$(python -c "import web3; print(web3.__version__)")
if [[ "$WEB3_VERSION" == 7.* ]]; then
    echo -e "${GREEN}✓ Web3.py v$WEB3_VERSION installed successfully${NC}"
else
    echo -e "${RED}✗ Unexpected web3.py version: $WEB3_VERSION${NC}"
    exit 1
fi
echo ""

# Step 5: Run migration tests
echo "[5/6] Running migration tests..."
if [ -f "scripts/test_migration.py" ]; then
    python scripts/test_migration.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Migration tests passed${NC}"
    else
        echo -e "${RED}✗ Migration tests failed${NC}"
        echo "Review the errors above and check MIGRATION.md for guidance."
        exit 1
    fi
else
    echo -e "${YELLOW}⚠ Test script not found, skipping tests${NC}"
fi
echo ""

# Step 6: Final verification
echo "[6/6] Final verification..."
echo "Checking Python version..."
PYTHON_VERSION=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Python version: $PYTHON_VERSION"

if (( $(echo "$PYTHON_VERSION >= 3.9" | bc -l) )); then
    echo -e "${GREEN}✓ Python version compatible${NC}"
else
    echo -e "${RED}✗ Python 3.9+ required, found $PYTHON_VERSION${NC}"
    exit 1
fi
echo ""

echo "================================"
echo -e "${GREEN}Upgrade Complete!${NC}"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Review MIGRATION.md for code changes"
echo "2. Test your specific workflows"
echo "3. Update any custom integrations"
echo ""
echo "If you encounter issues:"
echo "- Check logs for specific errors"
echo "- Review WEB3_V7_CHANGES.md"
echo "- Restore backup: pip install -r requirements.txt.backup.*"
echo ""
