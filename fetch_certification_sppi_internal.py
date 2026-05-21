from typing import Optional

from services.db_connection import get_database_connection
from services.config import (
    load_config,
    wait_timer,
    logger,
    get_branch_order,
    get_certification_filter_config,
    set_certification_filter_preset,
)
from services.database_queries import fetch_certification_data_internal
from services.certification_utils import (
    filter_expiring_certifications,
    group_by_branch,
    extract_branch_manager_info,
)
from services.email_formatter import format_internal_email_body
from services.email_sender import send_certification_email

CONFIG = load_config()

def process_internal_certification_reminders(
    filter_preset: Optional[str] = None, minimize_after_send: bool = True
) -> bool:
    if filter_preset and not set_certification_filter_preset(filter_preset):
        logger.error(f"[ERROR] FAILED TO SET FILTER PRESET : {filter_preset}, USING DEFAULT")

    conn = get_database_connection()
    if not conn:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info("[SYSTEM] FETCHING INTERNAL CERTIFICATION DATA FROM DATABASE")
        columns, rows = fetch_certification_data_internal(conn)

        if not columns or rows is None:
            logger.error("[ERROR] FAILED TO FETCH DATA FROM DATABASE")
            return False

        if not rows:
            logger.warning("[WARNING] NO DATA FOUND IN DATABASE")
            return False

        filtered_rows = filter_expiring_certifications(columns, rows, "EXPIRED_DATE")
        logger.info(f"[SYSTEM] FILTERED {len(filtered_rows)} ROWS BASED ON ACTIVE FILTER")

        if not filtered_rows:
            logger.info("[SYSTEM] NO EXPIRING CERTIFICATIONS FOUND")
            return True

        branch_groups = group_by_branch(columns, filtered_rows, "BRANCH_NAME")
        logger.info(f"[SYSTEM] GROUPED DATA INTO {len(branch_groups)} BRANCHES")

        column_indices = {col: idx for idx, col in enumerate(columns)}
        branch_order = get_branch_order()
        processed_count, failed_count = 0, 0

        for branch_name in branch_order:
            pic_list = branch_groups.get(branch_name)
            if not pic_list:
                continue

            branch_manager, bm_mail = extract_branch_manager_info(
                pic_list, column_indices, "BRANCH_MANAGER", "BM_MAIL"
            )

            if not branch_manager or not bm_mail:
                logger.warning(f"[WARNING] MISSING BRANCH MANAGER INFO FOR {branch_name}, SKIPPING")
                failed_count += 1
                continue

            email_body = format_internal_email_body(
                branch_name, branch_manager, pic_list, columns
            )

            success = send_certification_email(
                branch_name, branch_manager, bm_mail, email_body, minimize_after_send
            )

            if success:
                processed_count += 1
            else:
                failed_count += 1

            wait_timer(CONFIG.get("WAIT_TIME", {}).get("THREE_SECOND", 3))

        logger.info(
            f"[SYSTEM] INTERNAL CERTIFICATION REMINDER PROCESS COMPLETED : "
            f"{processed_count} EMAILS SENT, {failed_count} FAILED"
        )
        return True

    except Exception as e:
        logger.error(f"[ERROR] INTERNAL CERTIFICATION REMINDER PROCESS FAILED : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")

if __name__ == "__main__":
    process_internal_certification_reminders()
    # process_internal_certification_reminders(filter_preset="SIX_MONTHS")