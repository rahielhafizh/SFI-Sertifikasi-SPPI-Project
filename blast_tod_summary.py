import os
import pyautogui
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from general_task import *
from pynput.keyboard import Controller
from services.remover_tod_report import clear_submission_folder
from services.config import load_config, wait_timer, logger, get_month_id
from outlook_report_sender import send_outlook_email
from services.capslock_checker import capslock_checking
from services.duration_counter import start_counter, stop_counter, get_duration_result
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

pyautogui.FAILSAFE = False
CONFIG = load_config()
keyboard = Controller()


class ReportProcessor:
    def __init__(self, report_config: Dict):
        """
        INITIALIZE REPORT PROCESSOR WITH CONFIGURATION
        - report_type (str): TYPE OF REPORT (TOD, AR, WCM, ETC)
        - source_file (str): PATH TO SOURCE EXCEL FILE
        - submission_folder (str): FOLDER FOR OUTPUT FILES
        - recipients (List[str]): PRIMARY EMAIL RECIPIENTS
        - cc_recipients (Optional[List[str]]): CC EMAIL RECIPIENTS
        - subject_template (str): EMAIL SUBJECT TEMPLATE
        - body_template (str): EMAIL BODY TEMPLATE
        - custom_processing (Optional[Callable]): CUSTOM PROCESSING FUNCTION
        """
        self.report_type = report_config.get("report_type", "UNKNOWN")
        self.source_file = report_config.get("source_file")
        self.submission_folder = report_config.get("submission_folder")
        self.recipients = report_config.get("recipients", [])
        self.cc_recipients = report_config.get("cc_recipients", [])
        self.subject_template = report_config.get("subject_template", "")
        self.body_template = report_config.get("body_template", "")
        self.custom_processing = report_config.get("custom_processing", None)
        self.filename_template = report_config.get("filename_template", "Report_{date}")
        
        logger.info(f"[SYSTEM] INITIALIZE {self.report_type} REPORT PROCESSOR")

    # SYSTEM ENVIRONMENT FOR REPORT PROCESSING
    def prepare_environment(self):
        logger.info(f"[SYSTEM] PREPARE ENVIRONMENT FOR {self.report_type}")
        
        capslock_checking()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        
        find_screen_keeper_process()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        
        stop_screen_keeper()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # CLEARING PATH SUBMISSION FOLDER
    def clear_submission_folder(self):
        logger.info(f"[SYSTEM] CLEAR PATH FOLDER : {self.submission_folder}")
        clear_submission_folder(target_folder=self.submission_folder)
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # OPEN REPORT REPORT SOURCE FILE
    def open_source_file(self):
        logger.info(f"[SYSTEM] OPEN REPORT WORKBOOK : {self.source_file}")
        
        if not os.path.exists(self.source_file):
            raise FileNotFoundError(f"REPORT FILE NOT FOUND : {self.source_file}")
        
        os.startfile(self.source_file)
        wait_timer(CONFIG["WAIT_TIME"]["THIRTY_SECOND"])
        maximize_app_window()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

    # REFRESH DATA IN WORKBOOK
    def refresh_data(self):
        logger.info(f"[DATA] REFRESH DATA CONNECTIONS")
        
        switch_to_first_cells()
        move_cell_horizontal()
        
        refresh_excel_data()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_MINUTE"])
        
        move_cell_horizontal()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
        entering_operation()

    def process_excel_standard(self):
        logger.info(f"[DATA] EXECUTE SPPI EXCEL WORKFLOW")
        
        switch_to_first_cells()
        switch_to_right_sheet()
        switch_to_first_cells()
        
        select_sheet_down()
        move_or_copy_menu()
        move_or_copy_as_newbook()
        wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
        
        switch_to_first_sheet()
        break_excel_link()
        switch_to_first_cells()
        switch_to_table_cells()
        capture_table_as_picture()
        switch_to_first_cells()

    def save_report_file(self, filename: str):
        logger.info(f"[DATA] SAVE REPORT FILE IN : {filename}")
        
        save_new_book()
        pyautogui.write(self.submission_folder)
        confirm()
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])
        
        set_new_book_name()
        pyautogui.write(filename, interval=0.05)
        confirm()
        wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
        
        closing_tab()
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    def close_source_file(self):
        logger.info(f"[SYSTEM] CLOSE SOURCE FILE")
        
        switch_to_first_cells()
        switch_to_first_sheet()
        switch_to_first_cells()
        switch_to_right_sheet()
        
        save_file()
        wait_timer(CONFIG["WAIT_TIME"]["TWENTY_SECOND"])
        closing_tab()
        wait_timer(CONFIG["WAIT_TIME"]["THREE_SECOND"])

    def generate_filename(self, date_offset: int = -1) -> str:
        target_date = datetime.now() + timedelta(days=date_offset)
        day = target_date.strftime("%d")
        year = target_date.strftime("%Y")
        month_eng = target_date.strftime("%B")
        month_idn_title = get_month_id(month_eng, case="title")
        month_idn_upper = get_month_id(month_eng, case="upper")
        
        filename = self.filename_template.format(
            date=f"{day} {month_idn_title}",
            day=day,
            month=month_idn_title,
            month_upper=month_idn_upper,
            year=year,
            report_type=self.report_type
        )
        
        return filename

    def generate_email_content(self, date_offset: int = -1) -> Dict[str, str]:
        """
        Args:
            date_offset (int): DAYS OFFSET FROM TODAY
        
        Returns:
            Dict[str, str]: DICT CONTAINING 'subject' AND 'body'
        """
        target_date = datetime.now() + timedelta(days=date_offset)
        
        day = target_date.strftime("%d")
        year = target_date.strftime("%Y")
        month_eng = target_date.strftime("%B")
        month_idn_title = get_month_id(month_eng, case="title")
        month_idn_upper = get_month_id(month_eng, case="upper")
        
        subject = self.subject_template.format(
            day=day,
            month=month_idn_title,
            year=year,
            report_type=self.report_type
        )
        
        body = self.body_template.format(
            day=day,
            month=month_idn_title,
            year=year,
            report_type=self.report_type
        )
        
        return {"subject": subject, "body": body}

    def process_report(self):
        logger.info(f"[SYSTEM] START {self.report_type} REPORT PROCESSING")
        
        self.open_source_file()
        self.refresh_data()
        
        if self.custom_processing:
            logger.info(f"[SYSTEM] EXECUTE CUSTOM PROCESSING")
            self.custom_processing()
        else:
            self.process_excel_standard()
        
        filename = self.generate_filename()
        self.save_report_file(filename)
        self.close_source_file()
        
        logger.info(f"[SYSTEM] {self.report_type} REPORT PROCESSING COMPLETE")

    def send_email(self):
        logger.info(f"[SYSTEM] SEND {self.report_type} REPORT EMAIL")
        
        email_content = self.generate_email_content()
        
        footer_template = """
    

Hormat kami,
Asset Management Division
Collection HO - PT Suzuki Finance Indonesia
"""
        
        send_outlook_email(
            outlook_recipients=self.recipients,
            secondary_recipients=self.cc_recipients,
            subject_email=email_content["subject"],
            core_email=email_content["body"],
            footer_template=footer_template,
            submission_folder=self.submission_folder
        )
        
        logger.info(f"[SYSTEM] {self.report_type} REPORT EMAIL SENT")

    def execute(self):
        logger.info(f"[SYSTEM] EXECUTE {self.report_type} REPORT WORKFLOW")
        start_counter()
        
        try:
            self.prepare_environment()
            self.clear_submission_folder()
            self.process_report()
            self.send_email()
            
            stop_counter()
            execution_time = get_duration_result()
            logger.info(f"[SYSTEM] {self.report_type} EXECUTION TIME: {execution_time}")
            
        except Exception as e:
            logger.error(f"[ERROR] {self.report_type} REPORT FAILED: {e}")
            raise
        
        finally:
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])
            logger.warning("[SYSTEM] RESTART SCREEN KEEPER")
            run_screen_keeper()


