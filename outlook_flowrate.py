import pyautogui
from general_task import *
from services.config import load_config, wait_timer, logger
from services.capslock_checker import capslock_checking
from services.chrome_checker import open_outlook

CONFIG = load_config()


def send_outlook_email(
    outlook_recipients,
    secondary_recipients,
    subject_email,
    core_email,
    footer_template,
):
    logger.info("[SYSTEM] START FLOWRATE REPORT MAIL")

    try:
        if not open_outlook():
            raise RuntimeError("FAILED TO ACTIVATE OR LAUNCH OUTLOOK")
        wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
        maximize_app_window()
        capslock_checking()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        creating_new_task()

        if isinstance(outlook_recipients, str):
            recipient_list = [outlook_recipients]
        elif isinstance(outlook_recipients, list):
            recipient_list = outlook_recipients
        else:
            raise TypeError("OUTLOOK_RECIPIENTS MUST BE STRING OR LIST")
        
        for idx, recipient in enumerate(recipient_list):
            pyautogui.write(recipient)
            confirm()
            if idx < len(recipient_list) - 1:
                wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        
        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        
        if secondary_recipients:
            if isinstance(secondary_recipients, str):
                cc_list = [secondary_recipients]
            elif isinstance(secondary_recipients, list):
                cc_list = secondary_recipients
            else:
                cc_list = []
            
            for cc in cc_list:
                pyautogui.write(cc)
                confirm()
                wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        pyautogui.write(subject_email)

        pyautogui.press("tab")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        choose_file_attach()
        pyautogui.write(CONFIG["SUBMISSION_FLOWRATE"])
        confirm_file_attach()

        pyautogui.write(core_email)
        blank_mail_space()
        input_clipboard_picture()
        pyautogui.write(footer_template)

        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        finish_outlook()
        logger.info("[SYSTEM] FLOWRATE REPORT MAIL COMPLETED")

    except Exception as e:
        logger.error(f"[ERROR] FLOWRATE REPORT MAIL FAILED : {e}")
        raise
