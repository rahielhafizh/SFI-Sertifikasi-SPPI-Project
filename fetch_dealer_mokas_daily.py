from datetime import datetime
from services.db_connection import get_database_connection
from services.config import load_config, logger, get_month_id
from services.database_mokas import fetch_dealer_mokas_data
from services.mokas_utils import filter_mokas_birthdays, sort_by_birth_date
from services.mokas_formatter import format_mokas_daily_email_body
from services.email_sender import send_mokas_email
from services.sppi_utils import parse_date

CONFIG = load_config()
TARGET_EMAIL = "herberth.simbolon@sfi.co.id"


def get_mokas_birthdays_daily(minimize_after_send: bool = True) -> bool:
    conn = get_database_connection()
    if not conn:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info("[SYSTEM] FETCHING DEALER MOKAS DATA FROM DATABASE")
        columns, rows = fetch_dealer_mokas_data(conn)

        if not columns or rows is None:
            logger.error("[ERROR] FAILED TO FETCH DATA FROM DATABASE")
            return False

        if not rows:
            logger.warning("[WARNING] NO DATA FOUND IN DATABASE")
            return False

        filtered_rows = filter_mokas_birthdays(columns, rows, "DAILY")
        logger.info(f"[SYSTEM] FILTERED {len(filtered_rows)} DAILY ROWS")

        if not filtered_rows:
            logger.info("[SYSTEM] NO MOKAS BIRTHDAYS FOUND FOR TODAY OR UPCOMING DAYS")
            return True

        sorted_rows = sort_by_birth_date(columns, filtered_rows)
        today = datetime.now()
        birth_date_idx = columns.index("TANGGAL_LAHIR")
        check_today_birthdays = any(
            (d := parse_date(row[birth_date_idx])) is not None
            and d.month == today.month
            and d.day == today.day
            for row in sorted_rows
        )

        today_date_str = (
            f"{today.day} {get_month_id(today.strftime('%B'), 'title')} {today.year}"
        )

        unique_dates = []
        for row in sorted_rows:
            bdate = parse_date(row[birth_date_idx])
            if bdate:
                month_name = get_month_id(bdate.strftime("%B"), "title")
                date_str = f"{bdate.day} {month_name}"
                if date_str not in unique_dates:
                    unique_dates.append(date_str)

        if len(unique_dates) > 1:
            period_value = " & ".join(unique_dates) + f" {today.year}"
        elif len(unique_dates) == 1:
            period_value = f"{unique_dates[0]} {today.year}"
        else:
            period_value = today_date_str

        email_body = format_mokas_daily_email_body(
            sorted_rows, columns, check_today_birthdays, today_date_str
        )
        subject = (
            f"Pemberitahuan Ulang Tahun Pemilik Dealer Mokas Harian ({period_value})"
        )

        success = send_mokas_email(
            TARGET_EMAIL, subject, email_body, minimize_after_send=minimize_after_send
        )

        if success:
            logger.info("[SYSTEM] DAILY MOKAS EMAIL SENT SUCCESSFULLY")
        else:
            logger.error("[ERROR] FAILED TO SEND DAILY MOKAS EMAIL")

        return success

    except Exception as e:
        logger.error(f"[ERROR] DAILY MOKAS PROCESS FAILED : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")


if __name__ == "__main__":
    get_mokas_birthdays_daily()
