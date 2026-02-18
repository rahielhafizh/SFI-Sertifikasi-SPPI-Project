
from typing import List, Tuple, Dict
from services.certification_utils import (
    build_email_header,
    build_email_footer,
    format_pic_line,
)


def format_internal_email_body(
    branch_name: str, branch_manager: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    column_indices = {col: idx for idx, col in enumerate(columns)}

    email_lines = build_email_header(branch_name, branch_manager)
    email_lines.append("Daftar PIC Internal :")

    for pic in pic_list:
        pic_name = pic[column_indices["PIC_NAME"]]
        job_title = pic[column_indices["JOB_TITLE_CODE"]]
        expired_date = pic[column_indices["EXPIRED_DATE"]]

        email_lines.append(format_pic_line(pic_name, job_title, expired_date))

    email_lines.extend(build_email_footer())

    return "\n".join(email_lines)


def format_external_email_body(
    branch_name: str, branch_manager: str, pic_list: List[Tuple], columns: List[str]
) -> str:
    column_indices = {col: idx for idx, col in enumerate(columns)}

    email_lines = build_email_header(branch_name, branch_manager)
    email_lines.append("Daftar PIC Eksternal :")

    for pic in pic_list:
        pic_name = pic[column_indices["PIC_NAME"]]
        pic_role = pic[column_indices["PIC_ROLE"]]
        expired_date = pic[column_indices["EXPIRED_DATE"]]

        email_lines.append(format_pic_line(pic_name, pic_role, expired_date))

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
    if internal_pic_list and len(internal_pic_list) > 0:
        email_lines.append("PIC Internal :")
        column_indices_internal = {col: idx for idx, col in enumerate(columns_internal)}

        for pic in internal_pic_list:
            pic_name = pic[column_indices_internal["PIC_NAME"]]
            job_title = pic[column_indices_internal["JOB_TITLE_CODE"]]
            expired_date = pic[column_indices_internal["EXPIRED_DATE"]]

            email_lines.append(format_pic_line(pic_name, job_title, expired_date))

    if external_pic_list and len(external_pic_list) > 0:
        if internal_pic_list and len(internal_pic_list) > 0:
            email_lines.append("")

        email_lines.append("PIC Eksternal :")
        column_indices_external = {col: idx for idx, col in enumerate(columns_external)}

        for pic in external_pic_list:
            pic_name = pic[column_indices_external["PIC_NAME"]]
            pic_role = pic[column_indices_external["PIC_ROLE"]]
            expired_date = pic[column_indices_external["EXPIRED_DATE"]]

            email_lines.append(format_pic_line(pic_name, pic_role, expired_date))

    email_lines.extend(build_email_footer())

    return "\n".join(email_lines)
