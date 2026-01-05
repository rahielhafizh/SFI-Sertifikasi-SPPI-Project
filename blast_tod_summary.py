import os
import pyautogui
from datetime import datetime, timedelta
from general_task import *
from pynput.keyboard import Controller
from services.remover_tod_report import clear_submission_folder
from services.config import load_config, wait_timer, logger, get_month_id
from outlook_tod_report import send_outlook_email
from services.capslock_checker import capslock_checking
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

pyautogui.FAILSAFE = False
CONFIG = load_config()
keyboard = Controller()


def excel_config():
    logger.info("[SYSTEM] REPORT TOD PERFORMANCE EXCEL WORKFLOW")
    os.startfile(CONFIG["WORKSOURCE_TOD"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTYFIVE_SECOND"])
    maximize_app_window()

    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    switch_to_first_sheet()
    switch_to_first_cells()
    move_cell_horizontal()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])

    move_cell_horizontal()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    entering_operation()

    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_first_cells()

    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["FORTYFIVE_SECOND"])

    switch_to_first_sheet()
    break_excel_link()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_TOD"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    today = datetime.now() - timedelta(days=1)
    tod_report_day = today.strftime("%d")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    tod_report_filename = f"Summary Performance TOD {tod_report_day} {month_idn_title}"
    pyautogui.write(tod_report_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])

    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    switch_to_first_cells()
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_right_sheet()

    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def send_email():
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = "collho.3@sfi.co.id"

    today = datetime.now() - timedelta(days=1)
    tod_report_day = today.strftime("%d")
    tod_report_year = today.strftime("%Y")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Performance AR & TOD | {tod_report_day} {month_idn_title} {tod_report_year}"

    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Performance AR & TOD {tod_report_day} {month_idn_title} {tod_report_year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

"""

    footer_template = """
    

Hormat kami,
Asset Management Division
Collection HO - PT Suzuki Finance Indonesia
"""

    send_outlook_email(
        outlook_recipients,
        secondary_recipients,
        subject_email,
        core_email,
        footer_template,
    )


if __name__ == "__main__":
    logger.info("[SYSTEM] EXECUTING PERFORMANCE TOD REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUBMISSION_TOD"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] PERFORMANCE TOD REPORT SENT")

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME : {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
