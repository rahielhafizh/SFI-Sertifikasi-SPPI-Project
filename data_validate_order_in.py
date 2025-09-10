import os
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List
from dataclasses import dataclass
from services.config import load_config, logger


class ORDERValidationError(Exception):
    pass


class ORDERFileError(ORDERValidationError):
    pass


ORDER_COLUMNS = {
    "last_month": ["D", "E", "F"],
    "this_month": ["G", "H", "I"],
    "diff": ["J", "K", "L"],
}

ORDER_GROUPS = {"D-E-F": "DATA BULAN LALU", "G-H-I": "DATA BULAN INI", "J-K-L": "DIFF"}

CONFIG = load_config()


@dataclass
class ValidationResult:
    row_number: int
    reference_value: str
    column_category: str
    missing_columns: List[str]
    is_valid: bool

    @property
    def column_range(self) -> str:
        return "-".join(ORDER_COLUMNS.get(self.column_category, []))


@dataclass
class ValidationReport:
    results: List[ValidationResult]
    timestamp: datetime = datetime.now()

    @property
    def has_errors(self) -> bool:
        return any(not r.is_valid for r in self.results)

    @property
    def error_results(self) -> List[ValidationResult]:
        return [r for r in self.results if not r.is_valid]


class ExcelReader:
    def __init__(self, file_path: str, sheet_name: str = "SUMMARY"):
        self.file_path = Path(file_path)
        self.sheet_name = sheet_name

    def read_sheet(self) -> pd.DataFrame:
        if not self.file_path.exists():
            logger.error(f"[ERROR] FILE NOT FOUND: {self.file_path}")
            raise ORDERFileError(f"File not found: {self.file_path}")
        logger.info(f"[DATA] READING EXCEL FILE: {self.file_path}")
        return pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=None)


class DataValidator:
    def __init__(self, excel_reader: ExcelReader):
        self.excel_reader = excel_reader

    def _excel_col_to_index(self, col_name: str) -> int:
        result = 0
        for char in col_name.upper():
            result = result * 26 + (ord(char) - ord("A") + 1)
        return result - 1

    def _is_cell_empty(self, value) -> bool:
        return pd.isna(value) or (isinstance(value, str) and value.strip() == "")

    def _get_reference_value(self, df: pd.DataFrame, row_number: int) -> str:
        row_idx = row_number - 1
        if row_idx >= len(df):
            return f"ROW_{row_number}_NOT_FOUND"
        value = df.iloc[row_idx, 0]
        return str(value) if not pd.isna(value) else f"EMPTY_A{row_number}"

    def _validate_column_range(
        self,
        df: pd.DataFrame,
        row_number: int,
        column_letters: List[str],
        category: str,
    ) -> ValidationResult:
        row_idx = row_number - 1
        reference_value = self._get_reference_value(df, row_number)
        missing_columns = []

        if row_idx >= len(df):
            return ValidationResult(
                row_number=row_number,
                reference_value=reference_value,
                column_category=category,
                missing_columns=column_letters,
                is_valid=False,
            )

        for col_letter in column_letters:
            col_idx = self._excel_col_to_index(col_letter)
            if col_idx >= len(df.columns):
                missing_columns.append(col_letter)
                continue
            cell_value = df.iloc[row_idx, col_idx]
            if self._is_cell_empty(cell_value):
                missing_columns.append(col_letter)

        return ValidationResult(
            row_number=row_number,
            reference_value=reference_value,
            column_category=category,
            missing_columns=missing_columns,
            is_valid=len(missing_columns) == 0,
        )

    def validate_all_rows(self, row_numbers: List[int]) -> ValidationReport:
        logger.info("[DATA] STARTING VALIDATION PROCESS")
        df = self.excel_reader.read_sheet()
        results = []

        for row_number in row_numbers:
            for category, columns in ORDER_COLUMNS.items():
                results.append(
                    self._validate_column_range(df, row_number, columns, category)
                )

        logger.info("[DATA] VALIDATION COMPLETED")
        return ValidationReport(results=results)


class ORDERValidator:
    def __init__(self, file_path: str):
        if not file_path:
            raise ORDERFileError("FILE PATH NOT FOUND")
        self.file_path = file_path
        self.excel_reader = ExcelReader(file_path)
        self.data_validator = DataValidator(self.excel_reader)


def validate_order_in_data(file_path: str, validation_rows: List[int] = [22]) -> bool:
    if not file_path:
        logger.error("[ERROR] FILE PATH CANNOT BE EMPTY")
        return False

    try:
        validator = ORDERValidator(file_path)
        report = validator.data_validator.validate_all_rows(validation_rows)

        if report.has_errors:
            logger.warning("[VALIDATION] DATA INCOMPLETE - MISSING VALUES DETECTED")
            for result in report.error_results:
                logger.warning(
                    f"[VALIDATION] ROW {result.row_number} ({result.reference_value}): "
                    f"MISSING {', '.join(result.missing_columns)} IN {result.column_category}"
                )
            return False

        logger.info("[VALIDATION] DATA COMPLETE - ALL REQUIRED VALUES PRESENT")
        return True

    except Exception as e:
        logger.error(f"[ERROR] VALIDATION FAILED: {str(e)}")
        return False


def main():
    logger.info("[SYSTEM] STARTING ORDER IN VALIDATION SCRIPT")
    source_file = CONFIG.get("WORKSOURCE_ORDER_IN")

    if not source_file:
        logger.error("[SYSTEM] NO SOURCE FILE CONFIGURED")
        return False

    validation_success = validate_order_in_data(source_file)

    if validation_success:
        logger.info("[SYSTEM] ORDER IN DATA VALIDATION COMPLETED - DATA IS COMPLETE")
    else:
        logger.warning(
            "[SYSTEM] ORDER IN DATA VALIDATION COMPLETED - DATA IS INCOMPLETE"
        )

    return validation_success


if __name__ == "__main__":
    main()
