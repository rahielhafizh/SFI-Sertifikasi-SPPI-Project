import os
import pandas as pd
import pyperclip
from general_task import *
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Protocol
from services.capslock_checker import capslock_checking
from services.config import load_config, wait_timer, logger
from services.remover_flowrate import clear_submission_folder
from services.whatsapp_sender import send_paste_report, send_to_group
from data_build_flowrate import excel_config
from screen_keeper import (
    find_screen_keeper_process,
    stop_screen_keeper,
    run_screen_keeper,
)

CONFIG = load_config()


class ExcelConfig:
    TARGET_SHEET_NAME = "FR-4W-OD2-Collectible"
    DATE_CELLS = {"H3": "H-1"}


@dataclass
class DateValidationResult:
    cell_address: str
    expected_date: datetime
    actual_value: str
    is_valid: bool
    error_message: str = ""


class NotificationService(Protocol):
    def send_report(self, message: str, recipients: List[str]) -> bool: ...


class WhatsAppNotificationService:
    def send_report(self, message: str, recipients: List[str]) -> bool:
        try:
            pyperclip.copy(message)
            group_link = CONFIG["ASSET_GROUP"]

            if group_link:
                result = send_to_group(group_link, message)
                if result:
                    logger.info("[DATA] REPORT SENT TO GROUP")
                    return True
                else:
                    logger.error("[ERROR] FAILED TO SEND REPORT TO GROUP")
                    return False
            else:
                logger.warning("[WARNING] GROUP NOT FOUND")
                all_sent = True

                for recipient in recipients:
                    result = send_paste_report(recipient, message)

                    if result:
                        logger.info(f"[DATA] REPORT SENT TO {recipient}")
                    else:
                        logger.error(f"[ERROR] FAILED TO SEND REPORT TO {recipient}")
                        all_sent = False

                    wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

                return all_sent

        except Exception as e:
            logger.error(f"[ERROR] EXCEPTION WHILE SENDING REPORT: {e}")
            return False


