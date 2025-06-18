import os
import csv
import json
import tempfile
import unreal
from urllib import request, parse
from scripts.common.utils import get_sheet_data
from ..common.column_handler import ColumnHandler

# 상수 정의
SHEET_ID = "1jeq0WdGMsOcAEtW_p__-daOn22ZFoCm67UWgLh6p6CA"
GID = "301417934"
TABLE_PATH = "/Game/Core/DataTable/Maps/DT_LevelData"

# 고정 경로 매핑
FIXED_PATHS = {
    'LV_TestMap': '/Game/Maps/Development/TestMap/TestMap.TestMap',
    'LV_Test01': '/Game/CineProps/Fixed_Size/TestLevel/Test01.Test01',
    'CAM_TestMap': '/Game/Maps/Development/TestMap/TestMap_Camera.TestMap_Camera',
    'LIT_TestMap_DAY': '/Game/Maps/Development/CommonEnvironment/CommonEnvironment_Clear.CommonEnvironment_Clear',
    'BP_Test01': '/Game/CineProps/Fixed_Size/TestLevel/BP_Test01.BP_Test01'
}

class AssetPathCache:
    def __init__(self):
        self._cache = {}
        self._asset_index = {}
        self._initialized = False
        self._duplicate_assets = {}  # 중복 에셋 추적용

    def initialize(self):
        """에셋 레지스트리에서 모든 에셋을 가져와서 인덱스 생성"""
        if self._initialized:
            return

        print("에셋 인덱스 초기화 중...")
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

        # 한 번에 모든 에셋 가져오기
        ar_filter = unreal.ARFilter(
            package_paths=["/Game"],  # /Game 전체 검색
            recursive_paths=True
        )
        assets = asset_registry.get_assets(ar_filter)

        # 에셋 인덱스 생성 및 중복 검사
        for asset in assets:
            package_path = str(asset.package_name)
            package_path_lower = package_path.lower()

            path_parts = package_path_lower.split('/')
            asset_name = path_parts[-1]

            # 에셋 중복 검사
            if asset_name in self._duplicate_assets:
                self._duplicate_assets[asset_name].append(package_path)
            else:
                self._duplicate_assets[asset_name] = [package_path]

            # 에셋 이름으로 인덱싱 (대소문자 구분 없이)
            if asset_name not in self._asset_index:
                self._asset_index[asset_name] = []
            self._asset_index[asset_name].append(package_path)

        print(f"에셋 인덱스 생성 완료: {len(self._asset_index)} 개의 에셋")
        self._initialized = True

    def get_path(self, asset_name):
        """캐시된 에셋 경로 반환"""
        # 캐시 확인
        if asset_name in self._cache:
            return self._cache[asset_name]

        # 고정 경로 확인
        if asset_name in FIXED_PATHS:
            self._cache[asset_name] = FIXED_PATHS[asset_name]
            return self._cache[asset_name]

        # 인덱스에서 검색 (대소문자 구분 없이)
        asset_name_lower = asset_name.lower()
        if asset_name_lower in self._asset_index:
            # 여러 경로 중에서 가장 적절한 것 선택
            paths = self._asset_index[asset_name_lower]
            for path in paths:
                # LIT_ 파일의 경우 LightingLevel 폴더에 있는지 확인
                if asset_name.startswith('LIT_') and 'LightingLevel' in path:
                    full_path = f"{path}.{asset_name}"
                    self._cache[asset_name] = full_path
                    return full_path
                # CAM_ 파일의 경우 PhotoSpot 폴더에 있는지 확인
                elif asset_name.startswith('CAM_') and 'PhotoSpot' in path:
                    full_path = f"{path}.{asset_name}"
                    self._cache[asset_name] = full_path
                    return full_path
                # BP_ 파일의 경우 SubLevel 폴더에 있는지 확인
                elif asset_name.startswith('BP_') and 'SubLevel' in path:
                    full_path = f"{path}.{asset_name}"
                    self._cache[asset_name] = full_path
                    return full_path
                # LV_ 또는 SZ_ 파일의 경우 MainLevel 폴더에 있는지 확인
                elif (asset_name.startswith('LV_') or asset_name.startswith('SZ_')) and 'MainLevel' in path:
                    full_path = f"{path}.{asset_name}"
                    self._cache[asset_name] = full_path
                    return full_path

            # 특정 폴더를 찾지 못한 경우 첫 번째 경로 사용
            if paths:
                full_path = f"{paths[0]}.{asset_name}"
                self._cache[asset_name] = full_path
                return full_path

        # 찾지 못한 경우
        self._cache[asset_name] = ""
        return ""

    def check_asset_duplicates(self, asset_name):
        """에셋 중복 검사"""
        asset_name_lower = asset_name.lower()
        if asset_name_lower in self._duplicate_assets:
            paths = self._duplicate_assets[asset_name_lower]
            if len(paths) > 1:
                return paths
        return None

