import logging
import sys
import time
from typing import Dict, Any, List, Optional
from colorlog import ColoredFormatter
import pyautogui

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


# ─── LOGGER FORMATTER ─────────────────────────────────────────────────────────
class SafeColoredFormatter(ColoredFormatter):
    FALLBACK_DATE_FORMAT = "%d-%m-%Y %H:%M:%S"

    def formatTime(
        self, record: logging.LogRecord, datefmt: Optional[str] = None
    ) -> str:
        try:
            return super().formatTime(record, datefmt)
        except (UnicodeEncodeError, ValueError, OSError):
            ct = self.converter(record.created)
            return time.strftime(self.FALLBACK_DATE_FORMAT, ct)

    def format(self, record: logging.LogRecord) -> str:
        try:
            return super().format(record)
        except UnicodeEncodeError:
            record.msg = record.msg.encode("ascii", errors="replace").decode("ascii")
            record.args = ()
            try:
                return super().format(record)
            except Exception:
                return f"[LOG] {record.levelname}: {record.getMessage()}"


# ─── LOGGER SETUP ─────────────────────────────────────────────────────────────
def setup_logger() -> logging.Logger:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = SafeColoredFormatter(
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

        if hasattr(stream_handler.stream, "reconfigure"):
            try:
                stream_handler.stream.reconfigure(errors="replace")
            except Exception:
                pass
        elif hasattr(stream_handler.stream, "buffer"):
            try:
                import io

                stream_handler.stream = io.TextIOWrapper(
                    stream_handler.stream.buffer,
                    encoding="utf-8",
                    errors="replace",
                    line_buffering=True,
                )
            except Exception:
                pass

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

DEFAULT_CC_SPPI = [
    "agnes.tri@sfi.co.id",
    "ardi.supriyono@sfi.co.id",
    "swacita.apriyanti@sfi.co.id",
    "rio.maulana@sfi.co.id",
    "hermawan.nugroho@sfi.co.id",
    "ugi.lugina@sfi.co.id",
]


DEFAULT_CC_MOKAS = [
    "angelita.roma@sfi.co.id",
    "alfian.tejo@sfi.co.id",
    "aris.sumartono@sfi.co.id",
    "brian.yektibudi@sfi.co.id",
]

APPLICATION_PATHS = {
    "CHROME_PATH": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "OUTLOOK_PATH": "C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\\Microsoft Office\\Outlook 2013.lnk",
}

WAIT_TIMES = {
    "TENTH_SECOND": 0.1,
    "HALF_SECOND": 0.5,
    "ONE_SECOND": 1.0,
    "TWO_SECOND": 2.0,
    "THREE_SECOND": 3.0,
    "FIVE_SECOND": 5.0,
    "TEN_SECOND": 10.0,
    "TWENTY_SECOND": 20.0,
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
    "SUNTER",
    "SURABAYA",
    "TANGERANG",
    "TEGAL",
    "TERNATE",
    "YOGYAKARTA",
]

CERTIFICATION_FILTER_PRESETS = {
    "NEXT_MONTH": {"MODE": "NEXT_MONTH"},
    "SIX_MONTHS": {"MODE": "NEXT_N_MONTHS", "MONTHS_AHEAD": 6},
}

CERTIFICATION_FILTER_CONFIG = {
    "ACTIVE_PRESET": "NEXT_MONTH",
    "CUSTOM_CONFIG": None,
}

DEFAULT_CONFIG = {
    **APPLICATION_PATHS,
    "WAIT_TIME": WAIT_TIMES,
    "MONTHS_ID": MONTHS_ID,
    "BRANCH_ORDER": BRANCH_ORDER,
    "CERTIFICATION_FILTER_PRESETS": CERTIFICATION_FILTER_PRESETS,
    "CERTIFICATION_FILTER_CONFIG": CERTIFICATION_FILTER_CONFIG,
}


def load_config() -> Dict[str, Any]:
    return DEFAULT_CONFIG


def wait_timer(base_time: float) -> None:
    if base_time > 0:
        time.sleep(base_time)
    else:
        logger.warning(f"[TIMER] INVALID NEGATIVE VALUE : {base_time}")


def get_month_id(english_month: str, case: str = "as-is") -> str:
    indonesian_month = MONTHS_ID.get(english_month, english_month)
    if case == "upper":
        return indonesian_month.upper()
    elif case == "lower":
        return indonesian_month.lower()
    elif case == "title":
        return indonesian_month.title()
    return indonesian_month


def get_branch_order() -> List[str]:
    return BRANCH_ORDER.copy()


def get_certification_filter_config(preset: Optional[str] = None) -> Dict[str, Any]:
    active_preset = preset or CERTIFICATION_FILTER_CONFIG["ACTIVE_PRESET"]

    if CERTIFICATION_FILTER_CONFIG.get("CUSTOM_CONFIG"):
        logger.info("[CONFIG] USING CUSTOM CERTIFICATION FILTER CONFIGURATION")
        return CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"]

    if active_preset in CERTIFICATION_FILTER_PRESETS:
        logger.info(f"[CONFIG] USING CERTIFICATION FILTER PRESET : {active_preset}")
        return CERTIFICATION_FILTER_PRESETS[active_preset].copy()

    logger.warning(f"[CONFIG] UNKNOWN PRESET '{active_preset}'")
    return CERTIFICATION_FILTER_PRESETS["NEXT_MONTH"].copy()


def set_certification_filter_preset(preset: str) -> bool:
    if preset in CERTIFICATION_FILTER_PRESETS:
        CERTIFICATION_FILTER_CONFIG["ACTIVE_PRESET"] = preset
        CERTIFICATION_FILTER_CONFIG["CUSTOM_CONFIG"] = None
        logger.info(f"[CONFIG] CERTIFICATION FILTER PRESET SET TO : {preset}")
        return True

    logger.error(f"[CONFIG] INVALID PRESET NAME : {preset}")
    return False
