import unreal
import os
import csv
import tempfile
from scripts.common.utils import get_sheet_data

SHEET_ID = "1I4HCvuZkhIXRzQJcNj3teSioX5cxgi2NHZ3iEy76c4g"
GID = "0"
TABLE_PATH = "/Game/Core/DataTable/UnitAction/DT_UnitActionMetaData"

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
        print(f"=== 유닛 액션 메타데이터 임포트 시작 ===")
        print("테이블 정보:")
        print(f"- Sheet ID: {sheet_id}")
        print(f"- GID: {gid}")
        print(f"- 테이블 경로: {TABLE_PATH}")

        # 프로젝트 Content 디렉토리 경로 가져오기
        content_dir = unreal.Paths.project_content_dir()

        data = get_sheet_data(sheet_id, gid)
        if not data:
            return {'success': False, 'error': '데이터를 가져올 수 없습니다.'}

        # 에셋 checkout
        checkout_result = checkout_and_make_writable(TABLE_PATH)
        if not checkout_result['success']:
            return checkout_result

        # 데이터 테이블 생성 또는 로드
        data_table = unreal.EditorAssetLibrary.load_asset(TABLE_PATH)
        if not data_table:
            data_table = unreal.EditorAssetLibrary.make_new_data_table_asset(TABLE_PATH, unreal.DataTable)
            if not data_table:
                print(f"데이터 테이블 생성 실패: {TABLE_PATH}")
                return {'success': False, 'error': '데이터 테이블을 생성할 수 없습니다.'}

        # 데이터 처리 및 저장
        if process_and_save_data(data_table, data):
            print(f"데이터 테이블 업데이트 성공 ({len(data)}행)")
            return {'success': True, 'count': len(data)}
        return {'success': False, 'error': '데이터 처리 중 오류가 발생했습니다.'}

    except Exception as e:
        print(f"유닛 액션 메타데이터 임포트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

def process_and_save_data(data_table, data):
    # 필요한 필드만 선택하여 CSV 데이터 생성
    csv_data = []
    skipped_count = 0
    total_count = 0

    for row in data:
        total_count += 1
        # AnimationIndex와 ActionKey가 모두 비어있는 행은 건너뛰기
        if not row.get('AnimationIndex', '').strip() or not row.get('ActionKey', '').strip():
            skipped_count += 1
            continue

        csv_row = {
            'Name': row['AnimationIndex'],
            'ActionKey': row['ActionKey'],
            'Description': f"INVTEXT(\"{row['Description']}\")" if row.get('Description') else "INVTEXT(\"\")",
            'bIsUseableByS2M': row.get('bIsUseableByS2M', 'TRUE'),
            'bIsExposedToLibrary': row.get('bIsExposedToLibrary', 'TRUE'),
            'bIsCandidateForMetaAction': row.get('bIsCandidateForMetaAction', 'TRUE')
        }
        csv_data.append(csv_row)

    print(f"전체 행 수: {total_count}")
    print(f"건너뛴 행 수: {skipped_count}")
    print(f"처리된 행 수: {len(csv_data)}")

    # 임시 CSV 파일 생성
    temp_csv_path = os.path.join(tempfile.gettempdir(), 'temp_unit_action_metadata.csv')

    with open(temp_csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_data[0].keys())
        writer.writeheader()
        writer.writerows(csv_data)

    # Row Structure 설정
    struct_path = "/Script/Cinev.CinevUnitActionMetaData"
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
        unreal.EditorLoadingAndSavingUtils.reload_directories_in_path(os.path.dirname(TABLE_PATH))
    except Exception as e:
        print(f"콘텐츠 브라우저 새로고침 실패: {e}")

    print(f"데이터 테이블 업데이트 성공 ({len(data)}행)")
    return True