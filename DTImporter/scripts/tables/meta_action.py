import unreal
import tempfile
import os
import csv
from ..common.utils import get_sheet_data

SHEET_ID = "1pJmY-9qeM85mW0X69SqVfck-YENJKnh-y-vrg_VN5BQ"
GID = "866191023"
TABLE_PATH = "/Game/Core/DataTable/DT_MetaAction"

def create_target_data_list(data, row):
    """TargetDataList 문자열 생성"""
    # 첫 번째 TargetDataList
    allowed_types1 = str(row.get('허용타입', '0')).strip()
    required_prop_class_tag1 = str(row.get('필수클래스태그', '')).strip()
    required_prop_feature_tag1 = str(row.get('필수기능태그', '')).strip()
    target_description1 = str(row.get('대상설명', '')).strip()

    # 두 번째 TargetDataList
    allowed_types2 = str(row.get('허용타입2', '0')).strip()
    required_prop_class_tag2 = str(row.get('필수클래스태그2', '')).strip()
    required_prop_feature_tag2 = str(row.get('필수기능태그2', '')).strip()
    target_description2 = str(row.get('대상설명2', '')).strip()

    # 첫 번째 항목이 비어 있는지 확인
    is_first_empty = not (allowed_types1 or required_prop_class_tag1 or required_prop_feature_tag1 or target_description1)
    # 두 번째 항목이 비어 있는지 확인
    is_second_empty = not (allowed_types2 or required_prop_class_tag2 or required_prop_feature_tag2 or target_description2)

    if is_first_empty and is_second_empty:
        return "()"

    first_item = f'(AllowedTypes={allowed_types1 or "0"},RequiredPropClassTag=(TagName="{required_prop_class_tag1}"),RequiredPropFeatureTag=(TagName="{required_prop_feature_tag1}"),Description="{target_description1}")'

    if is_second_empty:
        return f'({first_item})'

    second_item = f'(AllowedTypes={allowed_types2 or "0"},RequiredPropClassTag=(TagName="{required_prop_class_tag2}"),RequiredPropFeatureTag=(TagName="{required_prop_feature_tag2}"),Description="{target_description2}")'

    return f'({first_item},{second_item})'

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
            return {'success': False, 'error': "에셋이 잠겨있습니다. 소스 컨트롤 상태를 확인해주세요."}

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
        print(f"=== 메타 액션 임포트 시작 ===")
        print("테이블 정보:")
        print(f"- Sheet ID: {sheet_id}")
        print(f"- GID: {gid}")
        print(f"- 테이블 경로: {TABLE_PATH}")

        data = get_sheet_data(sheet_id, gid)
        if not data:
            return {'success': False, 'error': '데이터를 가져올 수 없습니다.'}

        # 데이터 테이블 생성 또는 로드
        data_table = unreal.EditorAssetLibrary.load_asset(TABLE_PATH)
        if not data_table:
            data_table = unreal.EditorAssetLibrary.make_new_data_table_asset(TABLE_PATH, unreal.DataTable)
            if not data_table:
                print(f"데이터 테이블 생성 실패: {TABLE_PATH}")
                return {'success': False, 'error': '데이터 테이블을 생성할 수 없습니다.'}

        # 에셋 checkout
        checkout_result = checkout_and_make_writable(TABLE_PATH)
        if not checkout_result['success']:
            return checkout_result

        # 데이터 처리 및 저장
        if process_and_save_data(data_table, data):
            print(f"데이터 테이블 업데이트 성공 ({len(data)}행)")
            return {'success': True, 'count': len(data)}
        return {'success': False, 'error': '데이터 처리 중 오류가 발생했습니다.'}

    except Exception as e:
        print(f"메타 액션 임포트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def process_and_save_data(data_table, data):
    try:
        # CSV 파일 생성
        temp_dir = tempfile.gettempdir()
        temp_csv_path = os.path.join(temp_dir, "temp_meta_action.csv")

        fieldnames = ['Name', 'ActionKey', 'Type', 'Description', 'TargetDataList',
                     'bIsEnabled', 'bIsExposedToLibrary', 'bIsUseableByS2M']

        with open(temp_csv_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                action_key = str(row.get('행동키', '')).strip()
                if not action_key:
                    continue

                new_row = {
                    'Name': action_key,
                    'ActionKey': f'(TagName=ActionKey.{action_key})',
                    'Type': str(row.get('타입', '')).strip(),
                    'Description': str(row.get('설명', '')).strip(),
                    'TargetDataList': create_target_data_list(data, row),
                    'bIsEnabled': str(row.get('활성화', 'false')).upper(),
                    'bIsExposedToLibrary': str(row.get('유저사용', 'false')).upper(),
                    'bIsUseableByS2M': str(row.get('S2M사용', 'false')).upper()
                }
                writer.writerow(new_row)

        # 데이터 테이블 임포트 설정
        struct_path = "/Script/Cinev.CinevMetaActionData"
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

def import_meta_action(sheet_id, gid, table_path):
    try:
        print(f"=== 메타 액션 임포트 시작 ===")
        print("테이블 정보:")
        print(f"- Sheet ID: {sheet_id}")
        print(f"- GID: {gid}")
        print(f"- 테이블 경로: {table_path}")

        data = get_sheet_data(sheet_id, gid)
        if not data:
            return False

        # 에셋 checkout
        if not checkout_and_make_writable(table_path):
            return False

        # 데이터 테이블 생성 또는 로드
        data_table = unreal.EditorAssetLibrary.load_asset(table_path)
        if not data_table:
            data_table = unreal.EditorAssetLibrary.make_new_data_table_asset(table_path, unreal.DataTable)
            if not data_table:
                print(f"데이터 테이블 생성 실패: {table_path}")
                return False

        # 데이터 처리 및 저장
        if process_and_save_data(data_table, data):
            print(f"데이터 테이블 업데이트 성공 ({len(data)}행)")
            return True
        return False
    except Exception as e:
        print(f"메타 액션 임포트 중 오류 발생: {str(e)}")
        return False