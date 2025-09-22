import logging
import sys
import time
import random
from typing import Dict, Any, Optional, Tuple
from colorlog import ColoredFormatter
import pyautogui

_pyautogui_configured = False


# LOGGING CONFIGURATION MODULE
def setup_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    # PREVENT DUPLICATE HANDLER CREATION
    if not logger.handlers:
        formatter = ColoredFormatter(
            fmt=(
                "\n"
                "%(log_color)s[%(asctime)s] \n"
                "• CONDITION  : %(levelname)s\n"
                "• SOURCE     : %(filename)s:%(lineno)d\n"
                "• FUNCTION   : %(funcName)s()\n"
                "• MESSAGE    : %(message)s\n"
                "\n"
                "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬"
            ),
            datefmt=" 📆 %d-%m-%Y 🕒 %H:%M:%S ",
            log_colors={
                "DEBUG": "blue",
                "INFO": "green",
                "WARNING": "bold_yellow",
                "ERROR": "thin_red",
                "CRITICAL": "bold_red",
            },
        )

        # CREATE AND CONFIGURE STREAM HANDLER
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # SUPPRESS HTTPS CONNECTION DEBUG MESSAGES FROM UNDERLYING LIBRARIES
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("urllib3.util.retry").setLevel(logging.WARNING)
    logging.getLogger("requests.packages.urllib3.connectionpool").setLevel(
        logging.WARNING
    )
    logging.getLogger("requests.packages.urllib3.util.retry").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    return logger


logger = setup_logger()


# APPLICATION RAW PATH
APPLICATION_PATHS = {
    "CHROME_PATH": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "OUTLOOK_PATH": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\Outlook 2013.lnk",
}

# AUTOMATION RAW PATH
FOLDER_PATHS = {
    # SUBMISSION
    "SUBMISSION_FLOWRATE": rf"D:\Rahiel Hafizh\REPORT_FLOWRATE\SUBMISSION",
    "SUBMISSION_STOPSELL": rf"D:\Rahiel Hafizh\REPORT_STOPSELL\SUBMISSION",
    "SUBMISSION_PICKUP": rf"D:\Rahiel Hafizh\REPORT_SUMMARY_PICKUP\SUBMISSION",
    "SUBMISSION_LOR": rf"D:\Rahiel Hafizh\REPORT_LOR_EMAIL\SUBMISSION",
    "SUBMISSION_PIC": rf"D:\Rahiel Hafizh\REPORT_SUMMARY_AREA\SUBMISSION",
    "CEK-REPORT-FR": rf"D:\Rahiel Hafizh\REPORT_FLOWRATE\SUBMISSION\CEK-REPORT.xlsx",
    # SOURCE
    "WORKSOURCE_FLOWRATE": rf"D:\Rahiel Hafizh\REPORT_FLOWRATE\UPDATE-FR-SOURCE.xlsx",
    "WORKSOURCE_STOPSELL": rf"D:\Rahiel Hafizh\REPORT_FLOWRATE\STOP-SELL-SOURCE.xlsx",
    "WORKSOURCE_ORDER_IN": rf"D:\Rahiel Hafizh\MARKETING\ORDER-IN\CEK-REPORT.xlsx",
    "WORKSOURCE_PICKUP": rf"D:\Rahiel Hafizh\REPORT_SUMMARY_PICKUP\UPDATE-PICKUP-SOURCE.xlsx",
    "WORKSOURCE_LOR": rf"D:\Rahiel Hafizh\REPORT_LOR_EMAIL\REPORT_LOR_SOURCE.xlsx",
    "WORKSOURCE_PIC": rf"D:\Rahiel Hafizh\REPORT_SUMMARY_AREA\SUBMISSION\REPORT-PENUGASAN-PIC.xlsx",
}

CONTACT_INFO = {
    "ASSET_GROUP": "https://web.whatsapp.com/accept?code=KblwmcubP6g04LzqwooTYV",  # LINK GROUP
    "ADMIN_PRIMARY": "+6281382427588",  # WA ACCOUNT
    "PERSONAL_ONE": "+6285893093275",  # EL
    "PERSONAL_TWO": "+6281299606260",  # PAK UGI
    "PERSONAL_THREE": "+6285781690029",  # PAK RIO
    "PERSONAL_FOUR": "+6281282426399",  # PAK WAWAN
    "PERSONAL_FIVE": "+628988171583",  # PAK PANJI
}