# 전역 캐시 인스턴스 생성
asset_cache = AssetPathCache()

def find_asset_path(asset_name):
    """에셋 경로 찾기 (캐시 사용)"""
    # 캐시 초기화 확인
    if not asset_cache._initialized:
        asset_cache.initialize()

    path = asset_cache.get_path(asset_name)
    if path:
        print(f"에셋 찾음 {asset_name}: {path}")
    else:
        print(f"에셋을 찾을 수 없음: {asset_name}")
    return path

def show_duplicate_warning(duplicate_assets):
    """중복 파일 경고 창 표시"""
    dialog = unreal.EditorDialog()
    message = "다음 파일들이 중복되어 임포트가 중지되었습니다:\n\n"
    message += "\n".join(duplicate_assets)  # 중복된 파일명만 표시

    dialog.show_message(
        "경고",
        message,
        unreal.AppMsgType.OK,
        unreal.AppReturnType.OK
    )

def set_file_writable(file_path):
    """파일의 읽기 전용 속성을 해제"""
    if os.path.exists(file_path):
        try:
            import stat
            current_permissions = os.stat(file_path).st_mode
            os.chmod(file_path, current_permissions | stat.S_IWRITE)
            print(f"파일 쓰기 권한 설정됨: {file_path}")
            return True
        except Exception as e:
            print(f"파일 권한 변경 실패: {str(e)}")
            return False
    return True

def checkout_and_make_writable(asset_path):
    """에셋을 소스 컨트롤에서 checkout하고 쓰기 가능하게 만듦"""
    try:
        # 에셋이 존재하는지 확인
        if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            print(f"에셋이 존재하지 않음: {asset_path}")
            return {'success': False, 'error': f"에셋이 존재하지 않습니다: {asset_path}"}

        # 에셋 로드
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        if not asset:
            print(f"에셋을 로드할 수 없음: {asset_path}")
            return {'success': False, 'error': f"에셋을 로드할 수 없습니다: {asset_path}"}

        # 소스 컨트롤 상태 확인
        try:
            source_control = unreal.EditorUtilityLibrary.get_source_control_provider()
            if source_control and source_control.is_enabled():
                state = source_control.get_state(asset_path)
                if state:
                    other_user = state.get_other_user()
                    if other_user:
                        error_msg = f"{other_user}에 의해 에셋이 잠겨있습니다. {other_user}에게 문의해주세요."
                        print(f"⚠️ {error_msg}")
                        return {'success': False, 'error': error_msg}
        except Exception as e:
            print(f"소스 컨트롤 상태 확인 중 오류 발생: {str(e)}")

        # 에셋 체크아웃 시도
        try:
            if not unreal.EditorAssetLibrary.checkout_loaded_asset(asset):
                print(f"⚠️ 에셋 체크아웃 실패: {asset_path}")
                return {'success': False, 'error': "에셋이 잠겨있습니다. 소스 컨트롤 상태를 확인해주세요."}
        except Exception as e:
            print(f"체크아웃 중 오류 발생: {str(e)}")
            return {'success': False, 'error': f"체크아웃 중 오류 발생: {str(e)}"}

        print(f"✅ 에셋이 체크아웃됨: {asset_path}")

        # 에셋의 실제 파일 경로 가져오기
        package_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
        if not package_path:
            print(f"에셋 경로를 찾을 수 없음: {asset_path}")
            return {'success': False, 'error': f"에셋 경로를 찾을 수 없습니다: {asset_path}"}

        # 파일 쓰기 가능하게 만들기
        if not set_file_writable(package_path):
            print(f"파일을 쓰기 가능하게 만들 수 없음: {package_path}")
            return {'success': False, 'error': f"파일을 쓰기 가능하게 만들 수 없습니다: {package_path}"}

        print(f"✅ 에셋이 쓰기 가능하게 설정됨: {asset_path}")
        return {'success': True}
    except Exception as e:
        print(f"에셋 설정 중 오류 발생: {str(e)}")
        return {'success': False, 'error': str(e)}

