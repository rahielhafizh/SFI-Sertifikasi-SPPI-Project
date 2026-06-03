import keyboard
import pyautogui
from services.config import load_config, wait_timer, logger
from pynput.keyboard import Key, Controller

CONFIG = load_config()
keyboard = Controller()


def action_paste():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def adjust_picture_size():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] ADJUST IMAGE WIDTH VIA ALT MENU")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("w")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.write("70")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def blank_mail_space():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] INSERT BLANK SPACE IN EMAIL BODY")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def break_excel_link():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CONVERT LINKED EXCEL FILE TO STATIC VALUES")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("k")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("tab", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("left")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def capture_table_as_bitmap():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CAPTURE TABLE TO BITMAP FORMAT")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("down")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def capture_table_as_picture():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CAPTURE TABLE TO PICTURE FORMAT")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def capture_table_as_table():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CAPTURE TABLE AS TABLE FORMAT")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def choose_file_attach():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] LAUNCH FILE ATTACHMENT DIALOG")
    pyautogui.hotkey("alt", "n")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("f")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def close_unsave():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CLOSE WORKBOOK WITHOUT SAVING")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])


def closing_tab():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CLOSE ACTIVE WINDOW")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def confirm():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CONFIRMATION ACTION")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def confirm_file_attach():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CONFIRM FILE ATTACHMENT")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("tab", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def convert_to_range():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CONVERT TO STANDARD CELL RANGE")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("j", "t")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("g")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def creating_new_task():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CREATE NEW TASK")
    pyautogui.hotkey("ctrl", "n")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def entering_operation():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXECUTE MULTI-ENTERING DIALOG")
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def finish_outlook():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SEND EMAIL AND CLOSE OUTLOOK")
    pyautogui.hotkey("alt", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def minimize_outlook():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SEND EMAIL AND MINIMIZE OUTLOOK")
    pyautogui.hotkey("alt", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("win", "m")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def handle_office():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] HANDLING OFFICE STARTUP DIALOGS")
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def input_clipboard_picture():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] INSERT CLIPBOARD IMAGE")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def input_dynamic_picture():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] PASTE IMAGE THEN FORMAT")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def input_hyperlink():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] OPEN HYPERLINK DIALOG")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("n")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("i")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def make_new_pivot_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CREATE NEW PIVOT TABLE SHEET")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("n")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def maximize_app_window():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] MAXIMIZE WINDOW TO FULLSCREEN")
    pyautogui.hotkey("win", "up")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def minimize_text():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] REDUCE FONT SIZE")
    for _ in range(2):
        pyautogui.hotkey("alt")
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pyautogui.hotkey("h")
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pyautogui.hotkey("f")
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        pyautogui.hotkey("k")
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def move_cell_horizontal():
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    logger.info("[DATA] MOVE CELL TO KEEP SCREEN ACTIVE")
    pyautogui.hotkey("ctrl", "right")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.hotkey("ctrl", "right")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def move_or_copy_as_newbook():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] COPY SHEET TO NEW WORKBOOK")
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("tab", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("up", presses=5)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])
    pyautogui.press("tab", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def move_or_copy_menu():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] OPEN MOVE OR COPY DIALOG")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("e")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("m")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def paste_value_as_value():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] PASTE AS VALUES ONLY")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def refresh_excel_data():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] REFRESH ALL DATA CONNECTIONS")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("r")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_as_in():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] OPEN SAVE AS DIALOG")
    pyautogui.hotkey("f12")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_as_name():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] NAVIGATE TO FILENAME FIELD")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_file():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] SAVE CURRENT DOCUMENT")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_new_book():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] SAVE NEW WORKBOOK")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("tab", presses=2)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_new_copy():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] SAVE FILE WITH NEW NAME")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_header_content():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    logger.info("[SYSTEM] SELECT HEADER CONTENT")
    for _ in range(5):
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.up)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.up)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_hyperlink():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SELECT HYPERLINK TEXT")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    keyboard.press(Key.shift)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    keyboard.press(Key.up)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    keyboard.release(Key.shift)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    keyboard.release(Key.up)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_sheet_down():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION DOWNWARD")
    for _ in range(15):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])


def select_sheet_half_down():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION DOWNWARD PARTIAL")
    for _ in range(5):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_sheet_half_up():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION UPWARD PARTIAL")
    for _ in range(5):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_sheet_order_in():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SELECT WORKSHEETS FOR REPORT")
    for _ in range(2):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_sheet_up():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXTEND SELECTION UPWARD")
    for _ in range(10):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.press(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def set_new_book_name():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CLEAR FILENAME FOR INPUT")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def set_new_pivot_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CONFIGURE PIVOT TABLE LAYOUT")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("l")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("l")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("up", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def set_text_right():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] APPLY RIGHT TEXT ALIGNMENT")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("r")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def switch_to_first_cells():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] NAVIGATE TO FIRST CELLS")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "up")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_first_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SWITCH TO FIRST SHEET")
    for _ in range(15):
        pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_last_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SWITCH TO LAST SHEET")
    for _ in range(15):
        pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_left_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SWITCH TO PREVIOUS SHEET")
    pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_right_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SWITCH TO NEXT SHEET")
    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_table_cells():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] NAVIGATE TO TABLE CELLS")
    pyautogui.press("down", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])
    pyautogui.press("right", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])
