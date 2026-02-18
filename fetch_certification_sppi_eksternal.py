import pyodbc
from typing import Optional
from services.db_connection import get_database_connection
from services.email_sender import send_certification_email
from services.email_formatter import format_external_email_body
from services.config import (
    load_config,
    wait_timer,
    logger,
    get_branch_order,
    get_certification_filter_config,
    set_certification_filter_preset,
)
from services.database_queries import fetch_certification_data_external
from services.certification_utils import (
    filter_expiring_certifications,
    group_by_branch,
    extract_branch_manager_info,
)

CONFIG = load_config()


def process_external_certification_reminders(
    filter_preset: Optional[str] = None, minimize_after_send: bool = True
) -> bool:
    if filter_preset:
        if not set_certification_filter_preset(filter_preset):
            logger.error(
                f"[ERROR] FAILED TO SET FILTER PRESET : {filter_preset}, USING DEFAULT"
            )

    conn = get_database_connection()
    if conn is None:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info("[SYSTEM] FETCHING EXTERNAL CERTIFICATION DATA FROM DATABASE")
        columns, rows = fetch_certification_data_external(conn)

        if columns is None or rows is None:
            logger.error("[ERROR] FAILED TO FETCH DATA FROM DATABASE")
            return False

        if len(rows) == 0:
            logger.warning("[WARNING] NO DATA FOUND IN DATABASE")
            return False

        filtered_rows = filter_expiring_certifications(columns, rows, "EXPIRED_DATE")
        active_filter = get_certification_filter_config()
        logger.info(f"[SYSTEM] FILTERED {len(filtered_rows)} ROWS")

        if len(filtered_rows) == 0:
            logger.info("[SYSTEM] NO EXPIRING CERTIFICATIONS FOUND")
            return True

        branch_groups = group_by_branch(columns, filtered_rows, "BRANCH")
        logger.info(f"[SYSTEM] GROUPED DATA INTO {len(branch_groups)} BRANCHES")
        column_indices = {col: idx for idx, col in enumerate(columns)}
        branch_order = get_branch_order()
        processed_count = 0
        failed_count = 0

        for branch_name in branch_order:
            if branch_name not in branch_groups:
                continue

            pic_list = branch_groups[branch_name]

            branch_manager, bm_mail = extract_branch_manager_info(
                pic_list, column_indices, "BRANCH_MANAGER", "BM_MAIL"
            )

            if not branch_manager or not bm_mail:
                logger.warning(
                    f"[WARNING] MISSING BRANCH MANAGER INFO FOR {branch_name}, SKIPPING"
                )
                failed_count += 1
                continue

            email_body = format_external_email_body(
                branch_name, branch_manager, pic_list, columns
            )

            success = send_certification_email(
                branch_name, branch_manager, bm_mail, email_body, minimize_after_send
            )

            if success:
                processed_count += 1
            else:
                failed_count += 1

            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        logger.info(
            f"[SYSTEM] EXTERNAL CERTIFICATION REMINDER PROCESS COMPLETED : "
            f"{processed_count} EMAILS SENT, {failed_count} FAILED"
        )
        return True

    except Exception as e:
        logger.error(f"[ERROR] EXTERNAL CERTIFICATION REMINDER PROCESS FAILED : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")


if __name__ == "__main__":
    # process_external_certification_reminders()  # DEFAULT VALUE (NEXT_MONTH)
    # process_external_certification_reminders(filter_preset="TWO_MONTHS")
    # process_external_certification_reminders(filter_preset="THREE_MONTHS")
    # process_external_certification_reminders(filter_preset="SIX_MONTHS")
    # process_external_certification_reminders(filter_preset="SIXTY_DAYS")
    process_external_certification_reminders(filter_preset="SIX_MONTHS")
