import os
import pyautogui
from datetime import datetime

from general_task import *
from outlook_pickup import send_outlook_email
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger
from services.remover_pickup import clear_submission_folder
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

CONFIG = load_config()
pyautogui.FAILSAFE = False


def excel_config():
    logger.info("[SYSTEM] STARTING EXCEL WORKFLOW FOR SUMMARY PICKUP REPORT")

    os.startfile(CONFIG["WORKSOURCE_PICKUP"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    handle_office()
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_MINUTE"])

    switch_to_last_sheet()
    switch_to_first_cells()

    convert_to_range()
    capture_table_as_table()
    paste_value_as_value()

    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    save_as_in()
    pyautogui.write(CONFIG["SUBMISSION_PICKUP"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    # TIMESTAMP ENSURES UNIQUE FILE NAME FOR EACH RUN
    save_as_name()
    pickup_stamp = datetime.now().strftime("%d-%m ( %H.%M )")
    pickup_filename = f"REPORT SUMMARY PICKUP {pickup_stamp}"
    pyautogui.write(pickup_filename, interval=0.05)
    confirm()

    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    close_no_save()

    logger.info("[SYSTEM] EXCEL WORKFLOW COMPLETED SUCCESSFULLY")


def send_email():
    outlook_recipients = "herberth.simbolon@sfi.co.id"
    secondary_recipients = ["asset.mgmt@sfi.co.id"]
    current_time = datetime.now()
    subject_email = f"SUMMARY UPDATE (DAILY REPPO/PICKUP) - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    core_email = f"""Yth. Bapak Chief Of Operating Officer,
    
Dengan hormat,
Berikut terlampir Summary Update Daily Reppo pada : {current_time.strftime('%d-%m-%Y')} Pukul {current_time.strftime('%H:%M')} WIB.

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
    logger.info("[DATA] EMAIL SENT SUCCESSFULLY")


if __name__ == "__main__":
    logger.info("[SYSTEM] INITIALISING AUTOMATION PROCESS FOR SUMMARY PICKUP REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUBMISSION_PICKUP"])
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
