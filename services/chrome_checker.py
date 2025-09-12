import os
import time
import ctypes
import subprocess
import pyautogui
import psutil
import win32gui
import win32con
import win32api
import win32process
from typing import Optional, List
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from ctypes import wintypes
from services.config import load_config, wait_timer, logger

CONFIG = load_config()
SPI_GETFOREGROUNDLOCKTIMEOUT = 0x2000
SPI_SETFOREGROUNDLOCKTIMEOUT = 0x2001
SPIF_SENDWININICHANGE = 0x0002


class WindowState(Enum):
    MINIMIZED = win32con.SW_SHOWMINIMIZED
    MAXIMIZED = win32con.SW_SHOWMAXIMIZED
    RESTORED = win32con.SW_RESTORE
    HIDDEN = win32con.SW_HIDE


# CHECK WHETHER A PROCESS IS RUNNING BY NAME
def running_process_checker(process_name: str) -> bool:
    try:
        for p in psutil.process_iter(attrs=["name"]):
            name = p.info.get("name") or ""
            if process_name.lower() in name.lower():
                return True
        return False
    except Exception as e:
        logger.error(f"[ERROR] ERROR CHECKING {process_name} STATUS: {e}")
        return False


# WAIT UNTIL THE GIVEN HWND BECOMES THE FOREGROUND WINDOW
def window_foreground_waiter(hwnd: int, timeout: float = 5.0) -> bool:
    start = time.time()
    while time.time() - start < timeout:
        try:
            if win32gui.GetForegroundWindow() == hwnd:
                return True
        except Exception:
            pass
        time.sleep(0.1)
    return False


# FIND THE MAIN VISIBLE WINDOW FOR A PROCESS MATCHING FILTERS
def window_checker(
    process_name: str,
    class_filter: Optional[str] = None,
    title_filter: Optional[str] = None,
) -> Optional[int]:
    windows: List[tuple[int, int]] = []

    def enum_windows(hwnd, result):
        try:
            if not win32gui.IsWindowVisible(hwnd):
                return True

            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            process = psutil.Process(pid)
            proc_name = (process.name() or "").lower()
            class_name = (win32gui.GetClassName(hwnd) or "").lower()
            title = win32gui.GetWindowText(hwnd) or ""

            # MATCH PROCESS NAME AND OPTIONAL FILTERS
            if process_name.lower() in proc_name:
                if class_filter and class_filter.lower() not in class_name:
                    return True
                if title_filter and title_filter.lower() not in title.lower():
                    return True
                result.append((hwnd, len(title)))

        # IGNORE WINDOWS WE CANNOT ACCESS (SYSTEM/PRIVILEGE ISSUES)
        except Exception:
            pass
        return True

    win32gui.EnumWindows(enum_windows, windows)
    if windows:
        windows.sort(key=lambda x: x[1], reverse=True)
        return windows[0][0]
    return None


# ABSTRACT STRATEGY FOR ACTIVATING A WINDOW
class WindowActivationStrategy(ABC):
    @abstractmethod
    def activate(self, hwnd: int) -> bool:
        pass


# ATTACH THREAD INPUT STRATEGY
class ThreadAttachStrategy(WindowActivationStrategy):
    def activate(self, hwnd: int) -> bool:

        # ATTEMPT TO ATTACH THREAD INPUT AND SET FOREGROUND
        current = win32api.GetCurrentThreadId()
        foreground = win32gui.GetForegroundWindow()
        if not foreground or hwnd == foreground:
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                return True
            except Exception:
                return False

        try:
            foreground_thread = win32process.GetWindowThreadProcessId(foreground)[0]
            target_thread = win32process.GetWindowThreadProcessId(hwnd)[0]

            # ATTACH AND ENSURE WE ALWAYS DETACH
            win32process.AttachThreadInput(current, foreground_thread, True)
            win32process.AttachThreadInput(target_thread, foreground_thread, True)
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.BringWindowToTop(hwnd)
            success = False

            try:
                success = bool(win32gui.SetForegroundWindow(hwnd))
            except Exception:
                success = False

            # ALWAYS DETACH THREAD INPUT
            finally:
                try:
                    win32process.AttachThreadInput(
                        target_thread, foreground_thread, False
                    )
                except Exception:
                    pass
                try:
                    win32process.AttachThreadInput(current, foreground_thread, False)
                except Exception:
                    pass
            return success

        except Exception as e:
            logger.warning(f"[WINDOW] THREAD ATTACH FAILED: {e}")
            return False


# FORCE ACTIVATE BY SHOWING, BRINGING TO TOP AND SETTING FOREGROUND
class ForceActivateStrategy(WindowActivationStrategy):
    def activate(self, hwnd: int) -> bool:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            win32gui.BringWindowToTop(hwnd)
            win32gui.SetForegroundWindow(hwnd)
            return True
        except Exception as e:
            logger.warning(f"[WINDOW] FORCE ACTIVATE FAILED: {e}")
            return False


# BYPASS FOREGROUND LOCK TIMEOUT USING SYSTEM PARAMETERS
class TimeoutBypassStrategy(WindowActivationStrategy):
    def activate(self, hwnd: int) -> bool:
        try:
            user32 = ctypes.windll.user32
            timeout = wintypes.UINT()

            # READ CURRENT VALUE
            user32.SystemParametersInfoW(
                SPI_GETFOREGROUNDLOCKTIMEOUT, 0, ctypes.byref(timeout), 0
            )

            # SET TO 0 TO ALLOW SETFOREGROUND
            user32.SystemParametersInfoW(
                SPI_SETFOREGROUNDLOCKTIMEOUT, 0, 0, SPIF_SENDWININICHANGE
            )

            # RESTORE ORIGINAL VALUE
            try:
                win32gui.SetForegroundWindow(hwnd)
            finally:
                user32.SystemParametersInfoW(
                    SPI_SETFOREGROUNDLOCKTIMEOUT,
                    0,
                    timeout.value,
                    SPIF_SENDWININICHANGE,
                )
            return True

        except Exception as e:
            logger.warning(f"[WINDOW] TIMEOUT BYPASS FAILED: {e}")
            return False


