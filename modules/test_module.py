from __future__ import annotations

import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import psycopg2
from fastapi import APIRouter, HTTPException
from neo4j import GraphDatabase
from pydantic import BaseModel, Field


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

MODULE_NAME = "test_module"


# =========================================================
# FastAPI Router
# =========================================================

router = APIRouter(prefix="/modules/test-module", tags=["test-module"])


# =========================================================
# Pydantic Models
# =========================================================

class TestModuleBootstrapResponse(BaseModel):
    success: bool
    message: str


class TestModuleRunRequest(BaseModel):
    module_key: str = Field(default="demo_module")
    title: str = Field(default="Graphmaster Test Module Run")
    description: str = Field(default="This run validates PostgreSQL, Neo4j, REST, and GraphQL integration.")
    domain_name: str = Field(default="TestDomain")
    ifc_class_name: str = Field(default="IfcBoiler")
    property_set_name: str = Field(default="Pset_BoilerCommon")
    property_name: str = Field(default="NominalPower")
    constraint_name: str = Field(default="MustExist")


class TestModuleRunResponse(BaseModel):
    success: bool
    run_id: str
    postgres_written: bool
    neo4j_written: bool
    message: str


class TestModuleStatusResponse(BaseModel):
    success: bool
    run_id: str
    postgres: Dict[str, Any]
    neo4j: Dict[str, Any]


class TestModuleCleanupResponse(BaseModel):
    success: bool
    run_id: str
    postgres_deleted: bool
    neo4j_deleted: bool
    message: str


# =========================================================
# Database Helpers
# =========================================================

def get_postgres_connection():
    return psycopg2.connect(**POSTGRES_CONFIG)


def get_neo4j_driver():
    return GraphDatabase.driver(
        NEO4J_URI,
        auth=(NEO4J_USER, NEO4J_PASSWORD),
    )


# =========================================================
# PostgreSQL Setup
# =========================================================

def bootstrap_postgres() -> None:
    sql_statements = [
        """
        CREATE TABLE IF NOT EXISTS gm_modules (
            module_id SERIAL PRIMARY KEY,
            module_key VARCHAR(255) UNIQUE NOT NULL,
            module_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS gm_module_runs (
            run_id UUID PRIMARY KEY,
            module_key VARCHAR(255) NOT NULL,
            title VARCHAR(500) NOT NULL,
            description TEXT,
            status VARCHAR(50) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (module_key) REFERENCES gm_modules(module_key) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS gm_module_run_payloads (
            payload_id SERIAL PRIMARY KEY,
            run_id UUID NOT NULL,
            payload_json JSONB NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (run_id) REFERENCES gm_module_runs(run_id) ON DELETE CASCADE
        );
        """,
    ]

    conn = get_postgres_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                for statement in sql_statements:
                    cur.execute(statement)

                cur.execute(
                    """
                    INSERT INTO gm_modules (module_key, module_name)
                    VALUES (%s, %s)
                    ON CONFLICT (module_key) DO NOTHING
                    """,
                    (MODULE_NAME, "Graphmaster Test Module"),
                )
    finally:
        conn.close()


# =========================================================
# Neo4j Setup
# =========================================================

def bootstrap_neo4j() -> None:
    queries = [
        "CREATE CONSTRAINT test_run_id IF NOT EXISTS FOR (r:TestRun) REQUIRE r.run_id IS UNIQUE",
        "CREATE CONSTRAINT test_domain_name IF NOT EXISTS FOR (d:Domain) REQUIRE d.name IS UNIQUE",
        "CREATE CONSTRAINT test_ifc_class_name IF NOT EXISTS FOR (c:IFCClass) REQUIRE c.name IS UNIQUE",
        "CREATE CONSTRAINT test_pset_name IF NOT EXISTS FOR (p:PropertySet) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT test_property_name IF NOT EXISTS FOR (p:Property) REQUIRE p.name IS UNIQUE",
        "CREATE CONSTRAINT test_constraint_name IF NOT EXISTS FOR (c:Constraint) REQUIRE c.name IS UNIQUE",
    ]

    driver = get_neo4j_driver()
    try:
        with driver.session() as session:
            for query in queries:
                session.run(query)
    finally:
        driver.close()


