from __future__ import annotations
import os
import sys
import time
import random
import subprocess
import psutil
import argparse
import math
from datetime import datetime
from collections import deque
from typing import Deque, Callable, Optional, List
from pynput import mouse
from services.config import load_config, logger

CONFIG = load_config()
CM_TO_PIXELS = 37.8


class ScreenKeeperState:
    def __init__(self) -> None:
        self.click_times: Deque[float] = deque(maxlen=3)
        self.stop_flag: bool = False
        self.last_keypress_time: float = time.time()
        self.last_pattern_switch: float = time.time()
        self.idle_check_time: float = time.time()
        self.keypress_interval: float = random.uniform(3, 5)
        self.pattern_switch_interval: float = random.uniform(20, 40)

    def record_click(self) -> None:
        self.click_times.append(time.time())

    def setup_stop_keeper(self) -> bool:
        if (
            len(self.click_times) == 3
            and (self.click_times[-1] - self.click_times[0]) <= 2
        ):
            self.stop_flag = True
            return True
        return False

    def get_adaptive_sleep(self, base: float) -> float:
        try:
            cpu = psutil.cpu_percent(interval=0.05)
            return max(0.005, base * (1.0 - (cpu / 200)))
        except Exception:
            return base

    def run_switch_pattern(self) -> bool:
        now = time.time()
        if now - self.last_pattern_switch >= self.pattern_switch_interval:
            self.last_pattern_switch = now
            self.pattern_switch_interval = random.uniform(20, 40)
            return True
        return False

    def run_activity_simulator(self) -> bool:
        now = time.time()
        if now - self.last_keypress_time >= self.keypress_interval:
            self.last_keypress_time = now
            self.keypress_interval = random.uniform(3, 5)
            return True
        return False

    def run_night_simulator(self) -> bool:
        now = time.time()
        if now - self.idle_check_time >= 30:
            self.idle_check_time = now
            hour = datetime.now().hour
            return hour <= 6 or hour >= 22
        return False


class PatternManager:
    def __init__(self) -> None:
        self.patterns: List[
            Callable[[float, float, float, float], tuple[float, float]]
        ] = [self.circle, self.figure8, self.zigzag]
        self.current = random.choice(self.patterns)

    def get_current_pattern(
        self,
    ) -> Callable[[float, float, float, float], tuple[float, float]]:
        return self.current

    def switch_pattern(self) -> None:
        choices = [p for p in self.patterns if p is not self.current]
        self.current = random.choice(choices) if choices else self.current

    def circle(
        self, cx: float, cy: float, angle: float, r: float
    ) -> tuple[float, float]:
        x = cx + r * random.uniform(0.9, 1.1) * math.cos(angle)
        y = cy + r * random.uniform(0.9, 1.1) * math.sin(angle)
        return x, y

    def figure8(
        self, cx: float, cy: float, angle: float, r: float
    ) -> tuple[float, float]:
        x = cx + r * math.sin(angle)
        y = cy + (r / 2) * math.sin(2 * angle)
        return x, y

    def zigzag(
        self, cx: float, cy: float, angle: float, r: float
    ) -> tuple[float, float]:
        progress = (angle % (2 * math.pi)) / (2 * math.pi)
        amp = r * 0.8
        x = cx + amp * math.sin(progress * 8 * math.pi)
        y = cy + progress * amp * 2 - amp
        return x, y


class ActivitySimulator:
    def __init__(self, keyboard_module=None) -> None:
        self.keyboard = keyboard_module or __import__("keyboard")

    def setup_keyboard(self) -> None:
        try:
            action = random.choice(["left", "right", "up", "down"])
            self.keyboard.press_and_release(action)
            logger.info("[SCREEN] SIMULATED KEYPRESS")
        except Exception as e:
            logger.warning(f"[SCREEN] SIMULATION FAILED: {e}")

    def simulate_night(self) -> None:
        if random.random() < 0.3:
            self.setup_keyboard()
            logger.info("[SCREEN] NIGHT ACTIVITY TRIGGERED")


