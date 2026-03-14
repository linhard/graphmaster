# Graphmaster

Graphmaster is a **Semantic BIM Requirement Engine** that transforms natural language descriptions of BIM use cases into structured information requirements.

The platform combines:

- semantic search
- BIM knowledge graphs
- BIM standards (IFC, IDS, bSDD)
- ontologies
- modular plugins

to discover, instantiate, enrich, and validate BIM use cases.

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

# High-Level Architecture

\`\`\`mermaid
flowchart TB

User[User Interface]

Query[Natural Language Query]

SemanticEngine[Semantic Engine]

ReferenceKnowledge[Reference Knowledge]

Selection[Reference Use Case Selection]

Instantiation[Project Use Case Instantiation]

Plugins[Plugin Modules]

Graph[(Neo4j Knowledge Graph)]

Validation[Validation Engine]

Export[IDS / BCF / Reports]

User --> Query
Query --> SemanticEngine
SemanticEngine --> ReferenceKnowledge
ReferenceKnowledge --> Selection
Selection --> Instantiation
Instantiation --> Plugins
Plugins --> Graph
Graph --> Validation
Validation --> Export
\`\`\`

---

# Core Concept

Graphmaster does **not generate use cases from scratch**.

Instead it relies on **Reference Use Cases** that are stored in the system.

Users describe their requirements in natural language.  
The system performs **semantic similarity search** and suggests relevant reference knowledge.

---

# Reference Use Case Model

Reference Use Cases define the **information structure** but **do not contain constraint values**.

Domain  
→ IFCClass  
→ PropertySet  
→ Property  

Example

Energy Monitoring

Domain  
Energy

IFCClass  
IfcBoiler

PropertySet  
Pset_BoilerCommon

Properties  
EnergyConsumption  
NominalPower  
ThermalEfficiency  

---

# Semantic Search Pipeline

\`\`\`mermaid
flowchart LR

Query[Natural Language Query]

Embedding[Embedding Generation]

VectorSearch[Vector Similarity Search]

Results[Ranked Knowledge Results]

Selection[User Selects Reference Use Case]

Query --> Embedding
Embedding --> VectorSearch
VectorSearch --> Results
Results --> Selection
\`\`\`

---

# Core Data Model

Domain  
→ IFCClass  
→ PropertySet  
→ Property  
→ Constraint  

\`\`\`mermaid
graph TD

UseCase --> Domain
Domain --> IFCClass
IFCClass --> PropertySet
PropertySet --> Property
Property --> Constraint
\`\`\`

---

# Ontology Layer

\`\`\`mermaid
graph TD

Property --> Concept

Concept --> IFCConcept
Concept --> bSDDConcept
Concept --> OntologyConcept
Concept --> Synonym
Concept --> Unit
Concept --> DataType
\`\`\`

---

# Knowledge Graph Structure

Nodes

UseCase  
Domain  
IFCClass  
PropertySet  
Property  
Constraint  
Concept  
Calculation  
BCFIssue  
Module  

Relationships

UseCase → Domain  
Domain → IFCClass  
IFCClass → PropertySet  
PropertySet → Property  
Property → Constraint  
Property → Concept  
Property → Calculation  

---

# Calculations

Example

TotalEnergy = Power * OperatingHours

Graph

Property → Calculation

---

# BCF Integration

Constraint violations can generate BCF issues.

Constraint example

ThermalEfficiency >= 0.85

Violation

IfcBoiler missing value

---

# Plugin Architecture

Example modules

Core  
IFC  
bSDD  
OWL  
IDS  
XLS  
BCF  
BIM4HVAC  
PDF Regulations  

---

# Plugin System

\`\`\`mermaid
flowchart LR

ExternalData[External Data Source]

Plugin[Plugin Module]

Core[Core Engine]

Graph[(Knowledge Graph)]

ExternalData --> Plugin
Plugin --> Core
Core --> Graph
\`\`\`

---

# Technology Stack

API → FastAPI  
Query API → GraphQL  
Knowledge Graph → Neo4j  
Metadata Storage → PostgreSQL  
Vector Search → FAISS / pgvector  
NLP → spaCy  
Embeddings → Sentence Transformers  

---

# Repository Structure

graphmaster/

README.md

core/
engine.py
pipeline.py
graph_model.py
vector_search.py

api/
fastapi_server.py
graphql_schema.py

database/
neo4j_schema.cypher
postgres_schema.sql

modules/

ifc/
bsdd/
owl/
ids/
xls/
bcf/
bim4hvac/
pdf_regulations/

plugins/
loader.py

vector/
embeddings.py
index_manager.py

utils/
config.py
logging.py

---

# Complete System Overview

\`\`\`mermaid
flowchart TB

User[User]

Query[Natural Language Query]

SemanticEngine[Semantic Engine]

ReferenceKnowledge[Reference Knowledge]

UseCaseSelection[Use Case Selection]

Instantiation[Use Case Instantiation]

Plugins[Plugin Modules]

KnowledgeGraph[(Knowledge Graph)]

Validation[Validation]

IDSExport[IDS Export]

BCF[BCF Issues]

User --> Query
Query --> SemanticEngine
SemanticEngine --> ReferenceKnowledge
ReferenceKnowledge --> UseCaseSelection
UseCaseSelection --> Instantiation
Instantiation --> Plugins
Plugins --> KnowledgeGraph
KnowledgeGraph --> Validation
Validation --> IDSExport
Validation --> BCF
\`\`\`

---

# Design Principles

- reference knowledge instead of manual modelling
- semantic discovery of BIM use cases
- modular plugin architecture
- graph-based BIM knowledge representation
- integration of BIM standards and ontologies

---

# Final Goal

Graphmaster aims to become a **Semantic BIM Knowledge Platform** capable of connecting

- BIM standards
- semantic web technologies
- classification systems
- project requirements
- regulatory frameworks
- digital twins

within a unified semantic knowledge graph.
