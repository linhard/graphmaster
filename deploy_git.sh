#!/usr/bin/env bash

echo "======================================="
echo "Graphmaster Git Reset & Deploy"
echo "======================================="

PROJECT_DIR="/opt/graphmaster"
REPO_URL="git@github.com:linhakla/graphmaster.git"

cd $PROJECT_DIR || exit

echo ""
echo "Removing old git repository..."

rm -rf .git

echo ""
echo "Initializing new git repository..."

git init

git branch -M main

echo ""
echo "Creating .gitignore..."

cat <<EOF > .gitignore
venv/
logs/
__pycache__/
*.pyc
.env
*.log
EOF

echo ""
echo "Adding remote repository..."

git remote add origin $REPO_URL

echo ""
echo "Adding files..."

git add .

echo ""
echo "Creating initial commit..."

git commit -m "Graphmaster initial deployment"

echo ""
echo "Pushing to GitHub..."

git push -f origin main

echo ""
echo "======================================="
echo "Deploy complete"
echo "======================================="
