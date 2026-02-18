from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from collections import defaultdict
from services.config import (
    logger,
    get_certification_filter_config,
    set_certification_filter_preset,
    get_month_id,
    get_branch_order,
)


def parse_date(date_value: Any) -> Optional[datetime]:
    if date_value is None:
        return None

    if isinstance(date_value, datetime):
        return date_value

    if isinstance(date_value, str):
        formats = ["%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"]
        for fmt in formats:
            try:
                return datetime.strptime(date_value, fmt)
            except ValueError:
                continue

    return None


def format_date_indonesian(date_value: Any) -> str:
    parsed_date = parse_date(date_value)

    if parsed_date is None:
        return str(date_value) if date_value else ""

    day = parsed_date.day
    month_english = parsed_date.strftime("%B")
    year = parsed_date.year
    month_indonesian = get_month_id(month_english, case="as-is")

    return f"{day} {month_indonesian} {year}"


def format_name_title_case(name: Optional[str]) -> str:
    if not name or not isinstance(name, str):
        return name

    special_cases = {
        "Pt": "PT",
        "Cv": "CV",
        "Ud": "UD",
        "Ii": "II",
        "Iii": "III",
        "Iv": "IV",
        "Vi": "VI",
        "Vii": "VII",
        "Viii": "VIII",
        "Ix": "IX",
        "Xi": "XI",
        "Xii": "XII",
    }

    formatted = name.title()

    for incorrect, correct in special_cases.items():
        formatted = formatted.replace(incorrect, correct)

    return formatted


def filter_expiring_certifications(
    columns: List[str], rows: List[Tuple], date_column: str = "EXPIRED_DATE"
) -> List[Tuple]:
    today = datetime.now()
    column_indices = {col: idx for idx, col in enumerate(columns)}
    filtered_data = []

    filter_config = get_certification_filter_config()
    filter_mode = filter_config["MODE"]

    if filter_mode == "NEXT_MONTH":
        current_month = today.month
        current_year = today.year

        if current_month == 12:
            next_month = 1
            next_year = current_year + 1
        else:
            next_month = current_month + 1
            next_year = current_year

        for row in rows:
            expired_date_value = row[column_indices[date_column]]
            expired_date = parse_date(expired_date_value)

            if (
                expired_date
                and expired_date.month == next_month
                and expired_date.year == next_year
            ):
                filtered_data.append(row)

    elif filter_mode == "NEXT_N_MONTHS":
        months_ahead = filter_config.get("MONTHS_AHEAD", 2)

        target_months = []
        for i in range(1, months_ahead + 1):
            calc_month = today.month + i
            calc_year = today.year

            while calc_month > 12:
                calc_month -= 12
                calc_year += 1

            target_months.append((calc_month, calc_year))

        for row in rows:
            expired_date_value = row[column_indices[date_column]]
            expired_date = parse_date(expired_date_value)

            if expired_date:
                for month, year in target_months:
                    if expired_date.month == month and expired_date.year == year:
                        filtered_data.append(row)
                        break

    elif filter_mode == "DAYS_RANGE":
        days_ahead = filter_config.get("DAYS_AHEAD", 60)
        end_date = today + timedelta(days=days_ahead)

        for row in rows:
            expired_date_value = row[column_indices[date_column]]
            expired_date = parse_date(expired_date_value)

            if expired_date and today <= expired_date <= end_date:
                filtered_data.append(row)

    elif filter_mode == "SPECIFIC_DATE_RANGE":
        start_date = filter_config.get("START_DATE")
        end_date = filter_config.get("END_DATE")

        if start_date:
            start_date = parse_date(start_date)
        else:
            start_date = today

        if end_date:
            end_date = parse_date(end_date)
        else:
            end_date = today + timedelta(days=30)

        for row in rows:
            expired_date_value = row[column_indices[date_column]]
            expired_date = parse_date(expired_date_value)

            if expired_date and start_date <= expired_date <= end_date:
                filtered_data.append(row)

    else:
        logger.warning(
            f"[WARNING] UNKNOWN FILTER MODE : {filter_mode}, DEFAULTING TO NEXT_MONTH"
        )
        set_certification_filter_preset("NEXT_MONTH")
        return filter_expiring_certifications(columns, rows, date_column)

    return filtered_data


def group_by_branch(
    columns: List[str], filtered_rows: List[Tuple], branch_column: str = "BRANCH_NAME"
) -> Dict[str, List[Tuple]]:
    column_indices = {col: idx for idx, col in enumerate(columns)}
    branch_groups = defaultdict(list)

    for row in filtered_rows:
        branch_name = row[column_indices[branch_column]]
        if branch_name:
            branch_groups[branch_name].append(row)

    return branch_groups


def build_email_header(branch_name: str, branch_manager: str) -> List[str]:
    branch_name_formatted = format_name_title_case(branch_name)
    branch_manager_formatted = format_name_title_case(branch_manager)

    return [
        f"Dear Bapak {branch_manager_formatted},",
        "",
        f"Dengan ini kami sampaikan pemberitahuan terkait Tim Collection cabang {branch_name_formatted}.",
        "Berdasarkan data, terdapat PIC dengan masa berlaku Sertifikasi SPPI yang akan segera berakhir, dengan rincian sebagai berikut",
        "",
    ]


def build_email_footer() -> List[str]:
    return [
        "",
        "Sehubungan dengan hal tersebut, mohon agar dapat berkoordinasi dengan Divisi HR untuk penjadwalan Ujian Sertifikasi Penagihan.",
        "Jangan sampai terdapat petugas lapangan yang melakukan penagihan tanpa memiliki sertifikasi yang masih aktif atau dalam kondisi kedaluwarsa (expired).",
        "",
        "Atas perhatian dan kerja samanya, kami ucapkan terima kasih.",
        "",
        "",
        "Hormat kami,",
        "Asset Management Division.",
        "Collection HO – PT Suzuki Finance Indonesia.",
    ]


def format_pic_line(pic_name: str, pic_role: str, expired_date: Any) -> str:

    pic_name_formatted = format_name_title_case(pic_name)
    expired_date_str = format_date_indonesian(expired_date)

    return f"👨🏼 {pic_name_formatted} 🔰 {pic_role}\t\t📅  Masa Berlaku SPPI : {expired_date_str}"


def get_email_subject(branch_name: str) -> str:
    branch_name_formatted = format_name_title_case(branch_name)
    return f"Pemberitahuan Masa Berlaku Sertifikasi SPPI Tim Collection ({branch_name_formatted})"


def extract_branch_manager_info(
    pic_list: List[Tuple],
    column_indices: Dict[str, int],
    manager_column: str = "BRANCH_MANAGER",
    email_column: str = "BM_MAIL",
) -> Tuple[Optional[str], Optional[str]]:
    if not pic_list:
        return None, None

    branch_manager = pic_list[0][column_indices[manager_column]]
    bm_mail = pic_list[0][column_indices[email_column]]

    return branch_manager, bm_mail
