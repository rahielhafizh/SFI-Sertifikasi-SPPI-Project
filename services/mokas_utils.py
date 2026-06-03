from datetime import datetime, timedelta
from typing import List, Tuple
from services.sppi_utils import parse_date


def filter_mokas_birthdays(
    columns: List[str], rows: List[Tuple], mode: str
) -> List[Tuple]:
    if not isinstance(columns, list) or not isinstance(rows, list):
        return []

    today = datetime.now()
    today_date = today.date()
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

    valid_rows_with_delta = []

    for row in rows:
        dealer_id = row[dealer_id_idx]
        raw_date = row[birth_date_idx]
        nama_pemilik = row[owner_name_idx]

        if not raw_date or not nama_pemilik or not str(nama_pemilik).strip():
            continue

        birth_date = parse_date(raw_date)

        if birth_date is None:
            continue

        if mode == "MONTHLY":
            if dealer_id in seen_ids:
                continue
            if birth_date.month == today.month:
                seen_ids.add(dealer_id)
                filtered_data.append(row)

        elif mode == "WEEKLY":
            if dealer_id in seen_ids:
                continue
            try:
                this_year_bday = datetime(today.year, birth_date.month, birth_date.day)
            except (ValueError, TypeError):
                this_year_bday = datetime(today.year, 3, 1)

            if start_date <= this_year_bday <= end_date:
                seen_ids.add(dealer_id)
                filtered_data.append(row)

        elif mode == "DAILY":
            try:
                bday_target = datetime(
                    today.year, birth_date.month, birth_date.day
                ).date()
            except (ValueError, TypeError):
                bday_target = datetime(today.year, 3, 1).date()

            if bday_target < today_date:
                try:
                    bday_target = datetime(
                        today.year + 1, birth_date.month, birth_date.day
                    ).date()
                except (ValueError, TypeError):
                    bday_target = datetime(today.year + 1, 3, 1).date()

            days_until = (bday_target - today_date).days
            valid_rows_with_delta.append((row, dealer_id, days_until))

    if mode == "DAILY":
        future_deltas = [d for _, _, d in valid_rows_with_delta if d > 0]
        min_future_delta = min(future_deltas) if future_deltas else None

        for row, dealer_id, days_until in valid_rows_with_delta:
            if dealer_id in seen_ids:
                continue

            if days_until == 0 or (
                min_future_delta is not None and days_until == min_future_delta
            ):
                seen_ids.add(dealer_id)
                filtered_data.append(row)

    return filtered_data


def sort_by_birth_date(columns: List[str], rows: List[Tuple]) -> List[Tuple]:
    if not isinstance(columns, list) or not isinstance(rows, list):
        return []

    birth_date_idx = (
        columns.index("TANGGAL_LAHIR") if "TANGGAL_LAHIR" in columns else -1
    )

    def get_sort_key(r):
        if birth_date_idx == -1:
            return 99
        bdate = parse_date(r[birth_date_idx])
        return bdate.day if bdate is not None else 99

    return sorted(rows, key=get_sort_key)
