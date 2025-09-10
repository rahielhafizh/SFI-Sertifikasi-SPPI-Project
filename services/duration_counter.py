import time
import datetime
from services.config import logger


# TIMER STATE VARIABLES
_start_time = None
_end_time = None
_is_running = False


# STARTS THE TIMER AND MARKS IT AS RUNNING
def start_counter():
    global _start_time, _is_running
    _start_time = time.time()
    _is_running = True
    logger.warning(
        f"[SYSTEM] TIMER STARTED AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return _start_time


# STOPS THE TIMER IF RUNNING, OTHERWISE LOGS ERROR
def stop_counter():
    global _end_time, _is_running
    if not _is_running:
        logger.error("[ERROR] TIMER HAS NOT BEEN STARTED")
        return None
    _end_time = time.time()
    _is_running = False
    logger.warning(
        f"[SYSTEM] TIMER STOPPED AT {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )
    return _end_time


# RETURNS EXECUTION DURATION IN RAW SECONDS
def get_duration_result(format_output=True):
    global _start_time, _end_time
    if _start_time is None:
        logger.error("[ERROR] TIMER HAS NOT BEEN STARTED, DURATION UNAVAILABLE")
        return None
    execution_seconds = (time.time() if _end_time is None else _end_time) - _start_time
    if format_output:
        hours, remainder = divmod(execution_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    return execution_seconds


# LOGS TOTAL EXECUTION TIME WITH OPTIONAL PROCESS NAME CONTEXT
def log_counter_execution(process_name=None):
    execution_time = get_duration_result()
    process_str = f" FOR {process_name.upper()}" if process_name else ""
    log_message = f"[SYSTEM] TOTAL EXECUTION TIME{process_str} : {execution_time}"
    logger.info(log_message)
    return log_message


# FULLY RESETS THE TIMER STATE
def reset_timer():
    global _start_time, _end_time, _is_running
    _start_time = None
    _end_time = None
    _is_running = False
    logger.debug("[SYSTEM] TIMER HAS BEEN RESET")


# RETURNS TRUE IF TIMER IS CURRENTLY ACTIVE
def is_timer_running():
    return _is_running


# CONTEXT MANAGER FOR AUTOMATIC START/STOP AND EXECUTION LOGGING
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
