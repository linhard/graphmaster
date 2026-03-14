from fastapi import FastAPI
from ontology_app.routers import ontology
from ontology_app.routers import classification

app = FastAPI(title="Ontology Service")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

app.include_router(
    ontology.router,
    prefix="/ontologies",
    tags=["ontologies"]
)

app.include_router(classification.router, prefix="/classifications")
