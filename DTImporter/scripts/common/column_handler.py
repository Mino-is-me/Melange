from typing import List, Dict, Set
import unreal

class ColumnHandler:
    def __init__(self, table_name):
        self.table_name = table_name
        self.required_columns = []
        self.handled_columns = set()

    def set_required_columns(self, columns):
        self.required_columns = columns
        self.handled_columns.update(columns)

    def add_handled_columns(self, columns):
        self.handled_columns.update(columns)

    def process_columns(self, data):
        if not data:
            return {'success': False, 'message': '데이터가 비어있습니다.'}

        # 데이터의 컬럼 목록 가져오기
        columns = data[0].keys() if data else []

        # 필수 컬럼 체크
        missing_columns = [col for col in self.required_columns if col not in columns]
        if missing_columns:
            message = f"{self.table_name} 시트에서 다음 필수 컬럼이 누락되었습니다:\n"
            message += "\n".join([f"- {col}" for col in missing_columns])
            return {'success': False, 'message': message}

        # 처리되지 않는 컬럼 체크
        unhandled_columns = [col for col in columns if col not in self.handled_columns]
        if unhandled_columns:
            print(f"경고: {self.table_name} 시트에서 다음 컬럼은 처리되지 않습니다:")
            print("\n".join([f"- {col}" for col in unhandled_columns]))

        return {'success': True, 'message': ''}

    def add_handled_column(self, column: str):
        """처리된 컬럼 추가"""
        self.handled_columns.add(column)

    def add_handled_columns(self, columns: List[str]):
        """여러 처리된 컬럼 추가"""
        self.handled_columns.update(columns)