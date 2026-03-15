#!/usr/bin/env bash

PROJECT_DIR="/opt/graphmaster"

GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
BLUE="\033[0;34m"
NC="\033[0m"

echo -e "${BLUE}"
echo "=================================================="
echo " Graphmaster Git Diagnostics"
echo "=================================================="
echo -e "${NC}"

echo ""
echo -e "${BLUE}[1] Checking git installation${NC}"

if command -v git > /dev/null
then
    echo -e "${GREEN}git installed:${NC} $(git --version)"
else
    echo -e "${RED}git not installed${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[2] Checking project directory${NC}"

cd $PROJECT_DIR || {
    echo -e "${RED}Project directory not found${NC}"
    exit 1
}

echo "Current directory: $(pwd)"

echo ""
echo -e "${BLUE}[3] Checking git repository${NC}"

if [ -d ".git" ]
then
    echo -e "${GREEN}.git repository exists${NC}"
else
    echo -e "${RED}No git repository found${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}[4] Current branch${NC}"

git branch --show-current

echo ""
echo -e "${BLUE}[5] Git status${NC}"

git status

echo ""
echo -e "${BLUE}[6] Remote configuration${NC}"

git remote -v

echo ""
echo -e "${BLUE}[7] Testing SSH connection to GitHub${NC}"

ssh -T git@github.com 2>&1

echo ""
echo -e "${BLUE}[8] Checking last commits${NC}"

git log --oneline -n 5

echo ""
echo -e "${BLUE}[9] Checking staged files${NC}"

git diff --cached --name-only

echo ""
echo -e "${BLUE}[10] Checking tracked files that should not be tracked${NC}"

for item in venv logs __pycache__ "*.deb" ".env"
do
    git ls-files | grep "$item" && echo -e "${YELLOW}Warning: $item is tracked${NC}"
done

echo ""
echo -e "${BLUE}[11] .gitignore content${NC}"

if [ -f ".gitignore" ]
then
    cat .gitignore
else
    echo -e "${YELLOW}.gitignore not found${NC}"
fi

echo ""
echo -e "${GREEN}"
echo "=================================================="
echo " Git Diagnostics Complete"
echo "=================================================="
echo -e "${NC}"
