import pyautogui
from typing import List, Optional, Union

# Dipertahankan karena ini eksternal dependency yang dipanggil di parent source code.
from general_task import (
    maximize_app_window,
    creating_new_task,
    blank_mail_space,
    finish_outlook,
    minimize_outlook,
    confirm,
)
from services.config import load_config, wait_timer, logger
from services.capslock_checker import capslock_checking
from services.chrome_checker import open_outlook
from services.certification_utils import get_email_subject

CONFIG = load_config()

def normalizing_recipients(recipients: Union[str, List[str], None]) -> List[str]:
    if not recipients:
        return []
    if isinstance(recipients, str):
        val = recipients.strip().lower()
        return [val] if val else []
    return [str(r).strip().lower() for r in recipients if r and str(r).strip()]

def write_recipients(recipient_list: List[str]) -> None:
    for idx, recipient in enumerate(recipient_list):
        pyautogui.write(recipient)
        confirm()
        if idx < len(recipient_list) - 1:
            wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])

def _execute_outlook_email_flow(subject: str, body: str, to_list: List[str], cc_list: List[str], minimize: bool) -> bool:
    if not open_outlook():
        logger.error("[ERROR] FAILED TO ACTIVATE OR LAUNCH OUTLOOK")
        return False

    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    maximize_app_window()
    capslock_checking()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    try:
        from general_task import handle_office
        handle_office()
    except Exception:
        pass

    creating_new_task()
    write_recipients(to_list)
    pyautogui.press("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    if cc_list:
        write_recipients(cc_list)
    pyautogui.press("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    pyautogui.write(subject)
    pyautogui.press("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    pyautogui.write(body)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    blank_mail_space()
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    if minimize:
        minimize_outlook()
    else:
        finish_outlook()

    return True

def send_certification_email(
    branch_name: str,
    branch_manager: str,
    bm_mail: str,
    email_body: str,
    minimize_after_send: bool = True,
    cc_recipients: Optional[Union[str, List[str]]] = None,
) -> bool:
    primary_recipients = normalizing_recipients(bm_mail)
    if not primary_recipients:
        logger.error("[ERROR] PRIMARY RECIPIENT EMAIL (BM_MAIL) IS EMPTY")
        return False

    logger.info(f"[SYSTEM] START CERTIFICATION EMAIL (BRANCH='{branch_name}', MANAGER='{branch_manager}', TO='{primary_recipients[0]}')")

    success = _execute_outlook_email_flow(
        subject=get_email_subject(branch_name),
        body=email_body,
        to_list=primary_recipients,
        cc_list=normalizing_recipients(cc_recipients),
        minimize=minimize_after_send
    )

    if success:
        logger.info(f"[SYSTEM] CERTIFICATION EMAIL SENT SUCCESSFULLY FOR BRANCH '{branch_name}'")
    else:
        logger.error(f"[ERROR] CERTIFICATION EMAIL SENDING FAILED FOR BRANCH '{branch_name}'")
    return success

def send_mokas_email(
    target_email: str,
    subject_email: str,
    email_body: str,
    minimize_after_send: bool = True,
) -> bool:
    primary_recipients = normalizing_recipients(target_email)
    if not primary_recipients:
        logger.error("[ERROR] TARGET EMAIL IS EMPTY")
        return False

    logger.info(f"[SYSTEM] START MOKAS EMAIL (TO='{primary_recipients[0]}')")

    success = _execute_outlook_email_flow(
        subject=subject_email,
        body=email_body,
        to_list=primary_recipients,
        cc_list=[],
        minimize=minimize_after_send
    )

    if success:
        logger.info("[SYSTEM] MOKAS EMAIL SENT SUCCESSFULLY")
    else:
        logger.error("[ERROR] MOKAS EMAIL SENDING FAILED")
    return success