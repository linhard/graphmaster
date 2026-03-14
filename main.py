from fastapi import FastAPI
from neo4j import GraphDatabase
import psycopg2
import strawberry
from strawberry.fastapi import GraphQLRouter


# ------------------------------------------------
# FastAPI App
# ------------------------------------------------

app = FastAPI(title="Graphmaster API")


# ------------------------------------------------
# Configuration
# ------------------------------------------------

POSTGRES_CONFIG = {
    "host": "127.0.0.1",
    "port": 5432,
    "database": "graphmaster",
    "user": "graphmaster",
    "password": "graphmaster"
}

NEO4J_URI = "bolt://127.0.0.1:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "graphmaster"


# ------------------------------------------------
# Health Checks
# ------------------------------------------------

def check_postgres():
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        conn.close()
        return True
    except Exception as e:
        return str(e)


def check_neo4j():
    try:
        driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD)
        )
        driver.verify_connectivity()
        driver.close()
        return True
    except Exception as e:
        return str(e)


# ------------------------------------------------
# REST Endpoints
# ------------------------------------------------

@app.get("/")
def root():
    return {
        "service": "graphmaster",
        "status": "running"
    }


@app.get("/health")
def health():

    postgres = check_postgres()
    neo4j = check_neo4j()

    return {
        "service": "graphmaster",
        "postgres": postgres,
        "neo4j": neo4j
    }


# ------------------------------------------------
# GraphQL Schema
# ------------------------------------------------

@strawberry.type
class Query:

    @strawberry.field
    def hello(self) -> str:
        return "Graphmaster GraphQL running"

    @strawberry.field
    def neo4j_test(self) -> str:
        try:
            driver = GraphDatabase.driver(
                NEO4J_URI,
                auth=(NEO4J_USER, NEO4J_PASSWORD)
            )

            with driver.session() as session:
                result = session.run("RETURN 'Neo4j connected' AS message")
                record = result.single()

            driver.close()

            return record["message"]

        except Exception as e:
            return str(e)


schema = strawberry.Schema(query=Query)


# ------------------------------------------------
# GraphQL Router
# ------------------------------------------------

graphql_app = GraphQLRouter(schema)

app.include_router(graphql_app, prefix="/graphql")