# =========================================================
# Business Logic
# =========================================================

def run_test_module(payload: TestModuleRunRequest) -> TestModuleRunResponse:
    run_id = str(uuid.uuid4())
    created_at = datetime.now(timezone.utc).isoformat()

    postgres_written = False
    neo4j_written = False

    # ---------- PostgreSQL ----------
    conn = get_postgres_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO gm_modules (module_key, module_name)
                    VALUES (%s, %s)
                    ON CONFLICT (module_key) DO NOTHING
                    """,
                    (payload.module_key, payload.title),
                )

                cur.execute(
                    """
                    INSERT INTO gm_module_runs (run_id, module_key, title, description, status)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (run_id, payload.module_key, payload.title, payload.description, "SUCCESS"),
                )

                cur.execute(
                    """
                    INSERT INTO gm_module_run_payloads (run_id, payload_json)
                    VALUES (%s, %s::jsonb)
                    """,
                    (
                        run_id,
                        (
                            f'{{'
                            f'"module_key":"{payload.module_key}",'
                            f'"title":"{payload.title}",'
                            f'"description":"{payload.description}",'
                            f'"domain_name":"{payload.domain_name}",'
                            f'"ifc_class_name":"{payload.ifc_class_name}",'
                            f'"property_set_name":"{payload.property_set_name}",'
                            f'"property_name":"{payload.property_name}",'
                            f'"constraint_name":"{payload.constraint_name}",'
                            f'"created_at":"{created_at}"'
                            f'}}'
                        ),
                    ),
                )
                postgres_written = True
    finally:
        conn.close()

    # ---------- Neo4j ----------
    driver = get_neo4j_driver()
    try:
        with driver.session() as session:
            session.run(
                """
                MERGE (r:TestRun {run_id: $run_id})
                SET r.module_key = $module_key,
                    r.title = $title,
                    r.description = $description,
                    r.created_at = $created_at

                MERGE (d:Domain {name: $domain_name})
                MERGE (c:IFCClass {name: $ifc_class_name})
                MERGE (ps:PropertySet {name: $property_set_name})
                MERGE (p:Property {name: $property_name})
                MERGE (co:Constraint {name: $constraint_name})

                MERGE (r)-[:USES_DOMAIN]->(d)
                MERGE (d)-[:HAS_CLASS]->(c)
                MERGE (c)-[:HAS_PROPERTYSET]->(ps)
                MERGE (ps)-[:HAS_PROPERTY]->(p)
                MERGE (p)-[:HAS_CONSTRAINT]->(co)
                """,
                {
                    "run_id": run_id,
                    "module_key": payload.module_key,
                    "title": payload.title,
                    "description": payload.description,
                    "created_at": created_at,
                    "domain_name": payload.domain_name,
                    "ifc_class_name": payload.ifc_class_name,
                    "property_set_name": payload.property_set_name,
                    "property_name": payload.property_name,
                    "constraint_name": payload.constraint_name,
                },
            )
            neo4j_written = True
    finally:
        driver.close()

    return TestModuleRunResponse(
        success=True,
        run_id=run_id,
        postgres_written=postgres_written,
        neo4j_written=neo4j_written,
        message="Test module run completed successfully.",
    )


