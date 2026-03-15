# Graphmaster

Graphmaster is a **Semantic BIM Requirement Engine** that transforms natural language BIM use case descriptions into structured information requirements.

The platform combines:

- semantic search
- BIM knowledge graphs
- BIM standards (IFC, IDS, bSDD)
- ontologies
- modular plugins

to discover, instantiate, enrich and validate BIM use cases.

---

# System Vision

Graphmaster aims to become a **Semantic BIM Knowledge Platform** connecting:

- BIM standards
- ontologies
- classification systems
- project requirements
- regulatory frameworks
- digital twins

within a unified semantic knowledge graph.

---

# System Architecture

```mermaid
flowchart TB

User[User Interface]

Query[Natural Language Query]

FastAPI[FastAPI Backend]

GraphQL[GraphQL API]

Neo4j[(Neo4j Knowledge Graph)]

Postgres[(PostgreSQL Database)]

User --> Query
Query --> FastAPI

FastAPI --> GraphQL
FastAPI --> Neo4j
FastAPI --> Postgres

GraphQL --> Neo4j
