#!/usr/bin/env bash

echo "==========================================="
echo "Stopping Graphmaster"
echo "==========================================="

echo ""
echo "Stopping FastAPI..."

pkill -f "uvicorn main:app"

sleep 2

echo ""
echo "Stopping Neo4j..."

sudo systemctl stop neo4j

echo ""
echo "Stopping PostgreSQL..."

sudo systemctl stop postgresql

echo ""
echo "Graphmaster stopped"
echo "==========================================="
