from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, Depends
from common.deps import get_conn

router = APIRouter()

class VectorizeRequest(BaseModel):
    tokens: List[str]
    llm: str

@router.post("/vectorize")
async def vectorize_tokens(req: VectorizeRequest):
    return {
        "tokens": req.tokens,
        "llm": req.llm,
        "vectors": []
    }

@router.get("/health")
async def health(conn = Depends(get_conn)):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    return {"db_alive": cur.fetchone()[0] == 1}

