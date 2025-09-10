import os
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass
from services.config import load_config, logger

CONFIG = load_config()


class ExcelConfig:
    TARGET_SHEET_NAME = "TABLE"
    DATETIME_CELLS = {"K2": "K-2"}


@dataclass
class DateTimeValidationResult:
    cell_address: str
    expected_date: datetime
    actual_value: str
    is_valid: bool
    error_message: str = ""


class PicDateTimeValidatorMail:
    def __init__(self, CONFIG: Dict):
        self.CONFIG = CONFIG

    def get_expected_date(self) -> datetime:
        today = datetime.now().date()
        return datetime.combine(today, datetime.min.time())

    def load_pic_sheet(self, file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"EXCEL FILE NOT FOUND: {file_path}")

        try:
            return pd.read_excel(
                file_path, sheet_name=ExcelConfig.TARGET_SHEET_NAME, header=None
            )

        except ValueError as e:
            if "Worksheet named" in str(e):
                raise pd.errors.ExcelFileError(
                    f"SHEET '{ExcelConfig.TARGET_SHEET_NAME}' NOT FOUND IN FILE"
                )
            raise

        except Exception as e:
            raise pd.errors.ExcelFileError(f"FAILED TO READ EXCEL FILE: {e}")

    def excel_col_to_index(self, col_name: str) -> int:
        result = 0
        for char in col_name:
            result = result * 26 + (ord(char.upper()) - ord("A") + 1)
        return result - 1

    def parse_cell_value_as_datetime(self, value) -> Optional[datetime]:
        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value

        if hasattr(value, "to_pydatetime"):
            return value.to_pydatetime()

        if isinstance(value, str):
            datetime_formats = [
                "%d/%m/%Y %H:%M:%S",
                "%d/%m/%Y  %H:%M:%S",
                "%Y-%m-%d %H:%M:%S",
                "%d-%m-%Y %H:%M:%S",
                "%m/%d/%Y %H:%M:%S",
                "%d/%m/%Y %H:%M",
                "%Y-%m-%d %H:%M",
                "%d-%m-%Y %H:%M",
                "%m/%d/%Y %H:%M",
                "%d/%m/%Y",
                "%Y-%m-%d",
                "%d-%m-%Y",
                "%m/%d/%Y",
            ]
            for fmt in datetime_formats:
                try:
                    return datetime.strptime(value.strip(), fmt)
                except ValueError:
                    continue

        if isinstance(value, (int, float)):
            try:
                excel_epoch = datetime(1900, 1, 1)
                value = float(value) - (2 if value > 59 else 1)
                return excel_epoch + timedelta(days=value)
            except (ValueError, OverflowError):
                pass

        return None

    def validate_cell_datetime(
        self, df: pd.DataFrame, cell_address: str, expected_date: datetime
    ) -> DateTimeValidationResult:
        try:
            col_part = "".join(filter(str.isalpha, cell_address))
            row_part = "".join(filter(str.isdigit, cell_address))
            col_idx = self.excel_col_to_index(col_part)
            row_idx = int(row_part) - 1

            if row_idx >= len(df) or col_idx >= len(df.columns):
                return DateTimeValidationResult(
                    cell_address,
                    expected_date,
                    "NOT_FOUND",
                    False,
                    f"CELL {cell_address} NOT FOUND",
                )

            cell_value = df.iloc[row_idx, col_idx]
            actual_datetime = self.parse_cell_value_as_datetime(cell_value)
            actual_value_str = (
                actual_datetime.strftime("%d/%m/%Y %H:%M:%S")
                if actual_datetime
                else (str(cell_value) if not pd.isna(cell_value) else "EMPTY")
            )

            if not actual_datetime:
                return DateTimeValidationResult(
                    cell_address,
                    expected_date,
                    actual_value_str,
                    False,
                    f"INVALID DATETIME IN {cell_address}",
                )

            is_valid = actual_datetime.date() == expected_date.date()
            return DateTimeValidationResult(
                cell_address,
                expected_date,
                actual_value_str,
                is_valid,
                (
                    ""
                    if is_valid
                    else f"DATE MISMATCH IN {cell_address} - NOT TODAY'S DATE"
                ),
            )

        except Exception as e:
            return DateTimeValidationResult(
                cell_address,
                expected_date,
                "ERROR",
                False,
                f"ERROR VALIDATING {cell_address}: {e}",
            )

    def validate_pic_datetime(self, file_path: str) -> List[DateTimeValidationResult]:
        df = self.load_pic_sheet(file_path)
        expected_date = self.get_expected_date()
        cell_address = "K2"
        result = self.validate_cell_datetime(df, cell_address, expected_date)
        if result.is_valid:
            logger.info(
                f"[DATA] CELL {cell_address} VALIDATED SUCCESSFULLY | VALUE: {result.actual_value}"
            )

        else:
            logger.error(f"[ERROR] {result.error_message}")
        return [result]

    def is_data_valid(self, validation_results: List[DateTimeValidationResult]) -> bool:
        return all(result.is_valid for result in validation_results)


