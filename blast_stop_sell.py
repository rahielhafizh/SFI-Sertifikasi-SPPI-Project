import os
import pyautogui
from datetime import datetime, timedelta
from general_task import *
from pynput.keyboard import Controller
from services.config import load_config, wait_timer, logger, get_month_id
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


def excel_config():
    logger.info("[SYSTEM] STOPSELL REPORT EXCEL WORKFLOW")

    yesterday = datetime.now() - timedelta(days=1)
    year = yesterday.strftime("%Y")
    month_eng = yesterday.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_text = f"{month_idn_title} {year}"
    body_text = f"{month_idn_title} {year}"
    filename_text = f"{yesterday.day} {month_idn_title} {year}"

    os.startfile(CONFIG["WORKSOURCE_STOPSELL"])
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_MINUTE"])
    entering_operation()

    switch_to_right_sheet()
    select_sheet_half_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])

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
        f"Summary Penugasan & Kunjungan Cabang Stop Sell ({filename_text})"
    )
    pyautogui.write(stopsell_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])

    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    switch_to_first_sheet()
    switch_to_right_sheet()
    switch_to_first_cells()

    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    return subject_text, body_text


def send_email(subject_text, body_text):
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = "collho.3@sfi.co.id"

    subject_email = (
        f"Summary Penugasan & Kunjungan Cabang Stop Sell As Of | {subject_text}"
    )

    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Penugasan dan Kunjungan Cabang Stop Sell As of {body_text}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.
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


def main():
    logger.info("[SYSTEM] START STOP SELL REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUBMISSION_STOPSELL"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    subject_text, body_text = excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email(subject_text, body_text)
    logger.info("[SYSTEM] STOP SELL REPORT COMPLETED")

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()


if __name__ == "__main__":
    main()
