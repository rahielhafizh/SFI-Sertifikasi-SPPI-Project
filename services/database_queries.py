import pyodbc
from typing import List, Tuple, Optional
from services.config import logger


def fetch_certification_data_internal(
    conn: pyodbc.Connection,
) -> Tuple[Optional[List[str]], Optional[List[Tuple]]]:
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM [SFI_DWH].[dbo].[Dashboard_Certification_Date]"
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        logger.info(
            f"[DATABASE] FETCHED {len(rows)} ROWS FROM Dashboard_Certification_Date"
        )
        return columns, rows
    except pyodbc.Error as e:
        logger.error(f"[ERROR] QUERY FAILED (INTERNAL) : {e}")
        return None, None


def fetch_certification_data_external(
    conn: pyodbc.Connection,
) -> Tuple[Optional[List[str]], Optional[List[Tuple]]]:
    try:
        cursor = conn.cursor()
        query = "SELECT * FROM [SFI_DWH].[dbo].[Dashboard_Certification_Eksternal]"
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        logger.info(
            f"[DATABASE] FETCHED {len(rows)} ROWS FROM Dashboard_Certification_Eksternal"
        )
        return columns, rows
    except pyodbc.Error as e:
        logger.error(f"[ERROR] QUERY FAILED (EXTERNAL) : {e}")
        return None, None
