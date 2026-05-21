import pyodbc
from typing import Optional
from services.config import logger

def get_database_connection() -> Optional[pyodbc.Connection]:
    connection_string = (
        "DRIVER={SQL Server};"
        "SERVER=172.16.0.239;"
        "DATABASE=SFI_DWH;"
        "UID=usersfi;"
        "PWD=sfi.100;"
    )
    try:
        conn = pyodbc.connect(connection_string, timeout=5)
        logger.info("[SYSTEM] DATABASE CONNECTION SUCCESS")
        return conn
    except pyodbc.Error as e:
        logger.error(f"[ERROR] DATABASE CONNECTION FAILED : {e}")
        return None