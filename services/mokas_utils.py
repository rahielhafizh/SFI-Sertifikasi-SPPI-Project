from datetime import datetime, timedelta
from typing import List, Tuple
from services.certification_utils import parse_date


def filter_mokas_birthdays(
    columns: List[str], rows: List[Tuple], mode: str
) -> List[Tuple]:
    today = datetime.now()
    column_indices = {col: idx for idx, col in enumerate(columns)}

    dealer_id_idx = column_indices.get("DEALER_MOKAS_ID", -1)
    birth_date_idx = column_indices.get("TANGGAL_LAHIR", -1)
    owner_name_idx = column_indices.get("NAMA_PEMILIK", -1)

    filtered_data = []
    seen_ids = set()

    if mode == "WEEKLY":
        start_date = (today - timedelta(days=today.weekday())).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        end_date = (start_date + timedelta(days=6)).replace(
            hour=23, minute=59, second=59, microsecond=999999
        )

    for row in rows:
        dealer_id = row[dealer_id_idx]
        if dealer_id in seen_ids:
            continue

        birth_date = parse_date(row[birth_date_idx])
        nama_pemilik = row[owner_name_idx]

        if not birth_date or not nama_pemilik or not str(nama_pemilik).strip():
            continue

        if mode == "MONTHLY":
            if birth_date.month == today.month:
                seen_ids.add(dealer_id)
                filtered_data.append(row)

        elif mode == "WEEKLY":
            # Handle leap year birthday safely
            try:
                this_year_bday = datetime(today.year, birth_date.month, birth_date.day)
            except ValueError:
                this_year_bday = datetime(today.year, 3, 1)

            if start_date <= this_year_bday <= end_date:
                seen_ids.add(dealer_id)
                filtered_data.append(row)

    return filtered_data


def sort_by_birth_date(columns: List[str], rows: List[Tuple]) -> List[Tuple]:
    birth_date_idx = (
        columns.index("TANGGAL_LAHIR") if "TANGGAL_LAHIR" in columns else -1
    )
    return sorted(
        rows,
        key=lambda r: (
            parse_date(r[birth_date_idx]).day
            if birth_date_idx != -1 and parse_date(r[birth_date_idx])
            else 99
        ),
    )
