from enum import Enum
from typing import List, Dict, Any

class ValidationErrorType(Enum):
    MISSING_COLUMN = "컬럼 누락"
    MISSING_ASSET = "필수 에셋 누락"
    DUPLICATE_VALUE = "중복 값"
    INVALID_REFERENCE = "잘못된 참조"
    INVALID_VALUE = "잘못된 값"

class ValidationError:
    def __init__(self, error_type: ValidationErrorType, sheet_name: str, column_name: str, details: str):
        self.error_type = error_type
        self.sheet_name = sheet_name
        self.column_name = column_name
        self.details = details

    def __str__(self):
        if self.error_type == ValidationErrorType.MISSING_COLUMN:
            return f"{self.sheet_name}시트에 {self.column_name} 컬럼이 존재하지 않습니다."
        elif self.error_type == ValidationErrorType.MISSING_ASSET:
            return f"{self.sheet_name}시트의 {self.column_name}컬럼은 {self.details}이라는 에셋이 반드시 존재하고 있어야 합니다."
        elif self.error_type == ValidationErrorType.DUPLICATE_VALUE:
            return f"{self.sheet_name}시트의 {self.column_name}컬럼은 유니크한 값이어야 합니다."
        elif self.error_type == ValidationErrorType.INVALID_REFERENCE:
            return f"{self.sheet_name}시트의 {self.column_name}컬럼은 {self.details}"
        elif self.error_type == ValidationErrorType.INVALID_VALUE:
            return f"{self.sheet_name}시트의 {self.column_name}컬럼: {self.details}"

class DataValidator:
    def __init__(self, sheet_name: str):
        self.sheet_name = sheet_name
        self.errors: List[ValidationError] = []

    def check_required_columns(self, data: List[Dict], required_columns: List[str]) -> bool:
        """필수 컬럼 존재 여부 확인"""
        if not data:
            return False

        actual_columns = data[0].keys()
        for column in required_columns:
            if column not in actual_columns:
                self.errors.append(ValidationError(
                    ValidationErrorType.MISSING_COLUMN,
                    self.sheet_name,
                    column,
                    ""
                ))
        return len(self.errors) == 0

    def check_unique_values(self, data: List[Dict], column: str) -> bool:
        """컬럼의 유니크 값 검사"""
        values = {}
        for row in data:
            value = row.get(column)
            if value in values:
                self.errors.append(ValidationError(
                    ValidationErrorType.DUPLICATE_VALUE,
                    self.sheet_name,
                    column,
                    f"중복된 값: {value}"
                ))
                return False
            values[value] = True
        return True

    def check_asset_exists(self, asset_path: str, column_name: str) -> bool:
        """에셋 존재 여부 확인"""
        import unreal
        if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            self.errors.append(ValidationError(
                ValidationErrorType.MISSING_ASSET,
                self.sheet_name,
                column_name,
                asset_path
            ))
            return False
        return True

    def check_reference_exists(self, value: str, reference_table: str, reference_column: str, column_name: str) -> bool:
        """다른 테이블의 컬럼 참조 확인"""
        # 참조 테이블 데이터 가져오기
        import unreal
        data_table = unreal.load_asset(reference_table)
        if not data_table:
            self.errors.append(ValidationError(
                ValidationErrorType.INVALID_REFERENCE,
                self.sheet_name,
                column_name,
                f"{reference_table} 테이블을 찾을 수 없습니다."
            ))
            return False

        # 참조 값 존재 확인
        found = False
        for row in data_table.get_row_names():
            if str(row) == value:
                found = True
                break

        if not found:
            self.errors.append(ValidationError(
                ValidationErrorType.INVALID_REFERENCE,
                self.sheet_name,
                column_name,
                f"{reference_table}의 {reference_column}에 존재하는 값이어야 합니다."
            ))
            return False
        return True

    def show_errors(self) -> bool:
        """발견된 모든 에러를 표시"""
        if not self.errors:
            return True

        import unreal
        message = "데이터 검증 오류:\n\n"
        for error in self.errors:
            message += f"- {str(error)}\n"

        unreal.EditorDialog.show_message(
            "데이터 검증 실패",
            message,
            unreal.AppMsgType.OK
        )
        return False