class ScreenKeeperService:
    def __init__(self, activity_simulator: Optional[ActivitySimulator] = None) -> None:
        self.state = ScreenKeeperState()
        self.pattern_manager = PatternManager()
        self.activity_simulator = activity_simulator or ActivitySimulator()

    def right_click(self, x: float, y: float, button, pressed) -> bool:
        try:
            if button == mouse.Button.right and pressed:
                self.state.record_click()
                if self.state.setup_stop_keeper():
                    logger.info("[SCREEN] RIGHT CLICK STOP SEQUENCE DETECTED")
                    return False
        except Exception:
            pass
        return True

    def run_pattern_loop(
        self, diameter_cm: float, movement_time: float, sleep_time: float
    ) -> None:
        pyautogui = __import__("pyautogui")
        pyautogui.FAILSAFE = True
        radius_px = (diameter_cm * CM_TO_PIXELS) / 2
        screen_width, screen_height = pyautogui.size()
        centre_x, centre_y = screen_width / 2, screen_height / 2
        angle = random.uniform(0, 2 * math.pi)
        direction = 1
        listener = mouse.Listener(on_click=self.right_click)
        listener.start()
        logger.info("[SCREEN] SCREEN KEEPER STARTED")
        logger.warning("[SCREEN] PRESS RIGHT-CLICK 3 TIMES QUICKLY TO STOP")

        try:
            while not self.state.stop_flag:
                pattern_fn = self.pattern_manager.get_current_pattern()
                x, y = pattern_fn(centre_x, centre_y, angle, radius_px)
                try:
                    pyautogui.moveTo(
                        x, y, duration=movement_time * random.uniform(0.8, 1.2)
                    )
                except Exception as e:
                    logger.warning(f"[SCREEN] MOVE FAILED: {e}")

                time.sleep(self.state.get_adaptive_sleep(sleep_time))
                angle += 0.05 * direction

                if self.state.run_switch_pattern():
                    self.pattern_manager.switch_pattern()
                    direction *= -1
                    logger.info("[SCREEN] PATTERN SWITCHED")

                if self.state.run_activity_simulator():
                    self.activity_simulator.setup_keyboard()

                if self.state.run_night_simulator():
                    self.activity_simulator.simulate_night()

        except KeyboardInterrupt:
            logger.info("[SCREEN] INTERRUPTED BY KEYBOARD")
        except Exception as e:
            logger.error(f"[ERROR] UNEXPECTED ERROR IN PATTERN LOOP: {e}")
        finally:
            try:
                listener.stop()
            except Exception:
                pass
            logger.info("[SCREEN] SCREEN KEEPER STOPPED")

    def launch_background(
        self, diameter: float, movement_time: float, sleep_time: float
    ) -> bool:
        script_path = os.path.abspath(__file__)
        python_exec = sys.executable
        if sys.platform == "win32" and python_exec.lower().endswith("python.exe"):
            python_exec = python_exec[: -len("python.exe")] + "pythonw.exe"

        cmd = [
            python_exec,
            script_path,
            "--background",
            "--diameter",
            str(diameter),
            "--movement-time",
            str(movement_time),
            "--sleep-time",
            str(sleep_time),
        ]

        try:
            creationflags = (
                subprocess.CREATE_NEW_PROCESS_GROUP if sys.platform == "win32" else 0
            )
            subprocess.Popen(
                cmd,
                creationflags=creationflags,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(0.8)
            logger.info("[SYSTEM] BACKGROUND PROCESS STARTED")
            return True
        except Exception as e:
            logger.error(f"[ERROR] FAILED TO START BACKGROUND PROCESS: {e}")
            return False

    def stop_all(self) -> bool:
        logger.info("[SYSTEM] STOPPING SCREEN KEEPER PROCESSES")
        found = False

        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                name = (proc.info.get("name") or "").lower()
                cmdline = proc.info.get("cmdline") or []
                if "python" in name and any(
                    "screen_keeper" in (part or "").lower() for part in cmdline
                ):
                    found = True
                    try:
                        proc.terminate()
                        logger.info(f"[SYSTEM] TERMINATED {proc.pid}")
                        proc.wait(timeout=2)
                    except Exception:
                        try:
                            proc.kill()
                            logger.info(f"[SYSTEM] KILLED {proc.pid}")
                        except Exception as e:
                            logger.error(f"[ERROR] FAILED TO KILL {proc.pid}: {e}")
            except Exception:
                continue

        if not found:
            logger.warning("[SYSTEM] NO SCREEN KEEPER PROCESS FOUND")
        return not self.check_running_keeper()

    def check_running_keeper(self) -> bool:
        for proc in psutil.process_iter(["cmdline"]):
            try:
                cmdline = proc.info.get("cmdline") or []
                if any("screen_keeper" in (part or "").lower() for part in cmdline):
                    return True
            except Exception:
                continue
        return False


keeper_instance = ScreenKeeperService()


def find_screen_keeper_process() -> bool:
    return keeper_instance.check_running_keeper()


def stop_screen_keeper() -> bool:
    return keeper_instance.stop_all()


def run_screen_keeper(
    diameter: float = 5.0,
    movement_time: float = 0.015,
    sleep_time: float = 0.05,
    background: bool = True,
) -> Optional[bool]:
    if background:
        return keeper_instance.launch_background(diameter, movement_time, sleep_time)
    else:
        keeper_instance.run_pattern_loop(diameter, movement_time, sleep_time)
        return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Screen Keeper")
    parser.add_argument("--background", action="store_true")
    parser.add_argument("--stop", action="store_true")
    parser.add_argument("--diameter", type=float, default=5.0)
    parser.add_argument("--movement-time", type=float, default=0.15)
    parser.add_argument("--sleep-time", type=float, default=0.05)
    args = parser.parse_args()

    if args.stop:
        sys.exit(0 if stop_screen_keeper() else 1)

    if args.background:
        run_screen_keeper(
            args.diameter, args.movement_time, args.sleep_time, background=False
        )
    else:
        success = run_screen_keeper(
            args.diameter, args.movement_time, args.sleep_time, background=True
        )
        sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
