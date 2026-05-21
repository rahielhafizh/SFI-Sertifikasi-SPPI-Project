import pyodbc
from typing import List, Tuple, Optional
from services.config import logger


def fetch_dealer_mokas_data(
    conn: pyodbc.Connection,
) -> Tuple[Optional[List[str]], Optional[List[Tuple]]]:
    try:
        cursor = conn.cursor()
        query = """
            SELECT 
                DEALER_MOKAS_ID, AREA, CABANG, NAMA_DEALER, 
                NAMA_PEMILIK, NO_HP, KOTA, TANGGAL_LAHIR, ALAMAT 
            FROM [SFI_DWH].[dbo].[DEALER_MOKAS]
            WHERE TANGGAL_LAHIR IS NOT NULL AND NAMA_PEMILIK IS NOT NULL
        """
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        cursor.close()
        logger.info(f"[DATABASE] FETCHED {len(rows)} ROWS FROM DEALER_MOKAS")
        return columns, rows
    except pyodbc.Error as e:
        logger.error(f"[ERROR] QUERY FAILED (DEALER MOKAS) : {e}")
        return None, None
