import pyautogui
import pyperclip
import pywhatkit as kit
import webbrowser
from services.chrome_checker import open_chrome
from services.config import load_config, logger, wait_timer
from general_task import action_paste, confirm

CONFIG = load_config()
_template_cache = None
_template_scales = [0.8, 0.9, 1.0, 1.1, 1.2]

WHATSAPP_INPUT_X = 845
WHATSAPP_INPUT_Y = 820


def click_whatsapp() -> None:
    logger.info(
        f"[SYSTEM] CLICKING WHATSAPP INPUT AT X: {WHATSAPP_INPUT_X}, Y: {WHATSAPP_INPUT_Y}"
    )
    pyautogui.click(WHATSAPP_INPUT_X, WHATSAPP_INPUT_Y)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def formatting_phone_number(phone_no: str) -> str | None:
    if not phone_no or phone_no == "0":
        return None
    phone_no = phone_no.strip()
    if len(phone_no) < 5:
        return None
    if phone_no.startswith("0"):
        return "+62" + phone_no[1:]
    if not phone_no.startswith("+"):
        return "+" + phone_no
    return phone_no


def validating_group_link(group_link: str) -> str | None:
    if not group_link:
        return None
    group_link = group_link.strip()
    valid_prefixes = (
        "https://chat.whatsapp.com/",
        "https://web.whatsapp.com/accept?code=",
        "https://wa.me/",
    )
    if not any(group_link.startswith(p) for p in valid_prefixes):
        logger.error(f"[WHATSAPP] INVALID GROUP LINK FORMAT: {group_link}")
        return None
    return group_link


def clear_input() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def closing_web_tab() -> None:
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "w")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def send_to_group(group_link: str, message: str = "") -> bool:
    try:
        open_chrome()
        validated = validating_group_link(group_link)
        if not validated:
            raise ValueError("Invalid WhatsApp group link")

        webbrowser.open(validated)
        wait_timer(CONFIG["WAIT_TIME"]["TWENTYFIVE_SECOND"])

        click_whatsapp()
        clear_input()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        action_paste()
        confirm()
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
        closing_web_tab()
        logger.info("[WHATSAPP] MESSAGE SENT TO GROUP")
        return True

    except Exception as e:
        logger.error(f"[WHATSAPP] GROUP SEND FAILED: {e}")
        raise


def send_whatsapp_report(phone_no: str, message: str) -> bool:
    try:
        open_chrome()
        normalised = formatting_phone_number(phone_no)
        logger.info(f"[WHATSAPP] INITIATING MESSAGE TO {normalised}")

        kit.sendwhatmsg_instantly(
            phone_no=normalised,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        click_whatsapp()
        clear_input()

        if message:
            pyautogui.typewrite(message)
            wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])

        confirm()
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
        closing_web_tab()
        logger.info(f"[WHATSAPP] MESSAGE SENT TO {normalised}")
        return True

    except Exception as e:
        logger.error(f"[WHATSAPP] SEND FAILED TO {phone_no}: {e}")
        raise


def send_paste_report(phone_no: str, message: str):
    try:
        open_chrome()
        phone_no = formatting_phone_number(phone_no)
        logger.info(f"[SYSTEM] INITIATING PASTE MESSAGE TO {phone_no}")

        if message:
            pyperclip.copy(message)

        kit.sendwhatmsg_instantly(
            phone_no=phone_no,
            message="",
            wait_time=CONFIG["WAIT_TIME"]["TWENTY_SECOND"],
            tab_close=False,
        )

        click_whatsapp()
        clear_input()
        action_paste()
        confirm()
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
        closing_web_tab()
        return True

    except Exception as e:
        logger.error(f"[WHATSAPP] PASTE SEND FAILED TO {phone_no}: {e}")
        raise
