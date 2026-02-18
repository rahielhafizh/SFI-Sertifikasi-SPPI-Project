import logging
import sys
import time
from typing import Dict, Any, List, Optional
from colorlog import ColoredFormatter

import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


def setup_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
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

        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

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


APPLICATION_PATHS = {
    "CHROME_PATH": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "OUTLOOK_PATH": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office 2013\\Outlook 2013.lnk",
}


CONTACT_INFO = {
    "ASSET_GROUP": "https://web.whatsapp.com/accept?code=KblwmcubP6g04LzqwooTYV",
    "ADMIN_PRIMARY": "+6281382427588",
    "PERSONAL_COO": "+6282311919875",
    "PERSONAL_ONE": "+6285893093275",
    "PERSONAL_TWO": "+6281299606260",
    "PERSONAL_THREE": "+6285781690029",
    "PERSONAL_FOUR": "+6281282426399",
    "PERSONAL_FIVE": "+628988171583",
}


WAIT_TIMES = {
    "HUNDRED_MICROSECOND": 0.0001,
    "TWO_HUNDRED_MICROSECOND": 0.0002,
    "FIVE_HUNDRED_MICROSECOND": 0.0005,
    "ONE_MILLISECOND": 0.001,
    "TWO_MILLISECOND": 0.002,
    "FIVE_MILLISECOND": 0.005,
    "TEN_MILLISECOND": 0.01,
    "TWENTY_MILLISECOND": 0.02,
    "FIFTY_MILLISECOND": 0.05,
    "TWO_HUNDRED_MILLISECOND": 0.2,
    "TENTH_SECOND": 0.1,
    "EIGHTH_SECOND": 0.125,
    "QUARTER_SECOND": 0.25,
    "THIRD_SECOND": 0.33,
    "HALF_SECOND": 0.5,
    "THREE_QUARTER_SECOND": 0.75,
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
    "NORMAL": 1,
    "EXTENDED": 2,
    "LONG": 5,
    "VERY_LONG": 10,
    "ULTRA_LONG": 30,
}

PYAUTOGUI_SETTINGS = {
    "FAILSAFE": False,
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

AREA_BRANCH_MAPPING: Dict[str, List[str]] = {
    "IBT": [
        "DENPASAR",
        "MATARAM",
        "KUPANG",
    ],
    "JABODETABEKSER": [
        "KEDOYA",
        "SUNTER",
        "BEKASI",
        "TANGERANG",
        "BOGOR",
        "SERANG",
        "DEWI SARTIKA",
        "DEPOK",
    ],
    "JAWA BARAT": [
        "BANDUNG",
        "KARAWANG",
        "CIREBON",
    ],
    "JAWA TENGAH": [
        "YOGYAKARTA",
        "SEMARANG",
        "KUDUS",
        "PURWOKERTO",
        "TEGAL",
        "SOLO",
    ],
    "JAWA TIMUR": [
        "SURABAYA",
        "MALANG",
        "GRESIK",
        "KEDIRI",
    ],
    "KALIMANTAN": [
        "SAMARINDA",
        "BANJARMASIN",
        "BALIKPAPAN",
        "PALANGKARAYA",
        "BARABAI",
        "SAMPIT",
        "PONTIANAK",
    ],
    "SULAWESI": [
        "MAKASSAR",
        "MANADO",
        "GORONTALO",
        "PALU",
        "KENDARI",
        "TERNATE",
    ],
    "SUMBAGSEL": [
        "PALEMBANG",
        "LAMPUNG",
        "PANGKAL PINANG",
        "JAMBI",
    ],
    "SUMBAGUTENG": [
        "PEKANBARU",
        "MEDAN",
        "BATAM",
        "PADANG",
    ],
}

BRANCH_ORDER = [
    "BALIKPAPAN",
    "BANDAR LAMPUNG",
    "BANDUNG",
    "BANJARMASIN",
    "BATAM",
    "BEKASI",
    "BOGOR",
    "CIREBON",
    "DENPASAR",
    "DEPOK",
    "DEWI SARTIKA",
    "GORONTALO",
    "GRESIK",
    "JAMBI",
    "KARAWANG",
    "KEDIRI",
    "KEDOYA",
    "KENDARI",
    "KUDUS",
    "KUPANG",
    "MAKASSAR",
    "MALANG",
    "MANADO",
    "MATARAM",
    "MEDAN",
    "PALANGKARAYA",
    "PALEMBANG",
    "PALU",
    "PANGKAL PINANG",
    "PEKANBARU",
    "PONTIANAK",
    "PURWOKERTO",
    "SAMARINDA",
    "SAMPIT",
    "SEMARANG",
    "SERANG",
    "SOLO",
    "SUNTER",+
    "SURABAYA",
    "TANGERANG",
    "TEGAL",
    "TERNATE",
    "YOGYAKARTA",
]

# process_certification_reminders(filter_preset="SIX_MONTHS")
CERTIFICATION_FILTER_PRESETS = {
    "NEXT_MONTH": {"MODE": "NEXT_MONTH"},
    "TWO_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 2},
    "THREE_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 3},
    "FOUR_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 4},
    "FIVE_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 5},
    "SIX_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 6},
    "SEVEN_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 7},
    "EIGHT_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 8},
    "NINE_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 9},
    "TEN_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 10},
    "ELEVEN_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 11},
    "ONE_YEAR": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 12},
    "THIRTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 30},
    "SIXTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 60},
    "NINETY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 90},
    "ONE_HUNDRED_TWENTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 120},
    "ONE_HUNDRED_EIGHTY_DAYS": {"MODE": "DAYS_RANGE", "DAYS_AHEAD": 180},
    "CUSTOM_DATE_RANGE": {
        "MODE": "SPECIFIC_DATE_RANGE",
        "START_DATE": None,
        "END_DATE": None,
    },
}

