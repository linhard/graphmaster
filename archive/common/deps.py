from fastapi import Depends
from common.db import get_db_connection

def get_conn():
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()
