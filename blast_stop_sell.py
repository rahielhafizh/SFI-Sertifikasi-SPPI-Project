import os
import time
import keyboard
import pyautogui
import win32com.client
from datetime import datetime
from general_task import *
from pynput.keyboard import Key, Controller
from services.config import load_config, wait_timer, logger
from outlook_stopsell import send_outlook_email
from services.capslock_checker import capslock_checking
from services.remover_stopsell import clear_submission_folder
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

CONFIG = load_config()
keyboard = Controller()


def get_current_date_info():
    current_date = datetime.now()
    english_month = current_date.strftime("%B")
    month_name_id = CONFIG["MONTHS_ID"].get(english_month, english_month)
    year = current_date.year
    day = current_date.day
    subject_text = f"{month_name_id} {year}"
    filename_text = f"{day} {month_name_id} {year}"
    return subject_text, filename_text


def excel_config():
    subject_text, filename_text = get_current_date_info()

    os.startfile(CONFIG["WORKSOURCE_STOPSELL"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    handle_office()
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])

    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    select_sheet_down()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])

    break_excel_link()
    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_STOPSELL"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()

    stopsell_filename = (
        f"Report Penugasan dan Kunjungan Cabang Stop Sell As of {filename_text}"
    )

    pyautogui.write(stopsell_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])

    close_no_save()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])

    switch_to_first_sheet()
    for _ in range(2):
        pyautogui.hotkey("ctrl", "pagedown")

    switch_to_first_cells()
    close_with_save()

    created_file_path = os.path.join(
        CONFIG["SUBMISSION_STOPSELL"], f"{stopsell_filename}.xlsx"
    )

    return created_file_path, stopsell_filename, subject_text


def send_email(subject_text):
    outlook_recipients = "asset.mgmt@sfi.co.id"
    secondary_recipients = ["CollHO.3@sfi.co.id"]

    subject_email = (
        f"Report Penugasan dan Kunjungan Cabang Stop Sell As of {subject_text}"
    )

    core_email = f"""Dear All,

Dengan hormat,

Summary Penugasan dan Kunjungan Cabang Stop Sell As of {subject_text}

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


if __name__ == "__main__":
    logger.info("[SYSTEM] INITIALISING AUTOMATION PROCESS FOR STOP SELL REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUBMISSION_STOPSELL"])
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    created_file_path, filename, subject_text = excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    logger.info(f"[SYSTEM] EXCEL FILE CREATED: {filename}")
    logger.info(f"[SYSTEM] FILE PATH: {created_file_path}")

    send_email(subject_text)
    logger.info("[SYSTEM] AUTOMATION PROCESS COMPLETED SUCCESSFULLY")

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER SERVICE")
    run_screen_keeper()
