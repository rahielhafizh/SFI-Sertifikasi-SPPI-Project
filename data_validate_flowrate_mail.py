import os
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Union
from dataclasses import dataclass
import pandas as pd
from dateutil import parser as date_parser
from services.config import load_config, logger

DEFAULT_CONFIG = load_config()


@dataclass
class ValidationConfig:
    sheet_name: str = "FR-4W-OD2-Collectible"
    date_cells: Dict[str, str] = None
    submission_folder: str = ""
    worksource_flowrate: str = ""

    def __post_init__(self):
        if self.date_cells is None:
            self.date_cells = {"H3": "H-1"}


@dataclass
class DateValidationResult:
    cell_address: str
    expected_date: datetime
    actual_value: str
    is_valid: bool
    error_message: str = ""
    error_type: str = "NONE"


class FlowrateDateValidatorError(Exception):
    pass


class FlowrateDateValidator:
    EXCEL_EPOCH_1900 = datetime(1900, 1, 1)
    EXCEL_LEAP_YEAR_BUG_THRESHOLD = 59

    def __init__(self, config: Optional[ValidationConfig] = None):
        self.config = config or ValidationConfig(
            submission_folder=DEFAULT_CONFIG.get("SUBMISSION_FLOWRATE", ""),
            worksource_flowrate=DEFAULT_CONFIG.get("WORKSOURCE_FLOWRATE", ""),
        )

    def get_expected_dates(
        self, reference_date: Optional[datetime] = None
    ) -> Dict[str, datetime]:
        if reference_date is None:
            reference_date = datetime.now()
        yesterday = reference_date.date() - timedelta(days=1)
        return {
            cell: datetime.combine(yesterday, datetime.min.time())
            for cell in self.config.date_cells
        }

    def load_excel_sheet(self, file_path: Union[str, Path]) -> pd.DataFrame:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FlowrateDateValidatorError(f"FILE NOT FOUND | {file_path}")

        if file_path.suffix.lower() not in [".xlsx", ".xls"]:
            raise FlowrateDateValidatorError(f"BAD FORMAT | {file_path.suffix}")

        try:
            return pd.read_excel(
                file_path, sheet_name=self.config.sheet_name, header=None
            )

        except ValueError as e:
            if "Worksheet named" in str(e):
                raise FlowrateDateValidatorError(
                    f"SHEET NOT FOUND | {self.config.sheet_name}"
                ) from e
            raise

        except PermissionError as e:
            raise FlowrateDateValidatorError(f"PERMISSION DENIED | {file_path}") from e

        except Exception as e:
            raise FlowrateDateValidatorError(f"READ ERROR | {e}") from e

    @staticmethod
    def excel_col_to_index(col_name: str) -> int:
        result = 0
        for char in col_name.upper():
            if not char.isalpha():
                raise ValueError(f"BAD COLUMN | {col_name}")
            result = result * 26 + (ord(char) - ord("A") + 1)
        return result - 1

    def parse_cell_value_as_date(self, value) -> Optional[datetime]:
        if pd.isna(value):
            return None

        if isinstance(value, datetime):
            return value

        if hasattr(value, "to_pydatetime"):
            try:
                return value.to_pydatetime()
            except Exception:
                return

        if isinstance(value, str):
            try:
                return date_parser.parse(value.strip(), dayfirst=True)
            except Exception:
                return None

        if isinstance(value, (int, float)):
            try:
                excel_serial = int(value)
                if excel_serial <= 0:
                    return None
                excel_serial -= (
                    2 if excel_serial > self.EXCEL_LEAP_YEAR_BUG_THRESHOLD else 1
                )
                return self.EXCEL_EPOCH_1900 + timedelta(days=excel_serial)
            except Exception:
                return None
        return None

    def parse_cell_address(self, cell_address: str) -> tuple[int, int]:
        col_part = "".join(filter(str.isalpha, cell_address))
        row_part = "".join(filter(str.isdigit, cell_address))
        if not col_part or not row_part:
            raise ValueError(f"BAD CELL ADDRESS | {cell_address}")
        return int(row_part) - 1, self.excel_col_to_index(col_part)

    def validate_cell_date(
        self, df: pd.DataFrame, cell_address: str, expected_date: datetime
    ) -> DateValidationResult:
        try:
            row_idx, col_idx = self.parse_cell_address(cell_address)
            if row_idx >= len(df) or col_idx >= len(df.columns):
                return DateValidationResult(
                    cell_address,
                    expected_date,
                    "NOT_FOUND",
                    False,
                    "CELL OUTSIDE SHEET",
                    "NOT_FOUND",
                )

            cell_value = df.iloc[row_idx, col_idx]
            actual_date = self.parse_cell_value_as_date(cell_value)
            actual_value_str = (
                actual_date.strftime("%d/%m/%Y")
                if actual_date
                else ("EMPTY" if pd.isna(cell_value) else str(cell_value))
            )

            if not actual_date:
                return DateValidationResult(
                    cell_address,
                    expected_date,
                    actual_value_str,
                    False,
                    "INVALID DATE",
                    "INVALID_DATE",
                )

            is_valid = actual_date.date() == expected_date.date()
            return DateValidationResult(
                cell_address,
                expected_date,
                actual_value_str,
                is_valid,
                (
                    ""
                    if is_valid
                    else f"EXPECTED {expected_date.strftime('%d/%m/%Y')} GOT {actual_value_str}"
                ),
                "NONE" if is_valid else "DATE_MISMATCH",
            )

        except Exception as e:
            return DateValidationResult(
                cell_address,
                expected_date,
                "ERROR",
                False,
                f"PARSE ERROR | {e}",
                "PARSE_ERROR",
            )

    def validate_file(
        self, file_path: Union[str, Path], reference_date: Optional[datetime] = None
    ) -> List[DateValidationResult]:
        df = self.load_excel_sheet(file_path)
        expected_dates = self.get_expected_dates(reference_date)
        results = []

        for cell_address in self.config.date_cells:
            result = self.validate_cell_date(
                df, cell_address, expected_dates[cell_address]
            )
            results.append(result)

            if result.is_valid:
                logger.info(f"VALIDATION {cell_address} OK | {result.actual_value}")
            else:
                logger.warning(
                    f"VALIDATION {cell_address} FAIL | {result.error_message}"
                )
        return results

    def is_validation_successful(self, results: List[DateValidationResult]) -> bool:
        return all(result.is_valid for result in results)

    def find_latest_flowrate_file(self) -> Optional[Path]:
        if not self.config.submission_folder:
            return None

        submission_path = Path(self.config.submission_folder)
        if not submission_path.exists():
            return None

        flowrate_files = list(submission_path.glob("*FLOWRATE*.xls*"))
        return (
            max(flowrate_files, key=lambda f: f.stat().st_mtime)
            if flowrate_files
            else None
        )

    def build_flowrate_file_path(self, timestamp: str) -> Path:
        if not self.config.submission_folder:
            raise FlowrateDateValidatorError("NO SUBMISSION FOLDER")

        return (
            Path(self.config.submission_folder)
            / f"REPORT SUMMARY FLOWRATE {timestamp}.xlsx"
        )


