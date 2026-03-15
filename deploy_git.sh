#!/usr/bin/env bash

echo "======================================"
echo " Graphmaster Git Deploy"
echo "======================================"

cd /opt/graphmaster || exit

echo ""
echo "Git status:"
git status

echo ""
echo "Adding files..."
git add .

echo ""
echo "Commit message:"
read -r message

git commit -m "$message"

echo ""
echo "Pushing to GitHub..."
git push

echo ""
echo "Deploy finished"
echo "======================================"
