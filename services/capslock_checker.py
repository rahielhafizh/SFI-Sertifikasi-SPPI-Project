import sys
import time
import ctypes
import pyautogui
from services.config import load_config, logger


def is_capslock_on() -> bool:
    if sys.platform.startswith("win"):
        return bool(ctypes.windll.user32.GetKeyState(0x14) & 0x0001)
    logger.warning("[KEYBOARD] CAPSLOCK CANNOT BE READ")
    return False


def capslock_checking(config: dict = None) -> bool:
    cfg = config or load_config()
    retry_delay = cfg.get("WAIT_TIME", {}).get("HALF_SECOND", 0.5)

    if not is_capslock_on():
        logger.info("[KEYBOARD] CAPSLOCK IS ALREADY OFF")
        return True

    logger.warning("[KEYBOARD] ATTEMPTING TO DISABLE CAPSLOCK")
    pyautogui.press("capslock")

    for attempt in range(1, 6):
        time.sleep(retry_delay)
        if not is_capslock_on():
            logger.info(f"[KEYBOARD] CAPSLOCK DISABLED ON ATTEMPT {attempt}")
            return True

    logger.error("[KEYBOARD] FAILED TO DISABLE CAPSLOCK")
    return False
