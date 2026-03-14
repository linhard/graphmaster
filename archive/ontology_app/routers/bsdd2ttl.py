from fastapi import APIRouter, Depends, HTTPException
from common.deps import get_conn
import httpx
from bsdd2json import convert_ttl_to_json  # falls du JSON statt TTL willst
from fastapi import APIRouter, Depends
from common.deps import get_conn

router = APIRouter(tags=["bsdd2ttl"])

@router.post("/batch")
async def batch_bsdd2ttl(conn=Depends(get_conn)):
    # 1) Hole alle Classifications
    async with httpx.AsyncClient(base_url="http://localhost:8000") as client:
        resp = await client.get("/classifications")
    if resp.status_code != 200:
        raise HTTPException(502, "Classification-Service nicht erreichbar")
    classifications = resp.json()  # Liste von {id,name}

    cur = conn.cursor()
    inserted = []
    for c in classifications:
        # 2) TTL von deinem BS-DD-Service abrufen (hier hypothetisch)
        bsdd_resp = await client.get(f"/bsdd/{c['name']}/ttl")
        if bsdd_resp.status_code != 200:
            continue  # überspringen oder Fehler sammeln
        ttl = bsdd_resp.text

        # 3) In Ontologies einfügen
        cur.execute(
            """
            INSERT INTO ontologies (name, file_clob)
            VALUES (:name, :clob)
            """,
            {"name": c["name"], "clob": ttl}
        )
        inserted.append(c["name"])
    conn.commit()
    return {"processed": inserted}

@router.get("/health")
async def health(conn = Depends(get_conn)):
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM DUAL")
    return {"db_alive": cur.fetchone()[0] == 1}