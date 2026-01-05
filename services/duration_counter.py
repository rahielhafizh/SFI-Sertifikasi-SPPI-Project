import time
import datetime
from services.config import logger


start_timer = None
end_timer = None
on_going = False


def start_counter():
    global start_timer, on_going
    start_timer = time.time()
    on_going = True
    logger.warning(
        f"[SYSTEM] TIMER START AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return start_timer


def stop_counter():
    global end_timer, on_going
    if not on_going:
        logger.error("[ERROR] TIMER NOT STARTED")
        return None
    end_timer = time.time()
    on_going = False
    logger.warning(
        f"[SYSTEM] TIMER STOP AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return end_timer


def get_duration_result(format_output=True):
    global start_timer, end_timer
    if start_timer is None:
        logger.error("[ERROR] TIMER NOT STARTED, DURATION UNAVAILABLE")
        return None
    execution_seconds = (time.time() if end_timer is None else end_timer) - start_timer
    if format_output:
        hours, remainder = divmod(execution_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return execution_seconds


def log_counter_execution(process_name=None):
    execution_time = get_duration_result()
    process_str = f" FOR {process_name.upper()}" if process_name else ""
    log_message = f"[SYSTEM] TOTAL EXECUTION TIME{process_str} : {execution_time}"
    logger.info(log_message)
    return log_message


def reset_timer():
    global start_timer, end_timer, on_going
    start_timer = None
    end_timer = None
    on_going = False
    logger.debug("[SYSTEM] TIMER RESET")


def check_running_timer():
    return on_going


class ExecutionTimer:
    def __init__(self, process_name=None):
        self.process_name = process_name

    def __enter__(self):
        start_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        stop_counter()
        log_counter_execution(self.process_name)
        return False
