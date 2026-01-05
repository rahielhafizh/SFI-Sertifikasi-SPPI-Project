import keyboard
import pyautogui
from services.config import load_config, wait_timer, logger
from pynput.keyboard import Key, Controller

CONFIG = load_config()
keyboard = Controller()


def adjust_picture_size():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] ADJUSTING IMAGE WIDTH VIA ALT MENU SEQUENCE")
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
    logger.info("[SYSTEM] INSERTING SPACING IN EMAIL COMPOSITION BODY")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["TENTH_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def break_excel_link():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CONVERT LINKED EXCEL CONTENT TO STATIC VALUES")
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
    logger.info("[DATA] CONVERTING SELECTED TABLE TO BITMAP FORMAT")
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
    logger.info("[DATA] CONVERTING SELECTED TABLE TO PICTURE FORMAT")
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
    logger.info("[DATA] COPYING TABLE AS EDITABLE CELL FORMATTING")
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
    logger.info("[SYSTEM] LAUNCHING FILE ATTACHMENT DIALOG IN MICROSOFT OUTLOOK")
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


def closing_tab():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] TERMINATING ACTIVE APPLICATION WINDOW")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def close_unsave():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CLOSING WORKBOOK AND DISCARDING UNSAVED MODIFICATIONS")
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("tab")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])


def save_file():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] PERSISTING CURRENT DOCUMENT STATE TO STORAGE")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def confirm():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXECUTING CONFIRMATION ACTION TO CURRENT OPERATION")
    pyautogui.press("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def confirm_file_attach():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] FINALISING FILE ATTACHMENT SELECTION IN REPORT MAIL")
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
    logger.info("[DATA] CONVERTING STRUCTURED OBJECT TO STANDARD CELL FORMAT")
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
    logger.info("[SYSTEM] INITIATING NEW DOCUMENT/TASK INSTANCE")
    pyautogui.hotkey("ctrl", "n")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])


def finish_outlook():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] DISPATCHING MESSAGE AND TERMINATING MICROSOFT OUTLOOK")
    pyautogui.hotkey("alt", "s")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.hotkey("alt", "f4")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])


def handle_not_activated_office():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] BYPASSING OFFICE ACTIVATION PROMPTS")
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def handle_office():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] DISMISSING OFFICE STARTUP DIALOGS")
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("esc")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def input_clipboard_picture():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] INSERTING CLIPBOARD IMAGE CONTENT")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def input_dynamic_picture():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] PASTING IMAGE WITH PRESERVED SCALING CAPABILITIES")
    pyautogui.hotkey("ctrl", "v")
    wait_timer(CONFIG["WAIT_TIME"]["FIVE_SECOND"])
    pyautogui.hotkey("right")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def input_hyperlink():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] OPENING HYPERLINK INSERTION FOR URL ATTACHMENT")
    pyautogui.press("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("n")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("i")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def make_new_pivot_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] GENERATING NEW WORKSHEET FOR PIVOT TABLE STRUCTURE")
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
    logger.info("[SYSTEM] EXPANDING ACTIVE WINDOW TO FULL SCREEN MODE")
    pyautogui.hotkey("win", "up")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def minimize_text():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] REDUCING FONT SIZE OF SELECTED TEXT")
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
    logger.info("[DATA] MOVING CELL TO MAKE SCREEN KEEP ACTIVE")
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
    logger.info("[DATA] DUPLICATING ACTIVE WORKSHEET INTO NEW WORKBOOK FILE")
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
    logger.info("[SYSTEM] ACCESSING RELOCATION DIALOG FOR MOVE OR COPY OPERATIONS")
    pyautogui.hotkey("alt")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("e")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("m")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def paste_value_as_value():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] PASTING CLIPBOARD CONTENT AS UNFORMATTED VALUES")
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
    logger.info("[DATA] SYNCHRONISING ALL DATA CONNECTIONS TO RETRIEVE UPDATED VALUES")
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
    logger.info("[SYSTEM] ACCESSING SAVE AS DIALOG AND NAVIGATING TO TARGET DIRECTORY")
    pyautogui.hotkey("f12")
    wait_timer(CONFIG["WAIT_TIME"]["TEN_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_as_name():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] POSITIONING ACTIVE CURSOR IN FILENAME FIELD")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def save_new_book():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] COMMITTING NEW WORKBOOK TO SPECIFIED LOCATION")
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
    logger.info("[DATA] SAVING FILE WITH MODIFIED FILENAME IN SPECIFIED DIRECTORY")
    pyautogui.hotkey("ctrl", "s")
    wait_timer(CONFIG["WAIT_TIME"]["FIFTEEN_SECOND"])
    pyautogui.press("tab", presses=10)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("space")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.press("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def select_hyperlink():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] HIGHLIGHTING HYPERLINK TEXT")
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
    logger.info("[SYSTEM] EXTENDING WORKSHEET SELECTION DOWNWARD")
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
    logger.info("[SYSTEM] EXTENDING WORKSHEET SELECTION DOWNWARD - PARTIAL RANGE")
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


def select_sheet_up():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXTENDING WORKSHEET SELECTION UPWARD")
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


def select_sheet_half_up():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXTENDING WORKSHEET SELECTION UPWARD - PARTIAL RANGE")
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
    logger.info("[SYSTEM] SELECTING SPECIFIED WORKSHEETS FOR ORDER IN REPORT")
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


def select_header_content():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("enter")
    logger.info("[SYSTEM] SELECTING HEADER SECTION CONTENT")
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


def set_new_book_name():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] CLEARING FILENAME AND PREPARING FOR INPUT")
    pyautogui.press("tab", presses=6)
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    pyautogui.hotkey("backspace")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])


def set_text_right():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] APPLYING RIGHT TEXT ALIGNMENT TO SELECTED CELL CONTENT")
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


def set_new_pivot_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[DATA] CONFIGURING PIVOT TABLE LAYOUT AND DESIGN SETTINGS")
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


def switch_to_first_cells():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] INITIATED NAVIGATION TO FIRST CELLS/TOP-LEFT POSITION")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "up")
    for _ in range(5):
        pyautogui.hotkey("ctrl", "left")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_first_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXECUTING TRANSITION TO FIRST SHEET")
    for _ in range(15):
        pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_last_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] EXECUTING TRANSITION TO LAST SHEET")
    for _ in range(15):
        pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_left_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SWITCHING TO LEFT SHEET/PREVIOUS DATA WORKSHEET")
    pyautogui.hotkey("ctrl", "pgup")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_right_sheet():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] SWITCHING TO RIGHT SHEET/NEXT DATA WORKSHEET")
    pyautogui.hotkey("ctrl", "pagedown")
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])


def switch_to_table_cells():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] NAVIGATING TO TABLE SUMMARY CELLS")
    pyautogui.press("down", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])
    pyautogui.press("right", presses=3)
    wait_timer(CONFIG["WAIT_TIME"]["ONEHALF_SECOND"])

def entering_operation():
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])
    logger.info("[SYSTEM] PRESSING ENTER KEY TO HANDLE OPERATION DIALOG")
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
    pyautogui.hotkey("enter")
    wait_timer(CONFIG["WAIT_TIME"]["HALF_SECOND"])