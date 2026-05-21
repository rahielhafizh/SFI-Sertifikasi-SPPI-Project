from datetime import datetime, timedelta
from typing import List, Tuple
from services.config import logger
from services.certification_utils import parse_date


def filter_mokas_birthdays(
    columns: List[str], rows: List[Tuple], mode: str
) -> List[Tuple]:
    today = datetime.now()
    column_indices = {col: idx for idx, col in enumerate(columns)}
    filtered_data = []
    seen_ids = set()

    if mode == "WEEKLY":
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        start_date = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = end_of_week.replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

    for row in rows:
        dealer_id = row[column_indices.get("DEALER_MOKAS_ID")]

        if dealer_id in seen_ids:
            continue

        birth_date_val = row[column_indices.get("TANGGAL_LAHIR")]
        birth_date = parse_date(birth_date_val)
        nama_pemilik = row[column_indices.get("NAMA_PEMILIK")]

        if not birth_date or not nama_pemilik or not str(nama_pemilik).strip():
            continue

        seen_ids.add(dealer_id)

        if mode == "MONTHLY":
            if birth_date.month == today.month:
                filtered_data.append(row)

        elif mode == "WEEKLY":
            try:
                this_year_bday = datetime(today.year, birth_date.month, birth_date.day)
            except ValueError:
                this_year_bday = datetime(today.year, 3, 1)

            if start_date <= this_year_bday <= end_date:
                filtered_data.append(row)

    return filtered_data


def sort_by_birth_date(columns: List[str], rows: List[Tuple]) -> List[Tuple]:
    column_indices = {col: idx for idx, col in enumerate(columns)}
    return sorted(
        rows,
        key=lambda r: (
            parse_date(r[column_indices["TANGGAL_LAHIR"]]).day
            if parse_date(r[column_indices["TANGGAL_LAHIR"]])
            else 99
        ),
    )