def validate_flowrate_file(file_path, config=None, reference_date=None) -> bool:
    try:
        validator = FlowrateDateValidator(config)
        results = validator.validate_file(file_path, reference_date)
        return validator.is_validation_successful(results)

    except Exception as e:
        logger.error(f"VALIDATION FAIL | {e}")
        return False


def validate_default_flowrate_source(config=None, reference_date=None) -> bool:
    worksource_path = DEFAULT_CONFIG.get("WORKSOURCE_FLOWRATE")
    return (
        validate_flowrate_file(worksource_path, config, reference_date)
        if worksource_path
        else False
    )


def validate_latest_flowrate_report(
    file_path=None, config=None, reference_date=None
) -> bool:
    if file_path:
        return validate_flowrate_file(file_path, config, reference_date)

    else:
        validator = FlowrateDateValidator(config)
        latest_file = validator.find_latest_flowrate_file()
        return (
            validate_flowrate_file(latest_file, config, reference_date)
            if latest_file
            else False
        )


def validate_flowrate_by_timestamp(timestamp, config=None, reference_date=None) -> bool:
    try:
        validator = FlowrateDateValidator(config)
        return validate_flowrate_file(
            validator.build_flowrate_file_path(timestamp), config, reference_date
        )

    except Exception as e:
        logger.error(f"TIMESTAMP FAIL | {e}")
        return False


def main():
    logger.info("[SYSTEM] VALIDATING FLOWRATE DATE")
    results = [
        ("SOURCE", validate_default_flowrate_source()),
        ("LATEST", validate_latest_flowrate_report()),
    ]

    for name, result in results:
        logger.info(f"{name} | {'PASS' if result else 'FAIL'}")
    overall = all(r for _, r in results)
    logger.info(f"OVERALL | {'PASS' if overall else 'FAIL'}")
    return overall


if __name__ == "__main__":
    main()
