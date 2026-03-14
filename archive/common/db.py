import os
import oracledb

# Lade die Zugangsdaten aus der Umgebung
USER   = os.getenv("ORACLE_USER")
PWD    = os.getenv("ORACLE_PASSWORD")
HOST   = os.getenv("ORACLE_HOST")
PORT   = os.getenv("ORACLE_PORT")
SERVICE= os.getenv("ORACLE_SERVICE")

def get_db_connection():
    """
    Gibt eine mandantenfähige Verbindung zur Oracle-DB zurück.
        
    return oracledb.connect(
        user=USER,
        password=PWD,
        host=HOST,
        port=int(PORT),
        service_name=SERVICE
    )