# TIMING CONFIGURATION CONSTANTS
WAIT_TIMES = {
    # MICROSECOND PRECISION TIMERS
    "HUNDRED_MICROSECOND": 0.0001,
    "TWO_HUNDRED_MICROSECOND": 0.0002,
    "FIVE_HUNDRED_MICROSECOND": 0.0005,
    # MILLISECOND PRECISION TIMERS
    "ONE_MILLISECOND": 0.001,
    "TWO_MILLISECOND": 0.002,
    "FIVE_MILLISECOND": 0.005,
    "TEN_MILLISECOND": 0.01,
    "TWENTY_MILLISECOND": 0.02,
    "FIFTY_MILLISECOND": 0.05,
    "HUNDRED_MILLISECOND": 0.1,
    "TWO_HUNDRED_MILLISECOND": 0.2,
    # SUB-SECOND PRECISION TIMERS
    "TENTH_SECOND": 0.1,
    "EIGHTH_SECOND": 0.125,
    "QUARTER_SECOND": 0.25,
    "THIRD_SECOND": 0.33,
    "HALF_SECOND": 0.5,
    "THREE_QUARTER_SECOND": 0.75,
    # STANDARD SECOND-BASED TIMERS
    "ONE_SECOND": 1,
    "ONEHALF_SECOND": 1.5,
    "TWO_SECOND": 2,
    "TWOHALF_SECOND": 2.5,
    "THREE_SECOND": 3,
    "FOUR_SECOND": 4,
    "FIVE_SECOND": 5,
    "SIX_SECOND": 6,
    "SEVEN_SECOND": 7,
    "EIGHT_SECOND": 8,
    "NINE_SECOND": 9,
    "TEN_SECOND": 10,
    "TWELVE_SECOND": 12,
    "FIFTEEN_SECOND": 15,
    "EIGHTEEN_SECOND": 18,
    "TWENTY_SECOND": 20,
    "TWENTYFIVE_SECOND": 25,
    "THIRTY_SECOND": 30,
    "THIRTYFIVE_SECOND": 35,
    "FORTY_SECOND": 40,
    "FORTYFIVE_SECOND": 45,
    "FIFTY_SECOND": 50,
    "FIFTYFIVE_SECOND": 55,
    # MINUTE-BASED TIMERS
    "ONE_MINUTE": 60,
    "ONEHALF_MINUTE": 90,
    "TWO_MINUTE": 120,
    "TWOHALF_MINUTE": 150,
    "THREE_MINUTE": 180,
    "FOUR_MINUTE": 240,
    "FIVE_MINUTE": 300,
    "SIX_MINUTE": 360,
    "SEVEN_MINUTE": 420,
    "EIGHT_MINUTE": 480,
    "NINE_MINUTE": 540,
    "TEN_MINUTE": 600,
    "TWELVE_MINUTE": 720,
    "FIFTEEN_MINUTE": 900,
    "TWENTY_MINUTE": 1200,
    "TWENTYFIVE_MINUTE": 1500,
    "THIRTY_MINUTE": 1800,
    "THIRTYFIVE_MINUTE": 2100,
    "FORTY_MINUTE": 2400,
    "FORTYFIVE_MINUTE": 2700,
    "FIFTY_MINUTE": 3000,
    "FIFTYFIVE_MINUTE": 3300,
    "SIXTY_MINUTE": 3600,
    # EXTENDED DURATION TIMERS
    "NORMAL": 1,
    "EXTENDED": 2,
    "LONG": 5,
    "VERY_LONG": 10,
    "ULTRA_LONG": 30,
}

# PYAUTOGUI AUTOMATION SETTINGS
PYAUTOGUI_SETTINGS = {
    "FAILSAFE": True,
    "TRUE_CONDITION": True,
    "FALSE_CONDITION": False,
    "PAUSE": 0.1,
    "DURATION": 0.1,
    "INTERVAL": 0.05,
    "LOG_SCREENSHOTS": False,
    "SCREENSHOT_FOLDER": "screenshots",
    "MINIMUM_DURATION": 0.1,
    "MINIMUM_SLEEP": 0.05,
    "MAXIMUM_SLEEP": 2.0,
    "DEFAULT_PAUSE": 0.1,
    "DEFAULT_DURATION": 0.1,
    "DEFAULT_INTERVAL": 0.05,
}


# JITTER BEHAVIOR CONFIGURATION
JITTER_SETTINGS = {
    "STANDARD": {
        "MIN": 0.1,
        "MAX": 0.3,
        "FACTOR": 0.2,
    },
    "AGGRESSIVE": {
        "MIN": 0.2,
        "MAX": 0.5,
        "FACTOR": 0.35,
    },
    "CONSERVATIVE": {
        "MIN": 0.05,
        "MAX": 0.15,
        "FACTOR": 0.1,
    },
    "NONE": {
        "MIN": 0.0,
        "MAX": 0.0,
        "FACTOR": 0.0,
    },
}

