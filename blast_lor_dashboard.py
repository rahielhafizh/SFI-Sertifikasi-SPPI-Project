import os
import pyautogui
from datetime import datetime, timedelta
from outlook_lor import send_outlook_email
from general_task import *
from pynput.keyboard import Key, Controller
from services.config import load_config, wait_timer, logger, get_month_id
from services.remover_lor import clear_submission_folder
from services.capslock_checker import capslock_checking
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

CONFIG = load_config()
keyboard = Controller()


def excel_config():
    logger.info("[SYSTEM] INITIATING EXCEL WORKFLOW FOR LOR PREDICTION")

    os.startfile(CONFIG["WORKSOURCE_LOR"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])

    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_MINUTE"])

    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    select_sheet_order_in()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    break_excel_link()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_LOR"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    # DATE IS SET TO YESTERDAY TO AVOID INCOMPLETE DATA
    yesterday = datetime.now() - timedelta(days=1)
    lor_day = yesterday.strftime("%d")
    lor_year = yesterday.strftime("%Y")
    month_eng = yesterday.strftime("%B")
    month_idn_upper = get_month_id(month_eng, case="upper")

    lor_filename = f"REPORT MOBCOLL LOR PERIODE {lor_day} {month_idn_upper} {lor_year}"
    pyautogui.write(lor_filename, interval=0.05)
    confirm()

    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    close_no_save()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    switch_to_first_sheet()
    switch_to_first_cells()
    close_with_save()

    logger.info("[SYSTEM] EXCEL WORKFLOW COMPLETED SUCCESSFULLY")


def send_email():
    outlook_recipients = "asset.mgmt@sfi.co.id"
    secondary_recipients = ["CollHO.3@sfi.co.id"]

    yesterday = datetime.now() - timedelta(days=1)
    lor_year = yesterday.strftime("%Y")
    month_eng = yesterday.strftime("%B")
    month_idn_upper = get_month_id(month_eng, case="upper")
    month_idn_title = get_month_id(month_eng, case="title")

    subject_email = (
        f"SUMMARY UPDATE REPORT MOBCOLL LOR PERIODE {month_idn_upper} {lor_year}"
    )

    core_email = f"""Dear All,

Dengan hormat,
Berikut terlampir Summary Update Penugasan Mobile Collection LOR pada Periode {month_idn_title} {lor_year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Harap diperhatikan serta dapat dievaluasi kembali.

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
    logger.info("[DATA] EMAIL SENT SUCCESSFULLY")


if __name__ == "__main__":
    logger.info("[SYSTEM] INITIALISING AUTOMATION PROCESS FOR LOR PREDICTION REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUBMISSION_LOR"])
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    send_email()
    logger.info("[SYSTEM] AUTOMATION PROCESS COMPLETED SUCCESSFULLY")

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER SERVICE")
    run_screen_keeper()