class FlowrateDateValidator:
    def __init__(
        self, CONFIG: Dict, notification_service: Optional[NotificationService] = None
    ):
        self.CONFIG = CONFIG
        self.notification_service = (
            notification_service or WhatsAppNotificationService()
        )

    def get_expected_dates(self) -> Dict[str, datetime]:
        yesterday = datetime.now().date() - timedelta(days=1)
        return {"H3": datetime.combine(yesterday, datetime.min.time())}

    def get_notification_recipients(self) -> List[str]:
        candidate_keys = [
            "PERSONAL_ONE",
            "PERSONAL_TWO",
            "PERSONAL_THREE",
            "PERSONAL_FOUR",
            "PERSONAL_FIVE",
        ]
        fallback_keys = ["ADMIN_PRIMARY"]
        contact_info = self.CONFIG.get("CONTACT_INFO", {})
        recipients: List[str] = [
            contact_info.get(k)
            for k in candidate_keys
            if k in contact_info and contact_info.get(k)
        ]

        if not recipients:
            recipients = [
                contact_info.get(k)
                for k in fallback_keys
                if k in contact_info and contact_info.get(k)
            ]

        recipients = [r for r in recipients if r]
        return recipients

    def load_flowrate_sheet(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"EXCEL FILE NOT FOUND: {file_path}")

        try:
            return pd.read_excel(
                file_path, sheet_name=ExcelConfig.TARGET_SHEET_NAME, header=None
            )
        except ValueError as e:
            if "does not exist" in str(e):
                raise ValueError(
                    f"SHEET '{ExcelConfig.TARGET_SHEET_NAME}' NOT FOUND: {file_path}"
                )
            raise
        except Exception as e:
            raise RuntimeError(f"FAILED TO READ EXCEL FILE: {e}")

    def excel_col_to_index(self, col_name: str) -> int:
        result = 0
        for char in col_name:
            result = result * 26 + (ord(char.upper()) - ord("A") + 1)
        return result - 1

    def parse_cell_value_as_date(self, value) -> Optional[datetime]:
        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value

        if hasattr(value, "to_pydatetime"):
            return value.to_pydatetime()

        if isinstance(value, str):
            s = value.strip()
            for fmt in ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"]:
                try:
                    return datetime.strptime(s, fmt)
                except ValueError:
                    continue

        if isinstance(value, (int, float)):
            from datetime import date

            excel_epoch = date(1900, 1, 1)
            serial = int(value)
            serial_adjusted = serial - (2 if serial > 59 else 1)
            return datetime.combine(
                excel_epoch + timedelta(days=serial_adjusted), datetime.min.time()
            )

        return None

    def validate_cell_date(
        self, df: pd.DataFrame, cell_address: str, expected_date: datetime
    ) -> DateValidationResult:
        try:
            col_part = "".join(filter(str.isalpha, cell_address))
            row_part = "".join(filter(str.isdigit, cell_address))

            col_idx = self.excel_col_to_index(col_part)
            row_idx = int(row_part) - 1

            if row_idx >= len(df) or col_idx >= len(df.columns):
                return DateValidationResult(
                    cell_address,
                    expected_date,
                    "NOT_FOUND",
                    False,
                    f"CELL {cell_address} NOT FOUND",
                )

            cell_value = df.iloc[row_idx, col_idx]
            actual_date = self.parse_cell_value_as_date(cell_value)
            actual_value_str = (
                actual_date.strftime("%d/%m/%Y")
                if actual_date
                else (str(cell_value) if not pd.isna(cell_value) else "EMPTY")
            )

            if not actual_date:
                return DateValidationResult(
                    cell_address,
                    expected_date,
                    actual_value_str,
                    False,
                    f"INVALID DATE IN {cell_address}",
                )

            is_valid = actual_date.date() == expected_date.date()
            return DateValidationResult(
                cell_address,
                expected_date,
                actual_value_str,
                is_valid,
                "" if is_valid else f"DATE MISMATCH IN {cell_address}",
            )

        except Exception as e:
            return DateValidationResult(
                cell_address,
                expected_date,
                "ERROR",
                False,
                f"ERROR VALIDATING {cell_address}: {e}",
            )

    def validate_flowrate_dates(self, file_path: str) -> List[DateValidationResult]:
        df = self.load_flowrate_sheet(file_path)
        expected_dates = self.get_expected_dates()

        results: List[DateValidationResult] = []
        for cell_address in ExcelConfig.DATE_CELLS.keys():
            result = self.validate_cell_date(
                df, cell_address, expected_dates[cell_address]
            )

            if result.is_valid:
                logger.info(
                    f"[DATA] CELL {cell_address} VALID | VALUE: {result.actual_value}"
                )
            else:
                logger.error(
                    f"[ERROR] {result.error_message} | ACTUAL: {result.actual_value} | EXPECTED: {expected_dates[cell_address].strftime('%d/%m/%Y')}"
                )

            results.append(result)

        return results

    def format_validation_message(
        self, validation_results: List[DateValidationResult]
    ) -> str:
        invalid_results = [r for r in validation_results if not r.is_valid]
        if not invalid_results:
            return ""

        report_date_str = datetime.now().strftime("%d/%m/%Y")
        result = invalid_results[0]
        expected_date_str = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")

        return (
            f"📌 REPORT VALIDATION FR REPORT – {report_date_str}\n\n"
            f"Tanggal RunningReportDate belum diperbarui. Pada database : {result.actual_value}\n"
            f"Tanggal seharusnya diperbarui ke : {expected_date_str}\n\n"
        )

    def format_success_message(
        self, validation_results: List[DateValidationResult]
    ) -> str:
        valid_results = [r for r in validation_results if r.is_valid]
        if not valid_results:
            return ""

        report_date_str = datetime.now().strftime("%d/%m/%Y")
        result = valid_results[0]

        return (
            f"✅ REPORT VALIDATION FR REPORT – {report_date_str}\n\n"
            f"Data FR Report sudah diperbarui.\n"
            f"Tanggal RunningReportDate di database : {result.actual_value}"
        )

    def send_validation_report(
        self, validation_results: List[DateValidationResult]
    ) -> bool:
        invalid_results = [r for r in validation_results if not r.is_valid]
        valid_results = [r for r in validation_results if r.is_valid]

        recipients = self.get_notification_recipients()

        group_link = CONFIG["ASSET_GROUP"]
        if not group_link and not recipients:
            logger.error("[ERROR] NO NOTIFICATION RECIPIENTS OR GROUP FOUND")
            return False

        try:
            if invalid_results:
                error_message = self.format_validation_message(validation_results)
                result = self.notification_service.send_report(
                    error_message, recipients
                )
                if result:
                    logger.info("[DATA] FAILURE REPORT SENT")
                return result

            if valid_results:
                success_message = self.format_success_message(validation_results)
                result = self.notification_service.send_report(
                    success_message, recipients
                )
                if result:
                    logger.info("[DATA] SUCCESS REPORT SENT")
                return result

            return True

        except Exception as e:
            logger.error(f"[ERROR] FAILED TO SEND VALIDATION REPORT: {e}")
            return False

    def send_error_notification(self, error_message: str) -> None:
        try:
            recipients = self.get_notification_recipients()
            group_link = CONFIG["ASSET_GROUP"]

            if not group_link and not recipients:
                logger.error(
                    "[ERROR] NO RECIPIENTS OR GROUP AVAILABLE FOR ERROR NOTIFICATION"
                )
                return

            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = (
                f"❌ ERROR FLOWRATE VALIDATOR ❌\n\n{error_message}\n\n🕒 {timestamp}"
            )

            self.notification_service.send_report(formatted_message, recipients)
            logger.info("[DATA] ERROR NOTIFICATION SENT")

        except Exception as e:
            logger.error(f"[ERROR] FAILED TO SEND ERROR NOTIFICATION: {e}")


