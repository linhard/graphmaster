#!/usr/bin/env bash

echo "==========================================="
echo "Starting Graphmaster Stack"
echo "==========================================="

BASE_DIR="/opt/graphmaster"
LOG_DIR="$BASE_DIR/logs"

FASTAPI_PORT=8000
FASTAPI_URL="http://127.0.0.1:$FASTAPI_PORT/health"

# ------------------------------------------------
# Create logs directory
# ------------------------------------------------

mkdir -p $LOG_DIR

# ------------------------------------------------
# Start PostgreSQL
# ------------------------------------------------

echo ""
echo "Checking PostgreSQL..."

if systemctl is-active --quiet postgresql
then
    echo "PostgreSQL already running"
else
    echo "Starting PostgreSQL..."
    sudo systemctl start postgresql
fi

# ------------------------------------------------
# Start Neo4j
# ------------------------------------------------

echo ""
echo "Checking Neo4j..."

if systemctl is-active --quiet neo4j
then
    echo "Neo4j already running"
else
    echo "Starting Neo4j..."
    sudo systemctl start neo4j
fi

echo "Waiting for Neo4j to start..."

for i in {1..30}; do
    if ss -tulnp | grep 7687 > /dev/null
    then
        echo "Neo4j ready"
        break
    fi
    sleep 1
done



# ------------------------------------------------
# Start FastAPI
# ------------------------------------------------

echo ""
echo "Checking FastAPI..."

if curl -s $FASTAPI_URL > /dev/null
then
    echo "FastAPI already running"
else
    echo "Starting FastAPI..."

    cd $BASE_DIR

    source venv/bin/activate

    nohup uvicorn main:app \
        --host 0.0.0.0 \
        --port $FASTAPI_PORT \
        > $LOG_DIR/fastapi.log 2>&1 &

    sleep 5
fi

# ------------------------------------------------
# Final status
# ------------------------------------------------

echo ""
echo "==========================================="
echo "Graphmaster Status"
echo "==========================================="

curl -s $FASTAPI_URL || echo "FastAPI not reachable"

echo ""
echo "Neo4j:"
ss -tulnp | grep 7687 || echo "Neo4j not running"

echo ""
echo "PostgreSQL:"
ss -tulnp | grep 5432 || echo "Postgres not running"

echo ""
echo "Logs:"
echo "$LOG_DIR/fastapi.log"

echo ""
echo "Graphmaster started"
echo "==========================================="
