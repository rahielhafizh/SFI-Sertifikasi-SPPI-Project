from typing import List, Tuple

from services.sppi_utils import format_name_title_case, format_date_indonesian


def _build_mokas_header() -> List[str]:
    return [
        "Yth. Bapak Chief Operating Officer,",
        "",
    ]


def _build_mokas_footer() -> List[str]:
    return [
        "Mohon agar data tersebut dapat ditinjau kembali guna koordinasi pemberian apresiasi kepada pihak terkait.",
        "",
        "Atas perhatian dan kerja samanya, kami ucapkan terima kasih.",
        "",
        "Hormat kami,",
        "Collection HO \u2013 PT Suzuki Finance Indonesia",
    ]


def _build_pic_lines(rows: List[Tuple], columns: List[str]) -> List[str]:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    lines = []

    for pic in rows:
        nama = format_name_title_case(pic[col_idx["NAMA_PEMILIK"]])
        dealer = format_name_title_case(pic[col_idx["NAMA_DEALER"]])
        kota_raw = (
            pic[col_idx["KOTA"]]
            if "KOTA" in col_idx and pic[col_idx["KOTA"]]
            else pic[col_idx["CABANG"]]
        )
        lokasi = format_name_title_case(kota_raw)
        tgl_lahir = format_date_indonesian(pic[col_idx["TANGGAL_LAHIR"]])
        no_hp = pic[col_idx["NO_HP"]] or "-"

        lines.append(f"Nama Pemilik : {nama} (Dealer {dealer} - Kota {lokasi})")
        lines.append(f"Tanggal Lahir : {tgl_lahir} | No. HP : {no_hp}")
        lines.append("")

    return lines


def format_mokas_daily_email_body(
    rows: List[Tuple],
    columns: List[str],
    check_today_birthdays: bool,
    today_date_str: str,
) -> str:
    lines = _build_mokas_header()

    if check_today_birthdays:
        lines.extend(
            [
                f"Berikut kami lampirkan daftar pemilik Dealer Mobil Bekas yang berulang tahun pada hari ini ({today_date_str}) dan tanggal terdekat selanjutnya.",
                "",
                "Terlampir rincian data mitra terkait adalah sebagai berikut:",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "Berikut kami lampirkan daftar pemilik Dealer Mobil Bekas yang berulang tahun.",
                "",
                f"Adapun untuk hari ini ({today_date_str}), tidak terdapat mitra dealer yang berulang tahun, "
                "dan mitra dealer yang berulang tahun pada tanggal terdekat adalah sebagai berikut :",
                "",
            ]
        )

    lines.extend(_build_pic_lines(rows, columns))
    lines.extend(_build_mokas_footer())
    return "\n".join(lines)


def format_mokas_weekly_email_body(
    period_value: str,
    rows: List[Tuple],
    columns: List[str],
) -> str:
    lines = _build_mokas_header()
    lines.extend(
        [
            f"Berikut terlampir daftar pemilik Dealer Mobil Bekas yang berulang tahun pada minggu ini ({period_value}).",
            "",
            "Adapun rincian data mitra terkait adalah sebagai berikut:",
            "",
        ]
    )
    lines.extend(_build_pic_lines(rows, columns))
    lines.extend(_build_mokas_footer())
    return "\n".join(lines)


def format_mokas_monthly_email_body(
    period_value: str,
    rows: List[Tuple],
    columns: List[str],
) -> str:
    lines = _build_mokas_header()
    lines.extend(
        [
            f"Berikut terlampir daftar pemilik Dealer Mobil Bekas yang berulang tahun pada bulan ini ({period_value}).",
            "",
            "Adapun rincian data mitra terkait adalah sebagai berikut:",
            "",
        ]
    )
    lines.extend(_build_pic_lines(rows, columns))
    lines.extend(_build_mokas_footer())
    return "\n".join(lines)