def validate_pic_data_for_email(file_path: Optional[str] = None) -> bool:
    try:
        target_file = file_path or CONFIG["WORKSOURCE_PIC"]

        logger.info(
            f"[SYSTEM] STARTING PIC DATETIME VALIDATION FOR EMAIL: {target_file}"
        )

        if not os.path.exists(target_file):
            logger.error(f"[ERROR] EXCEL FILE NOT FOUND: {target_file}")
            return False

        validator = PicDateTimeValidatorMail(CONFIG)
        validation_results = validator.validate_pic_datetime(target_file)
        is_valid = validator.is_data_valid(validation_results)
        if is_valid:
            logger.info("[DATA] PIC DATETIME VALIDATION PASSED - EMAIL CAN BE SENT")
            return True

        for result in validation_results:
            if not result.is_valid:
                logger.warning(
                    f"[VALIDATION] {result.error_message} | "
                    f"EXPECTED: TODAY ({result.expected_date.strftime('%d/%m/%Y')}) | "
                    f"ACTUAL: {result.actual_value}"
                )
        return False

    except Exception as e:
        logger.error(f"[ERROR] PIC DATETIME VALIDATION ERROR FOR EMAIL: {e}")
        return False


def validate_pic_file_for_email(file_path: str) -> bool:
    if not file_path:
        logger.error("[ERROR] FILE PATH CANNOT BE EMPTY")
        return False

    if not os.path.exists(file_path):
        logger.error(f"[ERROR] FILE NOT FOUND: {file_path}")
        return False

    logger.info(f"[SYSTEM] VALIDATING PIC FILE: {file_path}")
    return validate_pic_data_for_email(file_path)


def get_pic_validation_details(file_path: Optional[str] = None) -> Dict:
    try:
        target_file = file_path or CONFIG["WORKSOURCE_PIC"]
        validator = PicDateTimeValidatorMail(CONFIG)
        validation_results = validator.validate_pic_datetime(target_file)
        details = {
            "file_path": target_file,
            "validation_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "expected_date": datetime.now().date().strftime("%d/%m/%Y"),
            "is_valid": validator.is_data_valid(validation_results),
            "results": [],
        }

        for result in validation_results:
            details["results"].append(
                {
                    "cell": result.cell_address,
                    "expected": result.expected_date.strftime("%d/%m/%Y"),
                    "actual": result.actual_value,
                    "valid": result.is_valid,
                    "error": result.error_message,
                }
            )
        return details

    except Exception as e:
        return {
            "file_path": target_file if "target_file" in locals() else "UNKNOWN",
            "validation_time": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "error": str(e),
            "is_valid": False,
        }


def main():
    source_validation = validate_pic_data_for_email()
    return source_validation


if __name__ == "__main__":
    main()