def create_tod_report_config() -> Dict:
    return {
        "report_type": "TOD",
        "source_file": CONFIG["WORKSOURCE_TOD"],
        "submission_folder": CONFIG["SUBMISSION_TOD"],
        "recipients": ["asset.mgmt@sfi.co.id"],
        "cc_recipients": ["collho.3@sfi.co.id"],
        "subject_template": "Summary Performance AR & TOD | {day} {month} {year}",
        "body_template": """Dear All,

Dengan hormat,

Berikut terlampir Summary Performance AR & TOD {day} {month} {year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

""",
        "filename_template": "Summary Performance TOD {date}",
        "custom_processing": None
    }


def create_wcm_report_config() -> Dict:
    """
    CREATE WCM REPORT CONFIGURATION
    
    Returns:
        Dict: WCM REPORT CONFIGURATION
    """
    return {
        "report_type": "WCM",
        "source_file": CONFIG.get("WORKSOURCE_WCM", ""),
        "submission_folder": CONFIG.get("SUBMISSION_WCM", ""),
        "recipients": ["wcm.team@sfi.co.id"],
        "cc_recipients": ["collho.3@sfi.co.id"],
        "subject_template": "Summary Working Capital Management | {day} {month} {year}",
        "body_template": """Dear All,

Dengan hormat,

Berikut terlampir Summary Working Capital Management {day} {month} {year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

""",
        "filename_template": "Summary WCM {date}",
        "custom_processing": None
    }


def create_ar_report_config() -> Dict:
    """
    CREATE AR REPORT CONFIGURATION
    
    Returns:
        Dict: AR REPORT CONFIGURATION
    """
    return {
        "report_type": "AR",
        "source_file": CONFIG.get("WORKSOURCE_AR", ""),
        "submission_folder": CONFIG.get("SUBMISSION_AR", ""),
        "recipients": ["ar.team@sfi.co.id"],
        "cc_recipients": ["collho.3@sfi.co.id"],
        "subject_template": "Summary Account Receivable | {day} {month} {year}",
        "body_template": """Dear All,

Dengan hormat,

Berikut terlampir Summary Account Receivable {day} {month} {year}

Catatan
- Laporan ini dihasilkan secara otomatis dan disusun oleh sistem.
Seluruh data harap diperhatikan dan dievaluasi kembali.

""",
        "filename_template": "Summary AR {date}",
        "custom_processing": None
    }


if __name__ == "__main__":
    # EXAMPLE: EXECUTE TOD REPORT
    tod_config = create_tod_report_config()
    tod_processor = ReportProcessor(tod_config)
    tod_processor.execute()
    
    # EXAMPLE: EXECUTE WCM REPORT
    wcm_config = create_wcm_report_config()
    wcm_processor = ReportProcessor(wcm_config)
    wcm_processor.execute()
    
    # EXAMPLE: EXECUTE AR REPORT
    # ar_config = create_ar_report_config()
    # ar_processor = ReportProcessor(ar_config)
    # ar_processor.execute()