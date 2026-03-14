from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends
from common.deps import get_conn

router = APIRouter()

@router.get("/health")
async def health(conn = Depends(get_conn)):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    return {"db_alive": cur.fetchone()[0] == 1}


@router.post("/upload")
async def upload_ontology(file: UploadFile = File(...)):
    if not file.filename.endswith(".ttl"):
        raise HTTPException(status_code=400, detail="Nur .ttl-Dateien erlaubt")
    return JSONResponse({
        "message": "Ontology uploaded (dummy)",
        "filename": file.filename
    })

@router.get("/{ontology_id}/metadata")
async def get_metadata(ontology_id: str):
    return {
        "ontology_id": ontology_id,
        "metadata": {
            "size_bytes": 0,
            "preview": ""
        }
    }

@router.get("/{ontology_id}/tokens")
async def extract_tokens(ontology_id: str):
    return {
        "ontology_id": ontology_id,
        "tokens": []
    }
