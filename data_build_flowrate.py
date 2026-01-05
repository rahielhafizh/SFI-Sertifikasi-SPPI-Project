import os
from datetime import datetime, timedelta
from services.config import load_config, wait_timer, logger
from general_task import *

CONFIG = load_config()


def excel_config():
    os.startfile(CONFIG["WORKSOURCE_FLOWRATE"])
    wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])
    maximize_app_window()
    switch_to_first_sheet()
    switch_to_first_cells()
    refresh_excel_data()
    wait_timer(CONFIG["WAIT_TIME"]["FOUR_MINUTE"])
    switch_to_right_sheet()
    switch_to_first_sheet()
    save_file()
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    closing_tab()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
    logger.info("BUILD FLOWRATE REPORT COMPLETED")
