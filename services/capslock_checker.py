import sys
import time
import ctypes
import pyautogui
from services.config import load_config, wait_timer, logger


# CLASS TO ABSTRACT KEYBOARD CONTROL OPERATIONS
class KeyboardController:
    VK_CAPITAL = 0x14

    def capslock_status(self) -> bool:
        if sys.platform.startswith("win"):
            return bool(ctypes.windll.user32.GetKeyState(self.VK_CAPITAL) & 0x0001)
        logger.warning("[KEYBOARD] CAPSLOCK CANNOT BE READ")
        return False

    def press_capslock(self):
        pyautogui.press("capslock")


# CLASS TO ENFORCE CAPSLOCK OFF STATE
class CapsLockEnforcer:
    def __init__(self, config: dict, controller: KeyboardController):
        self.config = config
        self.controller = controller
        self.max_retries = 5
        self.retry_delay = self.config.get("WAIT_TIME", {}).get("HALF_SECOND", 0.5)

    # CHECK IF CAPSLOCK IS ALREADY OFF
    def ensure_capslock_off(self) -> bool:
        if not self.controller.capslock_status():
            logger.info("[KEYBOARD] CAPSLOCK IS ALREADY OFF")
            return True

        # ATTEMPT TO TURN CAPSLOCK OFF
        logger.warning("[KEYBOARD] ATTEMPTING TO DISABLE")
        self.controller.press_capslock()

        # VERIFY CAPSLOCK STATE WITH RETRIES
        for attempt in range(1, self.max_retries + 1):
            time.sleep(self.retry_delay)
            if not self.controller.capslock_status():
                logger.info(f"[KEYBOARD] CAPSLOCK DISABLED ON ATTEMPT {attempt}")
                return True

        # FINAL FAILURE STATE
        logger.error("[KEYBOARD] FAILED TO DISABLE CAPSLOCK")
        return False


# PUBLIC FUNCTION ENTRY POINT
def capslock_checking(
    config: dict = None, controller: KeyboardController = None
) -> bool:
    effective_config = config or load_config()
    effective_controller = controller or KeyboardController()
    enforcer = CapsLockEnforcer(
        config=effective_config, controller=effective_controller
    )
    return enforcer.ensure_capslock_off()


if __name__ == "__main__":
    success = capslock_checking()
    sys.exit(0 if success else 1)
