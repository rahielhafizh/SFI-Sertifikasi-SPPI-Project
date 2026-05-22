from datetime import datetime
from services.db_connection import get_database_connection
from services.config import load_config, logger, get_month_id
from services.database_mokas import fetch_dealer_mokas_data
from services.mokas_utils import filter_mokas_birthdays, sort_by_birth_date
from services.mokas_formatter import format_mokas_monthly_email_body
from services.email_sender import send_mokas_email

CONFIG = load_config()
TARGET_EMAIL = "herberth.simbolon@sfi.co.id"


def get_mokas_birthdays_monthly(minimize_after_send: bool = True) -> bool:
    conn = get_database_connection()
    if not conn:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info("[SYSTEM] FETCHING DEALER MOKAS DATA FROM DATABASE")
        result = fetch_dealer_mokas_data(conn)

        if not isinstance(result, tuple) or len(result) != 2:
            logger.error(
                "[ERROR] UNEXPECTED RETURN FORMAT FROM fetch_dealer_mokas_data"
            )
            return False

        columns, rows = result

        if not isinstance(columns, list) or not isinstance(rows, list):
            logger.error("[ERROR] FAILED TO FETCH DATA FROM DATABASE")
            return False

        if not rows:
            logger.warning("[WARNING] NO DATA FOUND IN DATABASE")
            return False

        filtered_rows = filter_mokas_birthdays(columns, rows, "MONTHLY")
        logger.info(f"[SYSTEM] FILTERED {len(filtered_rows)} MONTHLY ROWS")

        if not filtered_rows:
            logger.info("[SYSTEM] NO MOKAS BIRTHDAYS FOUND FOR THIS MONTH")
            return True

        sorted_rows = sort_by_birth_date(columns, filtered_rows)

        today = datetime.now()
        period_value = (
            f"{get_month_id(today.strftime('%B'), case='title')} {today.year}"
        )

        email_body = format_mokas_monthly_email_body(period_value, sorted_rows, columns)
        subject = f"Pemberitahuan Ulang Tahun Pemilik Dealer Mokas - {period_value}"

        success = send_mokas_email(
            TARGET_EMAIL, subject, email_body, minimize_after_send=minimize_after_send
        )

        if success:
            logger.info("[SYSTEM] MONTHLY MOKAS EMAIL SENT SUCCESSFULLY")
        else:
            logger.error("[ERROR] FAILED TO SEND MONTHLY MOKAS EMAIL")

        return success

    except Exception as e:
        logger.error(f"[ERROR] MONTHLY MOKAS PROCESS FAILED : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")


if __name__ == "__main__":
    get_mokas_birthdays_monthly()
