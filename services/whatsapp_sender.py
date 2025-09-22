import time
import pyautogui
import pywhatkit as kit
import webbrowser
from services.config import load_config, wait_timer, logger
from services.chrome_checker import open_chrome


CONFIG = load_config()
_template_cache = None
_template_scales = [0.8, 0.9, 1.0, 1.1, 1.2]


def number_formatter(phone_no: str) -> str:
    if not phone_no or phone_no == "0":
        return None

    phone_no = phone_no.strip()
    if len(phone_no) < 5:
        return None

    if phone_no.startswith("0"):
        return "+62" + phone_no[1:]

    elif not phone_no.startswith("+"):
        return "+" + phone_no

    return phone_no


def validate_group_link(group_link: str) -> str:
    if not group_link:
        return None

    group_link = group_link.strip()
    valid_prefixes = [
        "https://chat.whatsapp.com/",
        "https://web.whatsapp.com/accept?code=",
        "https://wa.me/",
    ]

    if not any(group_link.startswith(prefix) for prefix in valid_prefixes):
        logger.error(f"[ERROR] INVALID WHATSAPP LINK FORMAT: {group_link}")
        return None

    return group_link


def cleanup_report_preparation():
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def closing_whatsapp_tab():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("ctrl", "w")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


# SEND REPORT TO GROUP
def send_to_group(group_link: str, message: str = ""):
    try:
        open_chrome()
        group_link = validate_group_link(group_link)
        if not group_link:
            raise ValueError("INVALID LINK FORMAT")

        webbrowser.open(group_link)
        wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])

        cleanup_report_preparation()

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])

        closing_whatsapp_tab()
        logger.info("[SYSTEM] MESSAGE SUCCESSFULLY SENT TO GROUP")
        return True

    except Exception as e:
        logger.error(f"[ERROR] GROUP MESSAGE SEND FAILURE: {str(e)}")
        raise


# SEND REPORT WITH PASTE + WRITE
def send_whatsapp_report(phone_no: str, message: str):
    try:
        open_chrome()
        phone_no = number_formatter(phone_no)
        logger.info(f"[SYSTEM] INITIATING MESSAGE TO {phone_no}")

        kit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        cleanup_report_preparation()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info(f"[SYSTEM] MESSAGE SUCCESSFULLY SENT TO {phone_no}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] MESSAGE SEND FAILURE TO {phone_no}: {str(e)}")
        raise


# SEND REPORT WITH WRITE ONLY
def send_summary_report(phone_no: str, message: str):
    try:
        open_chrome()
        phone_no = number_formatter(phone_no)
        logger.info(f"[SYSTEM] INITIATING SUMMARY MESSAGE TO {phone_no}")

        kit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        cleanup_report_preparation()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info(f"[SYSTEM] SUMMARY MESSAGE SUCCESSFULLY SENT TO {phone_no}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] SUMMARY MESSAGE SEND FAILURE TO {phone_no}: {str(e)}")
        raise


# SEND REPORT WITH PASTE ONLY
def send_paste_report(phone_no: str, message: str):
    try:
        open_chrome()
        phone_no = number_formatter(phone_no)
        logger.info(f"[SYSTEM] INITIATING PASTE MESSAGE TO {phone_no}")

        kit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        cleanup_report_preparation()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.hotkey("ctrl", "v")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        pyautogui.press("enter")
        wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])

        closing_whatsapp_tab()
        logger.info(f"[SYSTEM] PASTE MESSAGE SUCCESSFULLY SENT TO {phone_no}")
        return True

    except Exception as e:
        logger.error(f"[ERROR] PASTE MESSAGE SEND FAILURE TO {phone_no}: {str(e)}")
        raise