# CONTROLLER THAT TRIES STRATEGIES IN ORDER
class WindowController:

    # STRATEGIES ORDERED FROM LEAST INTRUSIVE TO MOST
    def __init__(self):
        self.strategies: List[WindowActivationStrategy] = [
            ThreadAttachStrategy(),
            ForceActivateStrategy(),
            TimeoutBypassStrategy(),
        ]

    def activate(self, hwnd: int) -> bool:
        for strategy in self.strategies:
            try:
                if strategy.activate(hwnd):
                    if window_foreground_waiter(
                        hwnd,
                        timeout=(
                            CONFIG["WAIT_TIME"]["TEN_SECOND"]
                            if "WAIT_TIME" in CONFIG
                            and "TEN_SECOND" in CONFIG["WAIT_TIME"]
                            else 5
                        ),
                    ):
                        logger.info("[WINDOW] ACTIVATION SUCCESS")
                        return True
            except Exception as e:
                logger.warning(f"[WINDOW] STRATEGY ERROR: {e}")
        logger.error("[WINDOW] ALL ACTIVATION METHODS FAILED")
        return False

    def maximize(self, hwnd: int) -> bool:
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            placement = win32gui.GetWindowPlacement(hwnd)

            # INDEX 1 IS SHOWCMD
            if placement[1] == win32con.SW_SHOWMAXIMIZED:
                return True

            # FALLBACK TO KEYBOARD SHORTCUT
            pyautogui.hotkey("win", "up")
            placement = win32gui.GetWindowPlacement(hwnd)
            return placement[1] == win32con.SW_SHOWMAXIMIZED
        except Exception as e:
            logger.error(f"[WINDOW] MAXIMIZE FAILED: {e}")
            return False


# BASE CLASS FOR APPLICATION MANAGERS
class BaseAppManager(ABC):

    # INITIALISE MANAGER WITH NAME, PATH AND CONTROLLER
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
        self.controller = WindowController()

    def running_process_result(self) -> bool:
        return running_process_checker(self.name)

    def validate_executer(self) -> None:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"EXEC NOT FOUND : {self.path}")

    # OPEN OR RESTORE APPLICATION AND ENSURE IT IS MAXIMISED
    def open(self) -> bool:
        if self.running_process_result():
            logger.info(f"[SYSTEM] RESTORING {self.name.upper()}")
            hwnd = self.window_checker()
            if hwnd:
                return self.controller.activate(hwnd) and self.controller.maximize(hwnd)

        # LAUNCH APPLICATION IF NOT RUNNING
        logger.info(f"[SYSTEM] LAUNCHING {self.name.upper()}")
        self.validate_executer()
        try:
            self.launch()
        except Exception as e:
            logger.error(f"[SYSTEM] FAILED TO LAUNCH {self.name.upper()}: {e}")
            return False

        wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
        hwnd = self.window_checker()
        if hwnd:
            return self.controller.activate(hwnd) and self.controller.maximize(hwnd)
        logger.error(f"[SYSTEM] NOT FIND {self.name.upper()} AFTER LAUNCH")
        return False

    @abstractmethod
    def window_checker(self) -> Optional[int]:
        pass

    @abstractmethod
    def launch(self) -> None:
        pass


# CHROME MANAGER
class ChromeManager(BaseAppManager):
    def __init__(self, path: str):
        super().__init__("chrome", path)

    def window_checker(self) -> Optional[int]:
        return window_checker("chrome", class_filter="chrome")

    # USE LIST-STYLE POPEN TO AVOID SHELL
    def launch(self) -> None:
        os.startfile(self.path)


# OUTLOOK MANAGER
class OutlookManager(BaseAppManager):
    def __init__(self, path: str):
        super().__init__("outlook", path)

    def window_checker(self) -> Optional[int]:
        return window_checker("outlook", class_filter="rctrl_renwnd32")

    # USE OS STARTFILE FOR REGISTERED PROTOCOLS/FILES
    def launch(self) -> None:
        os.startfile(self.path)

    # SEND KEY COMMANDS TO OUTLOOK WHEN ITS WINDOW IS ACTIVE
    def send_command(self, keys, desc: str = "") -> bool:
        hwnd = self.window_checker()
        if hwnd and self.controller.activate(hwnd):
            wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
            try:
                if isinstance(keys, list):
                    pyautogui.hotkey(*keys)
                else:
                    pyautogui.press(keys)
                logger.info(f"[SYSTEM] SENT OUTLOOK COMMAND : {desc}")
                return True
            except Exception as e:
                logger.error(f"[SYSTEM] FAILED TO SEND OUTLOOK COMMAND : {e}")
        return False


# FACTORY FUNCTIONS
def chrome_manager() -> ChromeManager:
    return ChromeManager(CONFIG["CHROME_PATH"])


def outlook_manager() -> OutlookManager:
    return OutlookManager(CONFIG["OUTLOOK_PATH"])


def open_chrome() -> bool:
    return chrome_manager().open()


def open_outlook() -> bool:
    return outlook_manager().open()


def send_outlook_command(keys, desc: str = "") -> bool:
    return outlook_manager().send_command(keys, desc)


def check_chrome_status() -> bool:
    return running_process_checker("chrome")


def check_outlook_status() -> bool:
    return running_process_checker("outlook")


if __name__ == "__main__":
    open_chrome()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    open_outlook()