def get_test_module_status(run_id: str) -> TestModuleStatusResponse:
    postgres_data: Dict[str, Any] = {}
    neo4j_data: Dict[str, Any] = {}

    # ---------- PostgreSQL ----------
    conn = get_postgres_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT run_id, module_key, title, description, status, created_at
                    FROM gm_module_runs
                    WHERE run_id = %s
                    """,
                    (run_id,),
                )
                row = cur.fetchone()

                if not row:
                    raise HTTPException(status_code=404, detail=f"Run {run_id} not found in PostgreSQL.")

                postgres_data = {
                    "run_id": str(row[0]),
                    "module_key": row[1],
                    "title": row[2],
                    "description": row[3],
                    "status": row[4],
                    "created_at": row[5].isoformat() if row[5] else None,
                }
    finally:
        conn.close()

    # ---------- Neo4j ----------
    driver = get_neo4j_driver()
    try:
        with driver.session() as session:
            result = session.run(
                """
                MATCH (r:TestRun {run_id: $run_id})-[:USES_DOMAIN]->(d:Domain)-[:HAS_CLASS]->(c:IFCClass)
                      -[:HAS_PROPERTYSET]->(ps:PropertySet)-[:HAS_PROPERTY]->(p:Property)
                      -[:HAS_CONSTRAINT]->(co:Constraint)
                RETURN r.run_id AS run_id,
                       r.module_key AS module_key,
                       r.title AS title,
                       d.name AS domain_name,
                       c.name AS ifc_class_name,
                       ps.name AS property_set_name,
                       p.name AS property_name,
                       co.name AS constraint_name
                """,
                {"run_id": run_id},
            )
            record = result.single()

            if not record:
                raise HTTPException(status_code=404, detail=f"Run {run_id} not found in Neo4j.")

            neo4j_data = {
                "run_id": record["run_id"],
                "module_key": record["module_key"],
                "title": record["title"],
                "domain_name": record["domain_name"],
                "ifc_class_name": record["ifc_class_name"],
                "property_set_name": record["property_set_name"],
                "property_name": record["property_name"],
                "constraint_name": record["constraint_name"],
            }
    finally:
        driver.close()

    return TestModuleStatusResponse(
        success=True,
        run_id=run_id,
        postgres=postgres_data,
        neo4j=neo4j_data,
    )


def cleanup_test_module(run_id: str) -> TestModuleCleanupResponse:
    postgres_deleted = False
    neo4j_deleted = False

    # ---------- PostgreSQL ----------
    conn = get_postgres_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM gm_module_run_payloads WHERE run_id = %s", (run_id,))
                cur.execute("DELETE FROM gm_module_runs WHERE run_id = %s", (run_id,))
                postgres_deleted = True
    finally:
        conn.close()

    # ---------- Neo4j ----------
    driver = get_neo4j_driver()
    try:
        with driver.session() as session:
            session.run(
                """
                MATCH (r:TestRun {run_id: $run_id})
                DETACH DELETE r
                """,
                {"run_id": run_id},
            )
            neo4j_deleted = True
    finally:
        driver.close()

    return TestModuleCleanupResponse(
        success=True,
        run_id=run_id,
        postgres_deleted=postgres_deleted,
        neo4j_deleted=neo4j_deleted,
        message="Test module cleanup completed successfully.",
    )


# =========================================================
# REST Endpoints
# =========================================================

@router.post("/bootstrap", response_model=TestModuleBootstrapResponse)
def bootstrap_test_module():
    try:
        bootstrap_postgres()
        bootstrap_neo4j()
        return TestModuleBootstrapResponse(
            success=True,
            message="Test module bootstrap completed successfully.",
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.post("/run", response_model=TestModuleRunResponse)
def execute_test_module(payload: TestModuleRunRequest):
    try:
        return run_test_module(payload)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/status/{run_id}", response_model=TestModuleStatusResponse)
def read_test_module_status(run_id: str):
    try:
        return get_test_module_status(run_id)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.delete("/cleanup/{run_id}", response_model=TestModuleCleanupResponse)
def delete_test_module_run(run_id: str):
    try:
        return cleanup_test_module(run_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

from modules.registry import register_module

register_module("test_module", router)