def import_table(sheet_id=SHEET_ID, gid=GID):
    try:
        print(f"=== 레벨 데이터 임포트 시작 ===")
        print("테이블 정보:")
        print(f"- Sheet ID: {sheet_id}")
        print(f"- GID: {gid}")
        print(f"- 테이블 경로: {TABLE_PATH}")

        data = get_sheet_data(sheet_id, gid)
        if not data:
            return {'success': False, 'error': '데이터를 가져올 수 없습니다.'}

        # 에셋 checkout
        checkout_result = checkout_and_make_writable(TABLE_PATH)
        if not checkout_result['success']:
            print(f"체크아웃 실패: {checkout_result['error']}")
            return checkout_result

        # 데이터 테이블 생성 또는 로드
        data_table = unreal.EditorAssetLibrary.load_asset(TABLE_PATH)
        if not data_table:
            data_table = unreal.EditorAssetLibrary.make_new_data_table_asset(TABLE_PATH, unreal.DataTable)
            if not data_table:
                print(f"데이터 테이블 생성 실패: {TABLE_PATH}")
                return {'success': False, 'error': '데이터 테이블을 생성할 수 없습니다.'}

        # 컬럼 핸들러 설정
        column_handler = ColumnHandler("레벨 데이터")
        column_handler.set_required_columns(['ID'])
        column_handler.add_handled_columns(['ID', 'Level'])

        # 컬럼 검증
        if not column_handler.process_columns(data):
            return {'success': False, 'error': '컬럼 검증 실패'}

        # 데이터 처리 및 저장
        if process_and_save_data(data_table, data):
            print(f"데이터 테이블 업데이트 성공 ({len(data)}행)")
            return {'success': True, 'count': len(data)}
        return {'success': False, 'error': '데이터 처리 중 오류가 발생했습니다.'}

    except Exception as e:
        print(f"실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def get_level_info(level_id):
    """특정 레벨 ID의 정보 반환"""
    try:
        data = get_sheet_data(SHEET_ID, GID)
        if not data:
            return None

        for row in data[1:]:
            if row.get('ID') == level_id:
                return {
                    'ID': row.get('ID'),
                    'Level': row.get('Level'),
                    'Thumb': f"/Game/Thumbnails/Maps/{row.get('ID')}/PhotoSpot1",
                    # 필요한 다른 필드들 추가
                }

        return None
    except Exception as e:
        print(f"레벨 정보 가져오기 실패: {str(e)}")
        return None

def process_and_save_data(data_table, data):
    try:
        # CSV 파일 생성
        temp_dir = tempfile.gettempdir()
        temp_csv_path = os.path.join(temp_dir, "temp_level_data.csv")

        fieldnames = ['Name', 'Level']

        with open(temp_csv_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                level_id = str(row.get('ID', '')).strip()
                if not level_id:
                    continue

                level_path = str(row.get('Level', '')).strip()
                if not level_path:
                    level_path = find_asset_path(level_id)

                new_row = {
                    'Name': level_id,
                    'Level': level_path
                }
                writer.writerow(new_row)

        # 데이터 테이블 임포트 설정
        struct_path = "/Script/Cinev.CinevStreamingLevelData"  # 수정된 구조체 경로
        row_struct = unreal.load_object(None, struct_path)

        if not row_struct:
            print(f"구조체를 찾을 수 없습니다: {struct_path}")
            return False

        # CSV 임포트 설정
        factory = unreal.CSVImportFactory()
        factory.automated_import_settings.import_row_struct = row_struct

        # 임포트 태스크 설정
        task = unreal.AssetImportTask()
        task.filename = temp_csv_path
        task.destination_path = os.path.dirname(TABLE_PATH)
        task.destination_name = os.path.basename(TABLE_PATH).replace("/Game/", "")
        task.replace_existing = True
        task.automated = True
        task.save = True
        task.factory = factory

        # 데이터 테이블 임포트 실행
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
        asset_tools.import_asset_tasks([task])

        # 임시 파일 삭제
        try:
            os.remove(temp_csv_path)
            print(f"임시 파일 삭제됨: {temp_csv_path}")
        except Exception as e:
            print(f"임시 파일 삭제 실패: {e}")

        # 콘텐츠 브라우저 새로고침
        try:
            content_browser = unreal.get_editor_subsystem(unreal.ContentBrowserSubsystem)
            content_browser.refresh_folder(os.path.dirname(TABLE_PATH))
        except Exception as e:
            print(f"콘텐츠 브라우저 새로고침 실패: {e}")

        return True
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {str(e)}")
        return False