CERTIFICATION_FILTER_CONFIG = {
    "ACTIVE_PRESET": "NEXT_MONTH",
    "CUSTOM_CONFIG": None,
}

DEFAULT_CONFIG = {
    **APPLICATION_PATHS,
    **CONTACT_INFO,
    "WAIT_TIME": WAIT_TIMES,
    "PYAUTOGUI": PYAUTOGUI_SETTINGS,
    "MONTHS_ID": MONTHS_ID,
    "AREA_BRANCH_MAPPING": AREA_BRANCH_MAPPING,
    "BRANCH_ORDER": BRANCH_ORDER,
    "CERTIFICATION_FILTER_PRESETS": CERTIFICATION_FILTER_PRESETS,
    "CERTIFICATION_FILTER_CONFIG": CERTIFICATION_FILTER_CONFIG,
}


def load_config() -> Dict[str, Any]:
    return DEFAULT_CONFIG


def wait_timer(base_time: float) -> None:
    if base_time < 0:
        logger.warning(f"[TIMER] INVALID NEGATIVE VALUE : {base_time}")
        return
    time.sleep(base_time)


def adaptive_wait(operation_type: str = "NORMAL") -> None:
    wait_mapping = {
        "FAST": WAIT_TIMES["HALF_SECOND"],
        "NORMAL": WAIT_TIMES["ONE_SECOND"],
        "SLOW": WAIT_TIMES["TWO_SECOND"],
        "VERY_SLOW": WAIT_TIMES["FIVE_SECOND"],
    }

    wait_time = wait_mapping.get(operation_type, WAIT_TIMES["ONE_SECOND"])
    wait_timer(wait_time)


def get_config_value(key: str, default: Any = None) -> Any:
    config = DEFAULT_CONFIG
    keys = key.split(".")
    try:
        for k in keys:
            config = config[k]
        return config

    except (KeyError, TypeError):
        logger.warning(f"[CONFIG] KEY NOT FOUND : {key}")
        return default


def get_wait_time(time_key: str, default: float = 1.0) -> float:
    return WAIT_TIMES.get(time_key, default)


def get_pyautogui_setting(setting_name: str, default: Any = None) -> Any:
    return PYAUTOGUI_SETTINGS.get(setting_name, default)


def get_month_id(english_month: str, case: str = "as-is") -> str:
    indonesian_month = MONTHS_ID.get(english_month, english_month)

    if case == "upper":
        return indonesian_month.upper()
    elif case == "lower":
        return indonesian_month.lower()
    elif case == "title":
        return indonesian_month.title()
    else:
        return indonesian_month


def area_branch_mapping() -> Dict[str, List[str]]:
    return AREA_BRANCH_MAPPING.copy()


def get_branch_order() -> List[str]:
    return BRANCH_ORDER.copy()


def get_certification_filter_config(preset: Optional[str] = None) -> Dict[str, Any]:
    if preset is None:
        preset = CERTIFICATION_FILTER_CONFIG["ACTIVE_PRESET"]

    if CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] is not None:
        logger.info("[CONFIG] USING CUSTOM CERTIFICATION FILTER CONFIGURATION")
        return CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"]

    if preset in CERTIFICATION_FILTER_PRESETS:
        logger.info(f"[CONFIG] USING CERTIFICATION FILTER PRESET : {preset}")
        return CERTIFICATION_FILTER_PRESETS[preset].copy()
    else:
        logger.warning(
            f"[CONFIG] UNKNOWN PRESET '{preset}', DEFAULTING TO 'NEXT_MONTH'"
        )
        return CERTIFICATION_FILTER_PRESETS["NEXT_MONTH"].copy()


def set_certification_filter_preset(preset: str) -> bool:
    if preset in CERTIFICATION_FILTER_PRESETS:
        CERTIFICATION_FILTER_CONFIG["ACTIVE_PRESET"] = preset
        CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] = None
        logger.info(f"[CONFIG] CERTIFICATION FILTER PRESET SET TO : {preset}")
        return True
    else:
        logger.error(f"[CONFIG] INVALID PRESET NAME : {preset}")
        return False


def set_custom_certification_filter(custom_config: Dict[str, Any]) -> bool:
    required_mode = custom_config.get("MODE")
    if required_mode not in [
        "NEXT_MONTH",
        "NEXT_N_MONTHS",
        "DAYS_RANGE",
        "SPECIFIC_DATE_RANGE",
    ]:
        logger.error(f"[CONFIG] INVALID MODE IN CUSTOM FILTER : {required_mode}")
        return False

    CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] = custom_config
    logger.info("[CONFIG] CUSTOM CERTIFICATION FILTER CONFIGURATION APPLIED")
    return True


def list_certification_filter_presets() -> List[str]:
    return list(CERTIFICATION_FILTER_PRESETS.keys())
