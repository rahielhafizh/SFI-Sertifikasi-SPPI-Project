import os
from datetime import datetime
from outlook_pivot import *
from general_task import *
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger, get_month_id
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)
from data_validate_pic_mail import (
    validate_pic_data_for_email,
    get_pic_validation_details,
)

CONFIG = load_config()


def excel_config():
    logger.info("[SYSTEM] MOBCOLL REGULER EXCEL WORKFLOW")
    os.startfile(CONFIG["WORKSOURCE_PIC"])
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    maximize_app_window()
    switch_to_first_sheet()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["FORTYFIVE_SECOND"])
    entering_operation()

    switch_to_right_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()

    switch_to_first_cells()
    switch_to_first_sheet()
    switch_to_first_cells()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def send_email():
    outlook_recipients = "herberth.simbolon@sfi.co.id"
    secondary_recipients = ["asset.mgmt@sfi.co.id"]

    today = datetime.now()
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")

    subject_email = f"Summary Penugasan & Kunjungan Mobcoll Reguler | {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"
    core_email = f"""Yth. Bapak Chief of Operating Officer,

Dengan hormat,

Berikut terlampir laporan aktivitas PIC yang telah dilaksanakan pada {today.strftime('%d')} {month_idn_title} pukul {today.strftime('%H:%M')} WIB.

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data diperoleh secara real-time namun harap diperhatikan dan dievaluasi kembali.
"""

    footer_template = """

Hormat kami,
Asset Management Division.
Collection HO - PT Suzuki Finance Indonesia.
"""

    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )
    logger.info("[DATA] MOBCOLL REGULER REPORT SENT")


def validate_and_send_email():
    is_valid = validate_pic_data_for_email()
    if is_valid:
        logger.info("[VALIDATION] MOBCOLL REGULER DATA SUCCESS")
        send_email()
        return

    else:
        logger.warning("[VALIDATION] MOBCOLL REGULER DATA FAILED")
        details = get_pic_validation_details()

        if "results" in details:
            for result in details["results"]:
                if not result["valid"]:
                    logger.warning(f"[WARNING] CELL {result['cell']} VAKUE | ")

        return False


if __name__ == "__main__":
    logger.info("[SYSTEM] START MOBCOLL REGULER REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    email_sent = validate_and_send_email()

    if email_sent:
        logger.info("[SYSTEM] MOBCOLL REGULER REPORT SENT")
    else:
        logger.warning("[SYSTEM] MOBCOLL REGULER REPORT FAILED")

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
