from typing import List, Tuple
from services.sppi_utils import format_name_title_case, format_date_indonesian


def set_mokas_header() -> List[str]:
    return [
        "Yth. Bapak Chief Operating Officer,",
        "",
    ]


def set_mokas_footer() -> List[str]:
    return [
        "Diharapkan agar data tersebut dapat ditinjau kembali guna koordinasi pemberian apresiasi kepada pihak terkait.",
        "",
        "Atas perhatian dan kerja samanya, kami ucapkan terima kasih.",
        "",
        "Hormat kami,",
        "Sales & Marketing \u2013 PT Suzuki Finance Indonesia",
    ]


def get_birthdays_list(rows: List[Tuple], columns: List[str]) -> List[str]:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    lines = []

    for pic in rows:
        nama = format_name_title_case(pic[col_idx["NAMA_MITRA"]])
        dealer = format_name_title_case(pic[col_idx["NAMA_DEALER"]])
        cabang = format_name_title_case(pic[col_idx["MAPPING_CABANG"]])
        tgl_lahir = format_date_indonesian(pic[col_idx["TANGGAL_LAHIR"]])
        no_hp = pic[col_idx["NO_MITRA"]] or "-"

        lines.append(f"Nama : {nama} (Dealer {dealer} - Cabang {cabang})")
        lines.append(f"Tanggal Lahir : {tgl_lahir} | No. HP : {no_hp}")
        lines.append("")

    return lines


def format_mokas_whatsapp_body(
    recipient_name: str,
    recipient_role: str,
    rows: List[Tuple],
    columns: List[str],
    check_today_birthdays: bool,
    today_date_str: str,
) -> str:
    lines = [f"Reminder untuk Bapak {recipient_name} selaku {recipient_role}.", ""]

    if check_today_birthdays:
        lines.extend(
            [
                f"Dengan ini kami informasikan daftar pemilik Dealer Mobil Bekas yang berulang tahun pada hari ini ({today_date_str}) :",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Dengan ini kami informasikan daftar pemilik Dealer Mobil Bekas yang berulang tahun.",
                "",
                f"Adapun untuk hari ini ({today_date_str}), tidak terdapat mitra dealer yang berulang tahun, "
                "dan mitra dealer yang berulang tahun pada tanggal terdekat adalah sebagai berikut :",
                "",
            ]
        )

    lines.extend(get_birthdays_list(rows, columns))
    lines.extend(set_mokas_footer())
    return "\n".join(lines)


def format_mokas_daily_email_body(
    rows: List[Tuple],
    columns: List[str],
    check_today_birthdays: bool,
    today_date_str: str,
) -> str:
    lines = set_mokas_header()

    if check_today_birthdays:
        lines.extend(
            [
                f"Dengan ini kami informasikan daftar pemilik Dealer Mobil Bekas yang berulang tahun pada hari ini ({today_date_str}) :",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Dengan ini kami informasikan daftar pemilik Dealer Mobil Bekas yang berulang tahun.",
                "",
                f"Adapun untuk hari ini ({today_date_str}), tidak terdapat mitra dealer yang berulang tahun, "
                "dan mitra dealer yang berulang tahun pada tanggal terdekat adalah sebagai berikut :",
                "",
            ]
        )

    lines.extend(get_birthdays_list(rows, columns))
    lines.extend(set_mokas_footer())
    return "\n".join(lines)


def format_mokas_weekly_email_body(
    period_value: str,
    rows: List[Tuple],
    columns: List[str],
) -> str:
    lines = set_mokas_header()
    lines.extend(
        [
            f"Dengan ini kami informasikan list pemilik Dealer Mobil Bekas yang berulang tahun pada minggu ini ({period_value}).",
            "",
            "Adapun rincian data mitra terkait adalah sebagai berikut:",
            "",
        ]
    )
    lines.extend(get_birthdays_list(rows, columns))
    lines.extend(set_mokas_footer())
    return "\n".join(lines)


def format_mokas_monthly_email_body(
    period_value: str,
    rows: List[Tuple],
    columns: List[str],
) -> str:
    lines = set_mokas_header()
    lines.extend(
        [
            f"Dengan ini kami informasikan daftar pemilik Dealer Mobil Bekas yang berulang tahun pada bulan ini ({period_value}).",
            "",
            "Adapun rincian data mitra terkait adalah sebagai berikut:",
            "",
        ]
    )
    lines.extend(get_birthdays_list(rows, columns))
    lines.extend(set_mokas_footer())
    return "\n".join(lines)
