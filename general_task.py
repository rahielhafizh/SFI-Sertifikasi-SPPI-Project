import keyboard
import pyautogui
from services.config import load_config, wait_timer, logger
from pynput.keyboard import Key, Controller

CONFIG = load_config()
keyboard = Controller()


def adjust_picture_size():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] ADJUSTING PICTURE SIZE")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("w")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.write("70")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def blank_mail_space():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] ADDING BLANK SPACE IN OUTLOOK")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def break_excel_link():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] BREAKING EXCEL LINKS")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("k")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("tab", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("left")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def capture_table_as_bitmap():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CAPTURING TABLE AS BITMAP")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("down")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def capture_table_as_picture():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CAPTURING TABLE AS PICTURE")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("p")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def capture_table_as_table():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] CAPTURING TABLE AS RAW DATA")
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("ctrl", "a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("c")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def choose_file_attach():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] OPENING FILE ATTACHMENT DIALOG")
    pyautogui.hotkey("alt", "n")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("f")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def close_no_save():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CLOSING EXCEL WITHOUT SAVING")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def close_unsave():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CLOSING EXCEL WITHOUT SAVING CHANGES")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def close_with_save():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] SAVING AND CLOSING EXCEL")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def confirm():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CONFIRMING OR ENTERING")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def confirm_file_attach():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CHOOSING FILE ATTACHMENT")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def convert_to_range():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CONVERTING TABLE TO RANGE")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j", "t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("g")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def creating_new_task():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CREATING NEW TASK")
    pyautogui.hotkey("ctrl", "n")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def finish_outlook():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SENT EMAIL AND CLOSE OUTLOOK")
    pyautogui.hotkey("alt", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def handle_not_activated_office():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] HANDLING OFFICE ACTIVATION DIALOG")
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def handle_office():
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    logger.info("[SYSTEM] HANDLING OFFICE DIALOG")
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def input_clipboard_picture():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] PASTING CLIPBOARD IMAGE")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def input_dynamic_picture():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] PASTING ADJUSTABLE SIZE IMAGE")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def input_hyperlink():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] INSERTING HYPERLINK")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("n")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("i")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def make_new_pivot_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CREATING NEW SHEET FOR PIVOT")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("n")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def maximize_app_window():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] MAXIMIZING APPLICATION WINDOW")
    pyautogui.hotkey("win", "up")
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])


def minimize_text():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] MINIMIZE TEXT")
    for _ in range(2):
        pyautogui.hotkey("alt")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.hotkey("h")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.hotkey("f")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        pyautogui.hotkey("k")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def move_or_copy_as_newbook():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] COPYING SHEET TO NEW WORKBOOK")
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("up", presses=5)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("tab", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def move_or_copy_menu():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] OPENING MOVE OR COPY MENU")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("e")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("m")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def paste_value_as_value():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] PASTING VALUES ONLY")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("v")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])


def refresh_excel_data():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] REFRESHING EXCEL DATA")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("r")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_as_in():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO SAVE DIRECTORY")
    pyautogui.hotkey("f12")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=11)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_as_name():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SETTING FILE NAME")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def save_new_book():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] SAVING NEW WORKBOOK")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=2)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=11)
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def save_new_copy():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[DATA] SAVING NEW COPY")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=11)
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def select_hyperlink():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SELECTING HYPERLINK TEXT")
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
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SELECTING SHEETS DOWNWARD")
    for _ in range(10):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_sheet_up():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SELECTING SHEETS UPWARD")
    for _ in range(10):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.page_up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_sheet_order_in():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SELECTING SHEETS IN ORDER")
    for _ in range(2):
        keyboard.press(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.page_down)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.ctrl)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def select_header_content():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    logger.info("[SYSTEM] SELECTING HEADER CONTENT")
    for _ in range(5):
        keyboard.press(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.press(Key.up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.shift)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
        keyboard.release(Key.up)
        wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def set_new_book_name():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SETTING NEW WORKBOOK NAME")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def set_text_right():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] SET SELECTED TEKS TO THE RIGHT")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("h")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("a")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("r")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def set_new_pivot_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] CONFIGURING NEW PIVOT SHEET")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("l")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("j")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("t")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("l")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("space")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.press("up", presses=4)
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])


def switch_to_first_cells():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO FIRST CELLS")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "up")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    for _ in range(5):
        pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def switch_to_first_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO FIRST SHEET")
    for _ in range(10):
        pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def switch_to_last_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO LAST SHEET")
    for _ in range(10):
        pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def switch_to_right_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO RIGHT SHEET")
    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def switch_to_left_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO RIGHT SHEET")
    pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def switch_to_table_cells():
    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO TABLE SUMMARY CELLS")
    pyautogui.press("down", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("right", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
