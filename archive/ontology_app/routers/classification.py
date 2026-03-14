from fastapi import APIRouter, Depends, HTTPException
from common.deps import get_conn
from typing import List
from pydantic import BaseModel
from fastapi import APIRouter, Depends
from common.deps import get_conn

router = APIRouter(tags=["classification"])

class Classification(BaseModel):
    id: int
    name: str

@router.get("/", response_model=List[Classification])
async def list_classifications(conn=Depends(get_conn)):
    """
    Gibt alle verfügbaren Classification-Einträge zurück.
    """
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM classifications")
    rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail="Keine Classifications gefunden")
    return [Classification(id=r[0], name=r[1]) for r in rows]
    
    
    
    @router.get("/health")
async def health(conn = Depends(get_conn)):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    return {"db_alive": cur.fetchone()[0] == 1}
