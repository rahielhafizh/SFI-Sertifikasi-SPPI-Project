import pyodbc
from typing import List, Tuple, Optional
from services.config import logger

def fetch_table_data(
    conn: pyodbc.Connection, table_name: str
) -> Tuple[Optional[List[str]], Optional[List[Tuple]]]:
    try:
        cursor = conn.cursor()
        query = f"SELECT * FROM [SFI_DWH].[dbo].[{table_name}]"
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        
        logger.info(f"[DATABASE] FETCHED {len(rows)} ROWS FROM {table_name}")
        return columns, rows
    except pyodbc.Error as e:
        logger.error(f"[ERROR] QUERY FAILED FOR TABLE '{table_name}' : {e}")
        return None, None

def fetch_certification_data_internal(conn: pyodbc.Connection):
    return fetch_table_data(conn, "Dashboard_Certification_Internal")

def fetch_certification_data_external(conn: pyodbc.Connection):
    return fetch_table_data(conn, "Dashboard_Certification_Eksternal")

def fetch_dealer_mokas_data(conn: pyodbc.Connection, period: str):
    table_name = "Dashboard_Dealer_Mokas_Monthly" if period.upper() == "MONTHLY" else "Dashboard_Dealer_Mokas_Weekly"
    return fetch_table_data(conn, table_name)