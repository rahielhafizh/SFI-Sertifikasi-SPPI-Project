from datetime import datetime
from services.db_connection import get_database_connection
from services.config import load_config, logger, get_month_id
from services.database_mokas import fetch_dealer_mokas_data
from services.mokas_utils import filter_mokas_birthdays, sort_by_birth_date
from services.mokas_formatter import format_mokas_whatsapp_body
from services.sppi_utils import parse_date
from services.whatsapp_sender import send_paste_report

CONFIG = load_config()


def check_today_birthday(rows, columns, today):
    birth_date_idx = columns.index("TANGGAL_LAHIR")
    return any(
        (d := parse_date(row[birth_date_idx])) is not None
        and d.month == today.month
        and d.day == today.day
        for row in rows
    )


def get_mokas_birthdays_whatsapp() -> bool:
    conn = get_database_connection()
    if not conn:
        logger.error("[ERROR] DATABASE CONNECTION UNAVAILABLE")
        return False

    try:
        logger.info("[SYSTEM] FETCHING DEALER MOBIL BEKAS DATA FOR WHATSAPP REMINDER")
        columns, rows = fetch_dealer_mokas_data(conn)

        if not columns or rows is None:
            logger.error("[ERROR] FAILED TO FETCH DATA FROM DATABASE")
            return False

        if not rows:
            logger.warning("[WARNING] NO DATA FOUND IN DATABASE")
            return False

        filtered_rows = filter_mokas_birthdays(columns, rows, "DAILY")
        logger.info(f"[SYSTEM] FILTERED {len(filtered_rows)} DAILY ROWS FOR WHATSAPP")

        if not filtered_rows:
            logger.info("[SYSTEM] NO BIRTHDAYS FOUND FOR TODAY OR UPCOMING DAYS")
            return True

        sorted_rows = sort_by_birth_date(columns, filtered_rows)
        today = datetime.now()

        today_date_str = (
            f"{today.day} {get_month_id(today.strftime('%B'), 'title')} {today.year}"
        )

        am_grouped = {}
        bm_grouped = {}
        am_name_idx = columns.index("NAMA_AM")
        am_no_idx = columns.index("NO_AM")
        map_area_idx = columns.index("MAPPING_AREA")
        bm_name_idx = columns.index("NAMA_BM")
        bm_no_idx = columns.index("NO_BM")
        map_cabang_idx = columns.index("MAPPING_CABANG")

        for row in sorted_rows:
            no_am = row[am_no_idx]
            nama_am = row[am_name_idx]
            map_area = row[map_area_idx]
            if no_am and nama_am and map_area:
                am_key = (no_am, nama_am, map_area)
                if am_key not in am_grouped:
                    am_grouped[am_key] = []
                am_grouped[am_key].append(row)

            no_bm = row[bm_no_idx]
            nama_bm = row[bm_name_idx]
            map_cabang = row[map_cabang_idx]
            if no_bm and nama_bm and map_cabang:
                bm_key = (no_bm, nama_bm, map_cabang)
                if bm_key not in bm_grouped:
                    bm_grouped[bm_key] = []
                bm_grouped[bm_key].append(row)

        # 1. COO
        logger.info("[WHATSAPP] PREPARING TO SEND TO COO")
        coo_check = check_today_birthday(sorted_rows, columns, today)
        coo_msg = format_mokas_whatsapp_body(
            "Herberth Simbolon", "COO", sorted_rows, columns, coo_check, today_date_str
        )
        try:
            send_paste_report("082311919875", coo_msg)
        except Exception as e:
            logger.error(f"[ERROR] WHATSAPP FAILED TO SEND TO COO: {e}")

        # 2. GM Sales & Marketing
        logger.info("[WHATSAPP] PREPARING TO SEND TO GM")
        gm_check = check_today_birthday(sorted_rows, columns, today)
        gm_msg = format_mokas_whatsapp_body(
            "Brian Yekti Budi",
            "GM Sales & Marketing",
            sorted_rows,
            columns,
            gm_check,
            today_date_str,
        )
        try:
            send_paste_report("08128558052", gm_msg)
        except Exception as e:
            logger.error(f"[ERROR] WHATSAPP FAILED TO SEND TO GM: {e}")

        # 3. Area Manager
        for (no_am, nama_am, map_area), rows_am in am_grouped.items():
            logger.info(f"[WHATSAPP] PREPARING TO SEND TO AM {nama_am} ({map_area})")
            am_check = check_today_birthday(rows_am, columns, today)
            am_msg = format_mokas_whatsapp_body(
                nama_am, f"AM {map_area}", rows_am, columns, am_check, today_date_str
            )
            try:
                send_paste_report(no_am, am_msg)
            except Exception as e:
                logger.error(f"[ERROR] WHATSAPP FAILED TO SEND TO AM {nama_am}: {e}")

        # 4. Branch Manager
        for (no_bm, nama_bm, map_cabang), rows_bm in bm_grouped.items():
            logger.info(f"[WHATSAPP] PREPARING TO SEND TO BM {nama_bm} ({map_cabang})")
            bm_check = check_today_birthday(rows_bm, columns, today)
            bm_msg = format_mokas_whatsapp_body(
                nama_bm, f"BM {map_cabang}", rows_bm, columns, bm_check, today_date_str
            )
            try:
                send_paste_report(no_bm, bm_msg)
            except Exception as e:
                logger.error(f"[ERROR] WHATSAPP FAILED TO SEND TO BM {nama_bm}: {e}")

        logger.info("[SYSTEM] WHATSAPP NOTIFICATION PROCESS COMPLETED")
        return True

    except Exception as e:
        logger.error(f"[ERROR] WHATSAPP PROCESS CRITICAL FAILURE : {e}")
        return False
    finally:
        conn.close()
        logger.info("[SYSTEM] DATABASE CONNECTION CLOSED")


if __name__ == "__main__":
    get_mokas_birthdays_whatsapp()
