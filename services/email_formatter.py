from typing import List, Tuple
from services.certification_utils import (
    build_email_header,
    build_email_footer,
    format_pic_line,
    format_name_title_case,
    format_date_indonesian,
)


def format_internal_email_body(
    branch_name: str, branch_manager: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    email_lines = build_email_header(branch_name, branch_manager)
    email_lines.append("Daftar PIC Internal :")

    for pic in pic_list:
        email_lines.append(
            format_pic_line(
                pic[col_idx["PIC_NAME"]],
                pic[col_idx["JOB_TITLE_CODE"]],
                pic[col_idx["EXPIRED_DATE"]],
            )
        )

    email_lines.extend(build_email_footer())
    return "\n".join(email_lines)


def format_external_email_body(
    branch_name: str, branch_manager: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    email_lines = build_email_header(branch_name, branch_manager)
    email_lines.append("Daftar PIC Eksternal :")

    for pic in pic_list:
        email_lines.append(
            format_pic_line(
                pic[col_idx["PIC_NAME"]],
                pic[col_idx["PIC_ROLE"]],
                pic[col_idx["EXPIRED_DATE"]],
            )
        )

    email_lines.extend(build_email_footer())
    return "\n".join(email_lines)


def format_combined_email_body(
    branch_name: str,
    branch_manager: str,
    internal_pic_list: List[Tuple],
    external_pic_list: List[Tuple],
    columns_internal: List[str],
    columns_external: List[str],
) -> str:
    email_lines = build_email_header(branch_name, branch_manager)

    if internal_pic_list:
        email_lines.append("PIC Internal :")
        col_idx_int = {col: idx for idx, col in enumerate(columns_internal)}
        for pic in internal_pic_list:
            email_lines.append(
                format_pic_line(
                    pic[col_idx_int["PIC_NAME"]],
                    pic[col_idx_int["JOB_TITLE_CODE"]],
                    pic[col_idx_int["EXPIRED_DATE"]],
                )
            )

    if external_pic_list:
        if internal_pic_list:
            email_lines.append("")
        email_lines.append("PIC Eksternal :")
        col_idx_ext = {col: idx for idx, col in enumerate(columns_external)}
        for pic in external_pic_list:
            email_lines.append(
                format_pic_line(
                    pic[col_idx_ext["PIC_NAME"]],
                    pic[col_idx_ext["PIC_ROLE"]],
                    pic[col_idx_ext["EXPIRED_DATE"]],
                )
            )

    email_lines.extend(build_email_footer())
    return "\n".join(email_lines)


def format_mokas_email_body(
    period_type: str, period_value: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    email_lines = [
        "Dear Bapak COO,",
        "",
        f"Dengan ini kami sampaikan daftar Pemilik Dealer Mokas yang berulang tahun pada {period_type} ({period_value}), dengan rincian sebagai berikut:",
        "",
    ]

    for pic in pic_list:
        nama = format_name_title_case(pic[col_idx["NAMA_PEMILIK"]])
        dealer = format_name_title_case(pic[col_idx["NAMA_DEALER"]])
        cabang = format_name_title_case(pic[col_idx["CABANG"]])
        tgl_lahir = format_date_indonesian(pic[col_idx["TANGGAL_LAHIR"]])
        no_hp = pic[col_idx["NO_HP"]] or "-"

        email_lines.append(
            f"👤 {nama} - {dealer} ({cabang})\t\t🎂 Tgl Lahir : {tgl_lahir}\t\t📱 HP : {no_hp}"
        )

    email_lines.extend(
        [
            "",
            "Mohon agar data tersebut dapat direview dan dikoordinasikan untuk pemberian greeting atau apresiasi kepada mitra dealer terkait.",
            "",
            "Atas perhatian dan kerja samanya, kami ucapkan terima kasih.",
        ]
    )

    return "\n".join(email_lines)
