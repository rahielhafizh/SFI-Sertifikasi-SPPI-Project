import os
import pyautogui
from datetime import datetime
from general_task import *
from pynput.keyboard import Controller
from services.remover_denda_aktif import clear_submission_folder
from services.config import load_config, wait_timer, logger, get_month_id
from outlook_denda_aktif import send_outlook_email
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
    logger.info("[SYSTEM] ACTIVE FINE REPORT EXCEL WORKFLOW")
    os.startfile(CONFIG["WORKSOURCE_DENDA"])
    wait_timer(CONFIG["WAIT_TIME"]["TWENTYFIVE_SECOND"])
    maximize_app_window()

    switch_to_right_sheet()
    switch_to_first_sheet()

    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["TWOHALF_MINUTE"])
    entering_operation()

    switch_to_first_cells()
    switch_to_right_sheet()

    switch_to_first_cells()
    select_sheet_down()
    move_or_copy_menu()
    move_or_copy_as_newbook()
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

    switch_to_first_sheet()
    break_excel_link()
    switch_to_first_cells()
    switch_to_table_cells()
    capture_table_as_picture()
    switch_to_first_cells()

    save_new_book()
    pyautogui.write(CONFIG["SUBMISSION_DENDA"])
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

    set_new_book_name()
    today = datetime.now()
    fine_day = today.strftime("%d")
    fine_year = today.strftime("%Y")
    month_eng = today.strftime("%B")
    month_idn_title = get_month_id(month_eng, case="title")

    fine_filename = f"Summary Report Performance Denda Aktif {fine_day} {month_idn_title} ({today.strftime('%H.%M')})"

    pyautogui.write(fine_filename, interval=0.05)
    confirm()
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    switch_to_first_sheet()
    switch_to_first_cells()
    switch_to_right_sheet()
    switch_to_first_cells()

    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def send_email():
    outlook_recipients = ["asset.mgmt@sfi.co.id"]
    secondary_recipients = "collho.3@sfi.co.id"

    today = datetime.now()
    month_eng = today.strftime("%B")
    fine_year = today.strftime("%Y")
    month_idn_title = get_month_id(month_eng, case="title")
    subject_email = f"Summary Update Denda Aktif | {datetime.now().strftime('%d')} {month_idn_title} ({today.strftime('%H:%M')})"

    core_email = f"""Dear All,

Dengan hormat,

Berikut terlampir Summary Report Performance Denda Aktif As Of {month_idn_title} {fine_year} Pukul {today.strftime('%H:%M')} WIB.

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


if __name__ == "__main__":
    logger.info("[SYSTEM] START ACTIVE FINE REPORT")
    start_counter()

    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    find_screen_keeper_process()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    stop_screen_keeper()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    clear_submission_folder(target_folder=CONFIG["SUBMISSION_DENDA"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    excel_config()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    send_email()
    logger.info("[SYSTEM] ACTIVE FINE REPORT SENT")

    stop_counter()
    execution_time = get_duration_result()
    logger.info(f"[SYSTEM] TOTAL EXECUTION TIME: {execution_time}")

    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.warning("[SYSTEM] RESTARTING SCREEN KEEPER")
    run_screen_keeper()
