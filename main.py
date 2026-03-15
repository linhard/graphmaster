from __future__ import annotations

import os

import psycopg2
import strawberry
from fastapi import FastAPI
from neo4j import GraphDatabase
from strawberry.fastapi import GraphQLRouter

# Module Engine
from modules.loader import load_modules, get_modules


# =========================================================
# App
# =========================================================

app = FastAPI(
    title="Graphmaster API",
    description="Semantic BIM Requirement Engine",
    version="0.1.0"
)


# =========================================================
# Configuration
# =========================================================

POSTGRES_CONFIG = {
    "host": os.getenv("POSTGRES_HOST", "127.0.0.1"),
    "port": int(os.getenv("POSTGRES_PORT", "5432")),
    "database": os.getenv("POSTGRES_DB", "graphmaster"),
    "user": os.getenv("POSTGRES_USER", "graphmaster"),
    "password": os.getenv("POSTGRES_PASSWORD", "graphmaster"),
}

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://127.0.0.1:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "graphmaster")


# =========================================================
# Health Checks
# =========================================================

def check_postgres():
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        conn.close()
        return True
    except Exception as exc:
        return str(exc)


def check_neo4j():
    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
        )
        driver.verify_connectivity()
        driver.close()
        return True
    except Exception as exc:
        return str(exc)


# =========================================================
# REST Endpoints
# =========================================================

@app.get("/")
def root():
    return {
        "service": "graphmaster",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "service": "graphmaster",
        "postgres": check_postgres(),
        "neo4j": check_neo4j()
    }



from modules.registry import get_registered_modules


@app.get("/system/modules")
def list_loaded_modules():
    modules = get_registered_modules()

    return {
        "loaded_modules": list(modules.keys()),
        "count": len(modules)
    }																									







# =========================================================
# Module Engine
# =========================================================

# Load modules dynamically
load_modules()

# Register module routers
modules = get_modules()

for name, router in modules.items():
    app.include_router(router)


# =========================================================
# GraphQL Schema
# =========================================================

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Graphmaster GraphQL API running"

    @strawberry.field
    def system(self) -> str:
        return "Graphmaster backend stack"


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
