from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any, Tuple
from collections import defaultdict
from services.config import (
    logger,
    get_certification_filter_config,
    set_certification_filter_preset,
    get_month_id,
)


def parse_date(date_value: Any) -> Optional[datetime]:
    if not date_value:
        return None
    if isinstance(date_value, datetime):
        return date_value
    if isinstance(date_value, date):
        return datetime(date_value.year, date_value.month, date_value.day)
    if isinstance(date_value, str):
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
            try:
                return datetime.strptime(date_value.split(" ")[0], fmt)
            except ValueError:
                continue
    return None


def format_date_indonesian(date_value: Any) -> str:
    parsed_date = parse_date(date_value)
    if not parsed_date:
        return str(date_value) if date_value else ""

    month_indonesian = get_month_id(parsed_date.strftime("%B"), case="as-is")
    return f"{parsed_date.day} {month_indonesian} {parsed_date.year}"


def format_name_title_case(name: Optional[str]) -> str:
    if not name or not isinstance(name, str):
        return name or ""

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
    filter_mode = filter_config.get("MODE", "NEXT_MONTH")

    for row in rows:
        expired_date = parse_date(row[column_indices.get(date_column, -1)])
        if not expired_date:
            continue

        if filter_mode == "NEXT_MONTH":
            next_month = (today.month % 12) + 1
            next_year = today.year + (1 if today.month == 12 else 0)
            if expired_date.month == next_month and expired_date.year == next_year:
                filtered_data.append(row)

        elif filter_mode == "NEXT_N_MONTHS":
            months_ahead = filter_config.get("MONTHS_AHEAD", 2)
            for i in range(1, months_ahead + 1):
                calc_month = ((today.month + i - 1) % 12) + 1
                calc_year = today.year + ((today.month + i - 1) // 12)
                if expired_date.month == calc_month and expired_date.year == calc_year:
                    filtered_data.append(row)
                    break

    if filter_mode not in ["NEXT_MONTH", "NEXT_N_MONTHS"]:
        set_certification_filter_preset("NEXT_MONTH")
        return filter_expiring_certifications(columns, rows, date_column)

    return filtered_data


def group_by_branch(
    columns: List[str], filtered_rows: List[Tuple], branch_column: str = "BRANCH_NAME"
) -> Dict[str, List[Tuple]]:
    branch_idx = columns.index(branch_column) if branch_column in columns else -1
    branch_groups = defaultdict(list)

    if branch_idx == -1:
        return branch_groups

    for row in filtered_rows:
        branch_name = row[branch_idx]
        if branch_name:
            branch_groups[branch_name].append(row)

    return branch_groups


def build_email_header(branch_name: str, branch_manager: str) -> List[str]:
    return [
        f"Dear Bapak {format_name_title_case(branch_manager)},",
        "",
        f"Dengan ini kami sampaikan pemberitahuan terkait Tim Collection cabang {format_name_title_case(branch_name)}.",
        "Berdasarkan data, terdapat PIC dengan masa berlaku Sertifikasi SPPI yang akan segera berakhir, dengan rincian sebagai berikut",
        "",
    ]


def build_email_footer() -> List[str]:
    return [
        "Sehubungan dengan hal tersebut, mohon agar dapat berkoordinasi dengan Divisi HR untuk penjadwalan Ujian Sertifikasi Penagihan. Jangan sampai terdapat petugas lapangan yang melakukan penagihan tanpa memiliki sertifikasi yang masih aktif atau dalam kondisi kedaluwarsa (expired).",
        "",
        "Atas perhatian dan kerja samanya, kami ucapkan terima kasih.",
        "",
        "",
        "Hormat kami,",
        "Asset Management Division.",
        "Collection HO - PT Suzuki Finance Indonesia.",
    ]


def format_pic_line(pic_name: str, pic_role: str, expired_date: Any) -> str:
    return f"👮 {format_name_title_case(pic_name)}  💼 {pic_role}\n📅 Masa Berlaku SPPI : {format_date_indonesian(expired_date)}\n"


def get_email_subject(branch_name: str) -> str:
    return f"Pemberitahuan Masa Berlaku Sertifikasi SPPI Tim Collection ({format_name_title_case(branch_name)})"


def extract_branch_manager_info(
    pic_list: List[Tuple],
    column_indices: Dict[str, int],
    manager_column: str = "BRANCH_MANAGER",
    email_column: str = "BM_MAIL",
) -> Tuple[Optional[str], Optional[str]]:
    if not pic_list:
        return None, None
    return (
        pic_list[0][column_indices.get(manager_column, -1)],
        pic_list[0][column_indices.get(email_column, -1)],
    )