# LOCALIZATION MAPPING
MONTHS_ID = {
    "January": "Januari",
    "February": "Februari",
    "March": "Maret",
    "April": "April",
    "May": "Mei",
    "June": "Juni",
    "July": "Juli",
    "August": "Agustus",
    "September": "September",
    "October": "Oktober",
    "November": "November",
    "December": "Desember",
}

# MASTER DEFAULT CONFIGURATION
DEFAULT_CONFIG = {
    **APPLICATION_PATHS,
    **FOLDER_PATHS,
    **CONTACT_INFO,
    "WAIT_TIME": WAIT_TIMES,
    "PYAUTOGUI": PYAUTOGUI_SETTINGS,
    "JITTER": JITTER_SETTINGS,
    "MONTHS_ID": MONTHS_ID,
}


# CONFIGURATION MANAGEMENT FUNCTIONS
def setup_pyautogui_config() -> None:
    # PREVENT DUPLICATE CONFIGURATION
    global _pyautogui_configured
    if _pyautogui_configured:
        return

    # APPLY FAILSAFE AND PAUSE SETTINGS
    try:
        pyautogui.FAILSAFE = PYAUTOGUI_SETTINGS["FAILSAFE"]
        pyautogui.PAUSE = PYAUTOGUI_SETTINGS["PAUSE"]
        _pyautogui_configured = True

    # LOG CONFIGURATION ERROR AND RE-RAISE
    except Exception as e:
        logger.error(f"FAILED TO CONFIGURE PYAUTOGUI: {e}")
        raise


# LOAD CONFIGURATION AND AUTOMATICALLY SETUP PYAUTOGUI
def load_config() -> Dict[str, Any]:
    setup_pyautogui_config()
    return DEFAULT_CONFIG


# TIMING AND DELAY FUNCTIONS
def wait_timer(base_time: float) -> None:
    time.sleep(base_time)


# WAIT TIMER WITH RANDOM JITTER FOR HUMAN-LIKE BEHAVIOR
def wait_with_jitter(base_time: float, jitter_type: str = "STANDARD") -> None:
    jitter_config = JITTER_SETTINGS.get(jitter_type, JITTER_SETTINGS["STANDARD"])

    # CALCULATE JITTER IF FACTOR IS GREATER THAN ZERO
    if jitter_config["FACTOR"] > 0:
        jitter = random.uniform(jitter_config["MIN"], jitter_config["MAX"])
        total_time = base_time + (base_time * jitter)
    else:
        total_time = base_time

    wait_timer(total_time)


# ADAPTIVE WAIT BASED ON OPERATION TYPE
def adaptive_wait(operation_type: str = "NORMAL") -> None:
    wait_mapping = {
        "FAST": WAIT_TIMES["HALF_SECOND"],
        "NORMAL": WAIT_TIMES["ONE_SECOND"],
        "SLOW": WAIT_TIMES["TWO_SECOND"],
        "VERY_SLOW": WAIT_TIMES["FIVE_SECOND"],
    }

    # GET WAIT TIME FROM MAPPING OR DEFAULT
    wait_time = wait_mapping.get(operation_type, WAIT_TIMES["ONE_SECOND"])
    wait_timer(wait_time)


# CONFIGURATION UTILITY FUNCTIONS
def get_config_value(key: str, default: Any = None) -> Any:
    config = DEFAULT_CONFIG
    keys = key.split(".")

    # TRAVERSE NESTED CONFIGURATION KEYS
    try:
        for k in keys:
            config = config[k]
        return config
    # RETURN DEFAULT VALUE ON KEY ERROR
    except (KeyError, TypeError):
        return default


# GET WAIT TIME VALUE WITH FALLBACK
def get_wait_time(time_key: str, default: float = 1.0) -> float:
    return WAIT_TIMES.get(time_key, default)


# GET PYAUTOGUI SETTING VALUE
def get_pyautogui_setting(setting_name: str, default: Any = None) -> Any:
    return PYAUTOGUI_SETTINGS.get(setting_name, default)


# GET JITTER SETTING VALUE
def get_jitter_setting(jitter_type: str, default: float = 0.5) -> float:
    jitter_config = JITTER_SETTINGS.get(jitter_type, JITTER_SETTINGS["STANDARD"])
    return jitter_config.get("FACTOR", default)


# CONVERT ENGLISH MONTH NAME TO INDONESIAN WITH CASE CONTROL
def get_month_id(english_month: str, case: str = "as-is") -> str:
    indonesian_month = MONTHS_ID.get(english_month, english_month)

    # APPLY CASE TRANSFORMATION
    if case == "upper":
        return indonesian_month.upper()
    elif case == "lower":
        return indonesian_month.lower()
    elif case == "title":
        return indonesian_month.title()
    else:
        return indonesian_month
