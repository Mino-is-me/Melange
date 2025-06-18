import unreal
import tempfile
import csv
import os
import json
from scripts.common.utils import get_sheet_data  # 이 줄 추가
from . import level_data  # DT_LevelData 임포트를 위한 모듈

SHEET_ID = "19t28YoMTYX6jrA8tW5mXvsu7PMjUNco7VwQirzImmIE"
GID = "810949862"
TABLE_PATH = "/Game/Core/DataTable/Maps/DT_SceneLevel"

def create_scene_spot_data(display_name, thumb_id, camera_name):
    """SceneSpotData 구조체 생성"""
    # 썸네일 경로 생성
    thumbnail_path = f"/Game/Thumbnails/Maps/{thumb_id}/PhotoSpot1.PhotoSpot1"

    # 해당 썸네일이 존재하는지 확인
    if not unreal.EditorAssetLibrary.does_asset_exist(thumbnail_path):
        # 썸네일이 없으면 기본 이미지 사용
        thumbnail_path = "/Game/Thumbnails/Empty/T_empty_logo_horizontal.T_empty_logo_horizontal"

    return f'((DisplayName=NSLOCTEXT("", "{display_name}", "{display_name}"),'\
           f'Thumbnail="{thumbnail_path}",'\
           f'CameraName="{camera_name}",Tags=))'

def create_crowd_data():
    """CrowdData 구조체 생성"""
    return '((DisplayName="",DensityLevel=MildlyCrowded,CrowdLevelId=""),'\
           '(DisplayName="",DensityLevel=Crowded,CrowdLevelId=""))'

def create_light_environment(env_id, display_name, min_time, max_time):
    """LightEnvironment 구조체 생성"""
    return f'(DisplayName=NSLOCTEXT("", "{env_id}", "{display_name}"),'\
           f'MinEffectiveTime={min_time:.6f},'\
           f'MaxEffectiveTime={max_time:.6f},'\
           f'EnvironmentLevelId="{env_id}")'

def validate_row(row_dict):
    """필수 컬럼 검증"""
    required_fields = [
        'ID',  # MapID
        'DisplayName',
        'MainLevelId',
        'DefaultTimeOfTheDay',
        'SceneLightEnvironment.EnvironmentLevelId[0]',
        'SceneLightEnvironment.DisplayName[0]',
        'SceneLightEnvironment.MinEffectiveTime[0]',
        'SceneLightEnvironment.MaxEffectiveTime[0]',
        'bIsEnabled',
        'bIsExposedToLibrary'
    ]

    missing_fields = []
    for field in required_fields:
        if field not in row_dict or not row_dict[field]:
            missing_fields.append(field)

    if missing_fields:
        print(f"행 {row_dict.get('ID', '알 수 없음')} 누락된 필드: {', '.join(missing_fields)}")
        return False

    return True

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
        print(f"=== 씬 레벨 데이터 임포트 시작 ===")
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

def process_and_save_data(data_table, data):
    try:
        # CSV 파일 생성
        temp_dir = tempfile.gettempdir()
        temp_csv_path = os.path.join(temp_dir, "temp_scene_level_data.csv")

        fieldnames = ['ID', 'DisplayName', 'MainLevelId', 'CameraLevelId', 'PropLevelId',
                     'ZoneLevelId', 'SceneSpotDatas', 'DefaultCrowdDensityLevel',
                     'SceneCrowdDatas', 'DefaultTimeOfTheDay', 'SceneLightEnvironments',
                     'bIsEnabled', 'bIsExposedToLibrary']

        with open(temp_csv_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                scene_id = str(row.get('ID', '')).strip()
                if not scene_id:
                    continue

                # SceneSpotDatas 생성
                scene_spots = []
                for i in range(3):  # 최대 3개의 스팟 데이터
                    display_name = str(row.get(f'SceneSpotDatas_DisplayName[{i}]', '')).strip()
                    thumb = str(row.get(f'SceneSpotDatas_Thumb[{i}]', '')).strip()
                    camera = str(row.get(f'SceneSpotDatas_Camera[{i}]', '')).strip()

                    if display_name or thumb or camera:
                        thumbnail_path = f'/Game/Thumbnails/Maps/{scene_id}/{thumb}.{thumb}'
                        entry = f'(DisplayName="{display_name}",Thumbnail="{thumbnail_path}",CameraName="{camera}")'
                        scene_spots.append(entry)

                # SceneLightEnvironments 생성
                light_envs = []
                for i in range(3):  # DAY, SUNSET, NIGHT
                    env_id = str(row.get(f'SceneLightEnvironment.EnvironmentLevelId[{i}]', '')).strip()
                    display_name = str(row.get(f'SceneLightEnvironment.DisplayName[{i}]', '')).strip()
                    min_time = str(row.get(f'SceneLightEnvironment.MinEffectiveTime[{i}]', '0')).strip()
                    max_time = str(row.get(f'SceneLightEnvironment.MaxEffectiveTime[{i}]', '0')).strip()

                    if env_id and display_name:
                        light_envs.append({
                            'EnvironmentLevelId': env_id,
                            'DisplayName': display_name,
                            'MinEffectiveTime': min_time,
                            'MaxEffectiveTime': max_time
                        })

                new_row = {
                    'ID': scene_id,
                    'DisplayName': str(row.get('DisplayName', '')).strip(),
                    'MainLevelId': str(row.get('MainLevelId', '')).strip(),
                    'CameraLevelId': str(row.get('CameraLevelId', '')).strip(),
                    'PropLevelId': str(row.get('PropLevelId', '')).strip(),
                    'ZoneLevelId': str(row.get('ZoneLevelId', '')).strip(),
                    'SceneSpotDatas': f'({",".join(scene_spots)})',
                    'DefaultCrowdDensityLevel': str(row.get('DefaultCrowdDensityLevel', '')).strip(),
                    'SceneCrowdDatas': json.dumps([
                        {'DensityLevel': 'MildlyCrowded', 'LevelId': str(row.get('Mildly_Crowded', '')).strip()},
                        {'DensityLevel': 'Crowded', 'LevelId': str(row.get('Crowded', '')).strip()}
                    ]),
                    'DefaultTimeOfTheDay': str(row.get('DefaultTimeOfTheDay', '')).strip(),
                    'SceneLightEnvironments': json.dumps(light_envs),
                    'bIsEnabled': str(row.get('bIsEnabled', 'true')).upper(),
                    'bIsExposedToLibrary': str(row.get('bIsExposedToLibrary', 'true')).upper()
                }
                writer.writerow(new_row)

        # 데이터 테이블 임포트 설정
        struct_path = "/Script/Cinev.CinevSceneLevelData"
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

        return True
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {str(e)}")
        return False

def import_scene_level_data(sheet_id, gid, table_path):
    try:
        print(f"=== 씬 레벨 데이터 임포트 시작 ===")
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
        print(f"씬 레벨 데이터 임포트 중 오류 발생: {str(e)}")
        return False