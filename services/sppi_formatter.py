from typing import List, Tuple

from services.sppi_utils import (
    build_email_header,
    build_email_footer,
    format_pic_line,
)


def format_internal_email_body(
    branch_name: str, branch_manager: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    lines = build_email_header(branch_name, branch_manager)
    lines.extend(
        ["Dengan ini kami lampirkan daftar Person in Charge (PIC) Internal terkait :", ""]
    )

    for pic in pic_list:
        lines.append(
            format_pic_line(
                pic[col_idx["PIC_NAME"]],
                pic[col_idx["JOB_TITLE_CODE"]],
                pic[col_idx["EXPIRED_DATE"]],
            )
        )

    lines.append("")
    lines.extend(build_email_footer())
    return "\n".join(lines)


def format_external_email_body(
    branch_name: str, branch_manager: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    col_idx = {col: idx for idx, col in enumerate(columns)}
    lines = build_email_header(branch_name, branch_manager)
    lines.extend(
        ["Dengan ini kami lampirkan daftar Person in Charge (PIC) Eksternal terkait:", ""]
    )

    for pic in pic_list:
        lines.append(
            format_pic_line(
                pic[col_idx["PIC_NAME"]],
                pic[col_idx["PIC_ROLE"]],
                pic[col_idx["EXPIRED_DATE"]],
            )
        )

    lines.append("")
    lines.extend(build_email_footer())
    return "\n".join(lines)


def format_combined_email_body(
    branch_name: str,
    branch_manager: str,
    internal_pic_list: List[Tuple],
    external_pic_list: List[Tuple],
    columns_internal: List[str],
    columns_external: List[str],
) -> str:
    lines = build_email_header(branch_name, branch_manager)

    if internal_pic_list:
        lines.extend(
            ["Berikut adalah daftar Person in Charge (PIC) Internal terkait:", ""]
        )
        col_idx_int = {col: idx for idx, col in enumerate(columns_internal)}
        for pic in internal_pic_list:
            lines.append(
                format_pic_line(
                    pic[col_idx_int["PIC_NAME"]],
                    pic[col_idx_int["JOB_TITLE_CODE"]],
                    pic[col_idx_int["EXPIRED_DATE"]],
                )
            )

    if external_pic_list:
        if internal_pic_list:
            lines.extend(["", ""])
        lines.extend(
            ["Berikut adalah daftar Person in Charge (PIC) Eksternal terkait:", ""]
        )
        col_idx_ext = {col: idx for idx, col in enumerate(columns_external)}
        for pic in external_pic_list:
            lines.append(
                format_pic_line(
                    pic[col_idx_ext["PIC_NAME"]],
                    pic[col_idx_ext["PIC_ROLE"]],
                    pic[col_idx_ext["EXPIRED_DATE"]],
                )
            )

    lines.append("")
    lines.extend(build_email_footer())
    return "\n".join(lines)
