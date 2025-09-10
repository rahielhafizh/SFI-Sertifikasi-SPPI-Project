import os
import pyautogui
from datetime import datetime
from outlook_pivot import *
from general_task import *
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger
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
    logger.info("[SYSTEM] STARTING EXCEL WORKFLOW FOR SUMMARY PIC ACTIVITY")

    os.startfile(CONFIG["WORKSOURCE_PIC"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])

    maximize_app_window()
    switch_to_first_sheet()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])

    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()
    switch_to_first_sheet()
    switch_to_first_cells()

    close_with_save()
    logger.info("[SYSTEM] EXCEL WORKFLOW COMPLETED SUCCESSFULLY")


def send_email():
    outlook_recipients = "herberth.simbolon@sfi.co.id"
    secondary_recipients = ["asset.mgmt@sfi.co.id"]

    current_time = datetime.now()
    subject_email = f"SUMMARY UPDATE (PENUGASAN DAN KUNJUNGAN) - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    core_email = f"""Yth. Bapak Chief Of Operating Officer,

Dengan hormat,

Berikut terlampir laporan aktivitas PIC yang telah dilaksanakan pada : {current_time.strftime('%d-%m-%Y')} Pukul {current_time.strftime('%H:%M')} WIB.

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data diperoleh secara real-time namun harap diperhatikan dan dievaluasi kembali.
"""

    footer_template = """
Hormat kami,
Asset Management Division
Collection Head Office
PT Suzuki Finance Indonesia
"""

    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )
    logger.info("[DATA] PIC SUMMARY EMAIL SENT SUCCESSFULLY")


def validate_and_send_email():
    is_valid = validate_pic_data_for_email()
    if is_valid:
        logger.info("[VALIDATION] PIC DATA PASSED - PROCEEDING WITH EMAIL")
        send_email()
        return

    else:
        logger.warning("[VALIDATION] PIC DATA FAILED - EMAIL NOT SENT")
        details = get_pic_validation_details()

        if "results" in details:
            for result in details["results"]:
                if not result["valid"]:
                    logger.warning(
                        f"[VALIDATION] CELL {result['cell']} : "
                        f"(EXPECTED {details['expected_date']}), FOUND: {result['actual']}"
                    )

        return False


if __name__ == "__main__":
    logger.info("[SYSTEM] INITIALISING AUTOMATION PROCESS FOR PIC SUMMARY REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    email_sent = validate_and_send_email()

    if email_sent:
        logger.info("[SYSTEM] AUTOMATION COMPLETED SUCCESSFULLY WITH EMAIL SENT")
    else:
        logger.warning(
            "[SYSTEM] AUTOMATION COMPLETED BUT EMAIL WAS SKIPPED DUE TO VALIDATION FAILURE"
        )

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER SERVICE")
    run_screen_keeper()
