import unreal
import os
import csv
import tempfile
import urllib.request
import json
from ..common.utils import set_file_writable, get_sheet_data

# 구글 시트 정보
SHEET_ID = "1as2q_Me31jXwfMA6yFF3r6PrZxd0MREjSMGZRmfjcOg"
GID = "1372236030"
TABLE_PATH = "/Game/Core/DataTable/DT_PropAsset"

def get_sheet_data(sheet_id, gid):
    """구글 시트에서 데이터 가져오기"""
    try:
        # 새로운 URL 사용
        base_url = "https://script.google.com/macros/s/AKfycbxufEpdMUBw9Pz6geYd6_msxwCVLwNlezK13YgRRlIl3cZksOJ66ANYGtO3L-ncYNasEA/exec"
        url = f"{base_url}?sheetId={sheet_id}&gid={gid}"
        print(f"요청 URL: {url}")

        response = urllib.request.urlopen(url)
        data = response.read().decode('utf-8')

        json_data = json.loads(data)
        if isinstance(json_data, list):
            print(f"데이터 {len(json_data)}개 로드됨")
            if len(json_data) > 0:
                print(f"첫 번째 행 필드: {list(json_data[0].keys())}")
        return json_data

    except Exception as e:
        print(f"데이터 가져오기 오류: {str(e)}")
        return None

def get_asset_path(asset_name):
    """에셋 이름으로부터 전체 경로를 생성"""
    try:
        # 에셋 레지스트리를 사용하여 모든 에셋 경로 가져오기
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

        # 에셋 검색을 위한 필터 생성
        ar_filter = unreal.ARFilter(
            class_names=["Blueprint"],
            recursive_paths=True,
            package_paths=["/Game"]  # 전체 Game 디렉토리 검색
        )

        # 에셋 검색
        all_assets = asset_registry.get_assets(ar_filter)

        # 중복 체크를 위한 리스트
        found_paths = []

        # 정확한 이름 매칭 시도
        for asset in all_assets:
            if asset.asset_name == asset_name:
                found_paths.append(str(asset.package_name))

        # 결과 처리
        if len(found_paths) > 1:
            print(f"경고: 중복된 에셋이 발견됨 ({asset_name}):")
            for path in found_paths:
                print(f"  - {path}")
            return None
        elif len(found_paths) == 1:
            return found_paths[0]

        print(f"에셋을 찾을 수 없음: {asset_name}")
        return None

    except Exception as e:
        print(f"에셋 경로 검색 중 에러 발생: {str(e)}")
        return None

def get_asset_tags(asset_name):
    """에셋의 게임플레이 태그 가져오기 (읽기 전용)"""
    try:
        # 에셋 레지스트리를 사용하여 블루프린트 찾기
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

        # 블루프린트 검색을 위한 필터 생성
        ar_filter = unreal.ARFilter(
            class_names=["Blueprint"],
            recursive_paths=True,
            package_paths=["/Game"]  # 전체 Game 디렉토리 검색
        )

        # 에셋 검색
        all_assets = asset_registry.get_assets(ar_filter)

        # 블루프린트 찾기
        bp_asset = None
        for asset in all_assets:
            if asset.asset_name == asset_name:
                bp_asset = asset
                break

        if not bp_asset:
            print(f"블루프린트를 찾을 수 없음: {asset_name}")
            return "(GameplayTags=)"

        # 블루프린트 경로 구성
        bp_path = str(bp_asset.package_name)
        print(f"블루프린트 경로: {bp_path}")

        # 블루프린트 클래스 경로 구성
        bp_class_path = f"{bp_path}.{asset_name}_C"

        # 블루프린트 클래스 로드 (읽기 전용)
        bp_class = unreal.load_class(None, bp_class_path)
        if not bp_class:
            print(f"블루프린트 클래스를 로드할 수 없음: {bp_class_path}")
            return "(GameplayTags=)"

        # 기본 객체 가져오기 (읽기 전용)
        default_obj = unreal.get_default_object(bp_class)
        if not default_obj:
            print(f"기본 객체를 가져올 수 없음: {bp_class_path}")
            return "(GameplayTags=)"

        # GameplayTags 프로퍼티 찾기 (읽기 전용)
        try:
            # CinevPropComponent 찾기
            prop_component = None
            for component in default_obj.get_components_by_class(unreal.ActorComponent):
                if component.get_name().startswith("CinevProp"):
                    prop_component = component
                    break

            if prop_component:
                # GameplayTags 프로퍼티 찾기
                for prop_name in dir(prop_component):
                    if prop_name.endswith("Tags") and not prop_name.startswith("__"):
                        tag_container = getattr(prop_component, prop_name)
                        if tag_container and len(tag_container.gameplay_tags) > 0:
                            tags = []
                            for tag in tag_container.gameplay_tags:
                                tag_str = str(tag)
                                if tag_str and tag_str != "None":
                                    tags.append(f'(TagName="{tag_str}")')
                            if tags:
                                return f"(GameplayTags=({','.join(tags)}))"

        except Exception as e:
            print(f"태그 검색 중 에러 발생: {str(e)}")

        print(f"태그를 찾을 수 없음: {asset_name}")
        return "(GameplayTags=)"

    except Exception as e:
        print(f"태그 가져오기 중 에러 발생: {str(e)}")
        return "(GameplayTags=)"