def validate_flowrate_data(file_path: Optional[str] = None) -> bool:
    try:
        target_file = file_path or CONFIG["WORKSOURCE_FLOWRATE"]
        logger.info("[SYSTEM] STARTING FLOWRATE DATE VALIDATION")

        if not os.path.exists(target_file):
            raise FileNotFoundError(f"EXCEL FILE NOT FOUND: {target_file}")

        validator = FlowrateDateValidator(CONFIG)
        validation_results = validator.validate_flowrate_dates(target_file)
        return validator.send_validation_report(validation_results)

    except Exception as e:
        error_msg = f"FLOWRATE VALIDATION ERROR: {e}"
        logger.error(f"[ERROR] {error_msg}")
        send_error_notification_to_admin(CONFIG, error_msg)
        return False


def send_error_notification_to_admin(CONFIG: Dict, error_message: str) -> None:
    try:
        group_link = CONFIG["ASSET_GROUP"]

        if group_link:
            timestamp = datetime.now().strftime("%H:%M:%S")
            formatted_message = f"[ERROR] {error_message} 🕒 {timestamp}"

            pyperclip.copy(formatted_message)
            send_to_group(group_link, formatted_message)
            logger.info("[DATA] ERROR NOTIFICATION SENT TO GROUP")
            return

        candidate_keys = [
            "PERSONAL_ONE",
            "PERSONAL_TWO",
            "PERSONAL_THREE",
            "PERSONAL_FOUR",
            "PERSONAL_FIVE",
            "ADMIN_PRIMARY",
        ]

        contact_info = CONFIG.get("CONTACT_INFO", {})
        recipients: List[str] = [
            contact_info.get(k)
            for k in candidate_keys
            if k in contact_info and contact_info.get(k)
        ]

        if not recipients:
            logger.error("[ERROR] NO RECIPIENTS FOUND FOR ADMIN ERROR NOTIFICATION")
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[ERROR] {error_message} 🕒 {timestamp}"

        for recipient in recipients:
            send_paste_report(recipient, formatted_message)
            wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        logger.info("[DATA] ERROR NOTIFICATION SENT")

    except Exception as e:
        logger.error(f"[ERROR] FAILED TO SEND ERROR NOTIFICATION: {e}")


def main():
    try:
        logger.info(">> INITIALIZING FLOWRATE REPORT VALIDATION")
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        capslock_checking()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        find_screen_keeper_process()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        stop_screen_keeper()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        excel_config()
        wait_timer(CONFIG["WAIT_TIME"]["ONE_SECOND"])

        logger.info("[SYSTEM] RUNNING FLOWRATE VALIDATOR")
        validation_ok = validate_flowrate_data()

        if validation_ok:
            logger.info("[DATA] FLOWRATE VALIDATION SUCCESS")
        else:
            logger.error("[ERROR] FLOWRATE VALIDATION FAILED")

    except Exception as e:
        logger.error(f"[ERROR] MAIN EXECUTION ERROR: {e}")


if __name__ == "__main__":
    main()
    wait_timer(CONFIG["WAIT_TIME"]["TWO_SECOND"])
    run_screen_keeper()
