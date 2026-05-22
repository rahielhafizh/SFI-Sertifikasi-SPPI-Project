import pyodbc
from typing import List, Tuple, Optional
from services.config import logger


def fetch_dealer_mokas_data(
    conn: pyodbc.Connection,
) -> Tuple[Optional[List[str]], Optional[List[Tuple]]]:
    cursor = None
    try:
        cursor = conn.cursor()
        # Query disesuaikan dengan struktur dan nama field tabel DEALER_MOKAS terbaru
        query = """
            SELECT 
                DEALER_MOKAS_ID, AREA, CABANG, NAMA_DEALER, 
                NAMA_MITRA, NO_MITRA, KOTA, TANGGAL_LAHIR, ALAMAT,
                MAPPING_AREA, MAPPING_CABANG, NAMA_BM, NO_BM, NAMA_AM, NO_AM
            FROM [SFI_DWH].[dbo].[DEALER_MOKAS]
            WHERE TANGGAL_LAHIR IS NOT NULL AND NAMA_MITRA IS NOT NULL
        """
        cursor.execute(query)

        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()

        logger.info(f"[DATABASE] FETCHED {len(rows)} ROWS FROM DEALER_MOKAS")
        return columns, rows
    except pyodbc.Error as e:
        logger.error(f"[ERROR] QUERY FAILED (DEALER MOKAS) : {e}")
        return None, None
