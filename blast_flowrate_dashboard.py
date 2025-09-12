import os
import time
import keyboard
import pyautogui
import win32com.client
from datetime import datetime
from general_task import *
from pynput.keyboard import Key, Controller
from services.config import load_config, wait_timer, logger
from outlook_flowrate import send_outlook_email
from services.capslock_checker import capslock_checking
from services.remover_flowrate import clear_submission_folder
from data_validate_flowrate_mail import validate_flowrate_file
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

CONFIG = load_config()
keyboard = Controller()


def excel_config():
    os.startfile(CONFIG["WORKSOURCE_FLOWRATE"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    handle_office()
    maximize_app_window()
    switch_to_first_sheet()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_MINUTE"])

    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    switch_to_first_sheet()

    for _ in range(2):
        pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_MINUTE"])

    break_excel_link()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_FLOWRATE"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    flowrate_stamp = datetime.now().strftime("%d-%m ( %H.%M )")
    flowrate_filename = f"REPORT SUMMARY FLOWRATE {flowrate_stamp}"
    pyautogui.write(flowrate_filename, interval=0.05)
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
        CONFIG["SUBMISSION_FLOWRATE"], f"{flowrate_filename}.xlsx"
    )
    return created_file_path


def send_email():
    outlook_recipients = "herberth.simbolon@sfi.co.id"
    secondary_recipients = ["asset.mgmt@sfi.co.id"]

    current_time = datetime.now()
    subject_email = f"SUMMARY UPDATE (PREDIKSI FLOWRATE) - {current_time.strftime('%Y-%m-%d %H:%M')}"

    core_email = f"""Yth. Bapak Chief Operating Officer,

Dengan hormat,
Berikut terlampir Summary Update Daily Flowrate per tanggal {current_time.strftime('%d-%m-%Y')} Pukul {current_time.strftime('%H:%M')} WIB.

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


def validate_and_send_email(created_file_path):
    if not os.path.exists(created_file_path):
        logger.error(f"[ERROR] FILE NOT FOUND : {created_file_path}")
        return False

    validation_result = validate_flowrate_file(created_file_path)
    if validation_result:
        logger.info("[DATA] VALIDATION COMPLETE")
        send_email()
        logger.info("[SYSTEM] EMAIL SUCCESS")
        return True
    else:
        logger.warning("[DATA] VALIDATION FAILED")
        return False


def main():
    start_counter()
    try:
        capslock_checking()
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        clear_submission_folder(target_folder=CONFIG["SUBMISSION_FLOWRATE"])
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        find_screen_keeper_process()
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
        stop_screen_keeper()
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        created_file_path = excel_config()
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        if not created_file_path or not os.path.exists(created_file_path):
            logger.error("[ERROR] REPORT NOT CREATED")
        else:
            logger.info(
                f"[SYSTEM] REPORT CREATED : {os.path.basename(created_file_path)}"
            )
            if validate_and_send_email(created_file_path):
                logger.info("[SYSTEM] PROCESSING REPORT")
            else:
                logger.warning("[SYSTEM] PROCESSING REPORT FAILURE")

    except Exception as exc:
        logger.exception(f"[ERROR] UNHANDLED EXCEPTION : {exc}")

    finally:
        stop_counter()
        execution_time = get_duration_result()
        logger.info(f"[TIMER] TOTAL : {execution_time}")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
        run_screen_keeper()


if __name__ == "__main__":
    main()
