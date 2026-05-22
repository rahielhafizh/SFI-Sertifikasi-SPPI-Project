from typing import Optional
from services.db_connection import get_database_connection
from services.sppi_formatter import format_combined_email_body
from services.email_sender import send_certification_email
from services.database_sppi import (
    fetch_certification_data_internal,
    fetch_certification_data_external,
)
from services.sppi_utils import (
    filter_expiring_certifications,
    group_by_branch,
    extract_branch_manager_info,
)
from services.config import (
    load_config,
    wait_timer,
    logger,
    get_branch_order,
    set_certification_filter_preset,
)

CONFIG = load_config()


def process_combined_certification_reminders(
    filter_preset: Optional[str] = None, minimize_after_send: bool = True
) -> bool:
    if filter_preset and not set_certification_filter_preset(filter_preset):
        logger.error(
            f"[ERROR] FAILED TO SET FILTER PRESET : {filter_preset}, USING DEFAULT"
        )

    conn = get_database_connection()
    if not conn:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info(
            "[SYSTEM] FETCHING INTERNAL & EXTERNAL CERTIFICATION DATA FROM DATABASE"
        )
        columns_internal, rows_internal = fetch_certification_data_internal(conn)
        columns_external, rows_external = fetch_certification_data_external(conn)

        if not columns_internal or not columns_external:
            logger.error(
                "[ERROR] FAILED TO FETCH ONE OR MORE DATA SOURCES FROM DATABASE"
            )
            return False

        filtered_internal = filter_expiring_certifications(
            columns_internal, rows_internal, "EXPIRED_DATE"
        )
        filtered_external = filter_expiring_certifications(
            columns_external, rows_external, "EXPIRED_DATE"
        )

        logger.info(
            f"[SYSTEM] FILTERED {len(filtered_internal)} INTERNAL + {len(filtered_external)} EXTERNAL ROWS"
        )

        branch_groups_internal = group_by_branch(
            columns_internal, filtered_internal, "BRANCH_NAME"
        )
        branch_groups_external = group_by_branch(
            columns_external, filtered_external, "BRANCH"
        )

        all_branches = set(branch_groups_internal.keys()) | set(
            branch_groups_external.keys()
        )
        logger.info(f"[SYSTEM] GROUPED DATA INTO {len(all_branches)} UNIQUE BRANCHES")

        if not all_branches:
            logger.info("[SYSTEM] NO EXPIRING CERTIFICATIONS FOUND")
            return True

        column_indices_internal = {col: idx for idx, col in enumerate(columns_internal)}
        column_indices_external = {col: idx for idx, col in enumerate(columns_external)}
        branch_order = get_branch_order()
        processed_count, failed_count = 0, 0

        for branch_name in branch_order:
            internal_pic_list = branch_groups_internal.get(branch_name, [])
            external_pic_list = branch_groups_external.get(branch_name, [])

            if not internal_pic_list and not external_pic_list:
                continue

            branch_manager, bm_mail = None, None

            if internal_pic_list:
                branch_manager, bm_mail = extract_branch_manager_info(
                    internal_pic_list,
                    column_indices_internal,
                    "BRANCH_MANAGER",
                    "BM_MAIL",
                )
            elif external_pic_list:
                branch_manager, bm_mail = extract_branch_manager_info(
                    external_pic_list,
                    column_indices_external,
                    "BRANCH_MANAGER",
                    "BM_MAIL",
                )

            if not branch_manager or not bm_mail:
                logger.warning(
                    f"[WARNING] MISSING BRANCH MANAGER INFO FOR {branch_name}, SKIPPING"
                )
                failed_count += 1
                continue

            email_body = format_combined_email_body(
                branch_name,
                branch_manager,
                internal_pic_list,
                external_pic_list,
                columns_internal,
                columns_external,
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
            f"[SYSTEM] COMBINED CERTIFICATION REMINDER PROCESS COMPLETED : "
            f"{processed_count} EMAILS SENT, {failed_count} FAILED"
        )
        return True

    except Exception as e:
        logger.error(f"[ERROR] COMBINED CERTIFICATION REMINDER PROCESS FAILED : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")


if __name__ == "__main__":
    process_combined_certification_reminders()
    # process_combined_certification_reminders(filter_preset="SIX_MONTHS")