def format_asset_path(asset_name):
    """에셋의 AssetClassPath 형식 경로 생성"""
    try:
        # 에셋 레지스트리를 사용하여 블루프린트 찾기
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

        # 블루프린트 검색을 위한 필터 생성
        ar_filter = unreal.ARFilter(
            class_names=["Blueprint"],
            recursive_paths=True,
            package_paths=["/Game"]
        )

        # 에셋 검색
        all_assets = asset_registry.get_assets(ar_filter)

        # 블루프린트 찾기
        bp_asset = None
        for asset in all_assets:
            if asset.asset_name == asset_name:
                bp_asset = asset
                break

        if not bp_asset:
            print(f"블루프린트를 찾을 수 없음: {asset_name}")
            return ""

        # 블루프린트 클래스 경로 구성
        bp_path = str(bp_asset.package_name)
        bp_class_path = f"{bp_path}.{asset_name}_C"
        print(f"블루프린트 경로: {bp_path}")

        # 블루프린트 클래스 참조 형식으로 반환 (SoftClassPath)
        return f"BlueprintGeneratedClass'{bp_class_path}'"

    except Exception as e:
        print(f"에셋 경로 포맷 중 에러 발생: {str(e)}")
        return ""

def format_thumbnail_path(asset_name):
    """에셋의 썸네일 경로 생성"""
    try:
        # 에셋 레지스트리를 사용하여 모든 에셋 경로 가져오기
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

        # 에셋 검색을 위한 필터 생성
        ar_filter = unreal.ARFilter(
            class_names=["Texture2D"],
            recursive_paths=True,
            package_paths=["/Game"]  # 전체 Game 디렉토리 검색
        )

        # 에셋 검색
        all_assets = asset_registry.get_assets(ar_filter)

        # 중복 체크를 위한 리스트
        found_paths = []

        # 정확한 이름 매칭 시도
        for asset in all_assets:
            if asset.asset_name == asset_name:
                found_paths.append(str(asset.package_name))

        # 결과 처리
        if len(found_paths) > 1:
            print(f"경고: 중복된 썸네일이 발견됨 ({asset_name}):")
            for path in found_paths:
                print(f"  - {path}")
            return ""
        elif len(found_paths) == 1:
            # 올바른 포맷으로 경로 반환
            return f"/Script/Engine.Texture2D'{found_paths[0]}.{asset_name}'"

        print(f"썸네일을 찾을 수 없음: {asset_name}")
        return ""

    except Exception as e:
        print(f"썸네일 경로 검색 중 에러 발생: {str(e)}")
        return ""

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

def process_and_save_data(data_table, data):
    """CSV 데이터를 처리하고 데이터 테이블에 저장"""
    try:
        # CSV 파일 생성
        temp_dir = tempfile.gettempdir()
        temp_csv_path = os.path.join(temp_dir, "temp_prop_asset.csv")

        fieldnames = ['RowName', 'DisplayName', 'AssetClassPath', 'Thumbnail', 'PropTags', 'Description', 'bIsEnabled', 'bIsExposedtoLibrary']

        with open(temp_csv_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                asset_name = row.get('AssetName', '')
                display_name = row.get('Display Name', '')
                description = row.get('Desc', '')
                is_enabled = row.get('bIsEnabled', 'false').lower() == 'true'
                is_exposed = row.get('bIsExposedtoLibrary', 'false').lower() == 'true'

                if not asset_name:
                    continue

                # 에셋 경로와 썸네일 경로 가져오기
                asset_path = format_asset_path(asset_name)
                thumbnail_path = format_thumbnail_path(asset_name)

                new_row = {
                    'RowName': asset_name,
                    'DisplayName': display_name,
                    'AssetClassPath': asset_path or "",
                    'Thumbnail': thumbnail_path,
                    'PropTags': "(GameplayTags=)",  # 빈 태그 컨테이너
                    'Description': description,
                    'bIsEnabled': str(is_enabled).lower(),
                    'bIsExposedtoLibrary': str(is_exposed).lower()
                }
                writer.writerow(new_row)

        # 데이터 테이블 임포트 설정
        struct_path = "/Script/Cinev.CinevPropAssetData"  # 수정된 구조체 경로
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

        return True

    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def import_table(sheet_id=SHEET_ID, gid=GID):
    try:
        print(f"=== 프롭 에셋 임포트 시작 ===")
        print("테이블 정보:")
        print(f"- Sheet ID: {sheet_id}")
        print(f"- GID: {gid}")
        print(f"- 테이블 경로: {TABLE_PATH}")

        data = get_sheet_data(sheet_id, gid)
        if not data:
            return {'success': False, 'error': '데이터를 가져올 수 없습니다.'}

        # 데이터 구조 출력
        if len(data) > 0:
            print("\n=== 데이터 구조 확인 ===")
            print("첫 번째 행의 키:", list(data[0].keys()))
            print("첫 번째 행의 값:", data[0])
            print(f"총 데이터 수: {len(data)}")
            print("========================\n")

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
        print(f"프롭 에셋 임포트 중 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}