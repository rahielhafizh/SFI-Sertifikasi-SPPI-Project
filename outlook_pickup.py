import os
import pyautogui
import win32gui
import win32con
from general_task import *
from services.config import load_config, wait_timer, logger
from services.chrome_checker import open_outlook

CONFIG = load_config()


def send_outlook_email(
    outlook_recipients,
    secondary_recipients,
    subject_email,
    core_email,
    footer_template,
):
    logger.info("[SYSTEM] INITIATING AUTOMATED OUTLOOK (SUMMARY PICKUP)")

    try:
        if not open_outlook():
            raise RuntimeError("FAILED TO ACTIVATE OR LAUNCH OUTLOOK")
        handle_office()
        maximize_app_window()
        creating_new_task()

        pyautogui.write(outlook_recipients)
        confirm()

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        for cc in secondary_recipients:
            pyautogui.write(cc)
            confirm()

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.write(subject_email)

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        choose_file_attach()
        pyautogui.write(CONFIG["SUBMISSION_PICKUP"])
        confirm_file_attach()

        pyautogui.write(core_email)
        blank_mail_space()
        input_clipboard_picture()
        pyautogui.write(footer_template)

        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        finish_outlook()
        logger.info("[SYSTEM] OUTLOOK PROTOCOL EXECUTED SUCCESSFULLY")

    except Exception as e:
        logger.error(f"[ERROR] OUTLOOK DELIVERY FAILURE: {e}")
        raise
