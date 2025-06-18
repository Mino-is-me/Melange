import unreal
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import urllib.request
import json
import tempfile
import os
import csv
from datetime import datetime
import os.path
import sys
import importlib
from ..common.utils import get_sheet_data, check_unreal_environment

SHEET_ID = "1D0yAS0QdlNbXWsYUKC1P8Tu9wnWapTMJhOUFx5YQDjo"
GID = "1354904481"
TABLE_PATH = "/Game/Core/DataTable/CharacterCustomize/DT_CinevCharacterPresetData"

class ImportHistory:
    def __init__(self):
        self.history_file = "character_preset_import_history.json"
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def add_entry(self, data, row_count):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            'timestamp': timestamp,
            'row_count': row_count,
            'data': data
        }
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()
        self.save_history()
        return timestamp

class AssetPathCache:
    def __init__(self):
        self._cache = {}
        self._asset_index = {}
        self._initialized = False
        self._duplicate_thumbnails = {}  # 중복 썸네일 추적용

    def initialize(self):
        if self._initialized:
            return

        print("에셋 인덱스 초기화 중...")
        asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

        ar_filter = unreal.ARFilter(
            package_paths=["/Game"],
            recursive_paths=True
        )
        assets = asset_registry.get_assets(ar_filter)

        # 에셋 인덱스 생성 및 중복 검사
        for asset in assets:
            package_path = str(asset.package_name)
            package_path_lower = package_path.lower()

            path_parts = package_path_lower.split('/')
            asset_name = path_parts[-1]

            # 썸네일 에셋 중복 검사
            if asset_name.startswith('t_'):
                if asset_name in self._duplicate_thumbnails:
                    self._duplicate_thumbnails[asset_name].append(package_path)
                else:
                    self._duplicate_thumbnails[asset_name] = [package_path]

            if asset_name not in self._asset_index:
                self._asset_index[asset_name] = []
            self._asset_index[asset_name].append(package_path)

        print(f"에셋 인덱스 생성 완료: {len(self._asset_index)} 개의 에셋")
        self._initialized = True

    def check_thumbnail_duplicates(self, thumbnail_name):
        """썸네일 중복 검사"""
        thumbnail_name_lower = thumbnail_name.lower()
        if thumbnail_name_lower in self._duplicate_thumbnails:
            paths = self._duplicate_thumbnails[thumbnail_name_lower]
            if len(paths) > 1:
                return paths
        return None

    def get_path(self, asset_name):
        """캐시된 에셋 경로 반환"""
        if asset_name in self._cache:
            return self._cache[asset_name]

        asset_name_lower = asset_name.lower()
        if asset_name_lower in self._asset_index:
            paths = self._asset_index[asset_name_lower]
            if paths:
                full_path = f"{paths[0]}.{asset_name}"
                self._cache[asset_name] = full_path
                return full_path

        self._cache[asset_name] = ""
        return ""

# 전역 캐시 인스턴스 생성
asset_cache = AssetPathCache()

def create_gui():
    root = tk.Tk()
    root.title("캐릭터 프리셋 데이터 임포트")
    root.geometry("800x700")

    history_manager = ImportHistory()

    # 구글 시트 정보 프레임
    sheet_info_frame = ttk.LabelFrame(root, text="구글 시트 정보", padding="10")
    sheet_info_frame.pack(fill=tk.X, padx=10, pady=5)

    ttk.Label(sheet_info_frame, text="시트 ID:").pack(anchor=tk.W)
    sheet_id_entry = ttk.Entry(sheet_info_frame, width=50)
    sheet_id_entry.pack(fill=tk.X, pady=(0, 5))
    sheet_id_entry.insert(0, SHEET_ID)

    ttk.Label(sheet_info_frame, text="GID:").pack(anchor=tk.W)
    gid_entry = ttk.Entry(sheet_info_frame, width=20)
    gid_entry.pack(fill=tk.X, pady=(0, 5))
    gid_entry.insert(0, GID)

    # 히스토리 프레임
    history_frame = ttk.LabelFrame(root, text="임포트 히스토리", padding="10")
    history_frame.pack(pady=10, padx=10, fill=tk.X)

    history_var = tk.StringVar()
    history_combo = ttk.Combobox(history_frame, textvariable=history_var, width=40)
    history_combo['values'] = [f"{entry['timestamp']} ({entry['row_count']}행)"
                             for entry in history_manager.history]
    history_combo.pack(side=tk.LEFT, padx=5)

    def update_history_combo():
        history_combo['values'] = [f"{entry['timestamp']} ({entry['row_count']}행)"
                                 for entry in history_manager.history]
        if history_combo['values']:
            history_combo.current(0)

    def view_history_data():
        selected = history_combo.current()
        if selected >= 0:
            entry = history_manager.history[selected]
            data_window = tk.Toplevel(root)
            data_window.title(f"임포트 데이터 - {entry['timestamp']}")
            data_window.geometry("800x600")

            text_frame = tk.Frame(data_window)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            scrollbar = tk.Scrollbar(text_frame)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            text_area = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set)
            text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            scrollbar.config(command=text_area.yview)

            text_area.insert(tk.END, f"임포트 시간: {entry['timestamp']}\n")
            text_area.insert(tk.END, f"처리된 행 수: {entry['row_count']}\n\n")
            text_area.insert(tk.END, "데이터 내용:\n")
            for idx, row in enumerate(entry['data'], 1):
                text_area.insert(tk.END, f"\n{idx}. Row Name: {row.get('Row Name', '')}\n")
                text_area.insert(tk.END, f"   DisplayName: {row.get('DisplayName', '')}\n")
                text_area.insert(tk.END, f"   Sex: {row.get('Sex', '')}\n")

            text_area.config(state=tk.DISABLED)

    view_button = ttk.Button(history_frame, text="상세보기", command=view_history_data)
    view_button.pack(side=tk.LEFT, padx=5)

    # 상태 표시 레이블
    status_label = tk.Label(root, text="", wraplength=700)
    status_label.pack(pady=10)

    def import_data():
        try:
            sheet_id = sheet_id_entry.get().strip()
            gid = gid_entry.get().strip()

            if not sheet_id or not gid:
                status_label.config(text="시트 ID와 GID를 입력해주세요.", fg="red")
                return

            data = get_sheet_data(sheet_id, gid)
            if not data:
                status_label.config(text="데이터를 가져올 수 없습니다.", fg="red")
                return

            result = import_table(sheet_id, gid)
            if result['success']:
                timestamp = history_manager.add_entry(data, len(data))
                update_history_combo()

                status_text = f"임포트 완료!\n총 {len(data)}개의 행이 추가되었습니다."
                status_label.config(text=status_text, fg="green")
            else:
                status_label.config(text=f"임포트 실패: {result.get('error', '알 수 없는 오류가 발생했습니다.')}", fg="red")

        except Exception as e:
            status_label.config(text=f"오류 발생: {str(e)}", fg="red")

    # 임포트 버튼
    import_button = ttk.Button(root, text="구글 시트에서 임포트", command=import_data, width=30)
    import_button.pack(pady=20)

    return root

def show_duplicate_warning(duplicate_thumbnails):
    """중복 파일 경고 창 표시"""
    dialog = unreal.EditorDialog()
    message = "다음 썸네일 파일들이 중복되어 임포트가 중지되었습니다:\n\n"
    message += "\n".join(duplicate_thumbnails)  # 중복된 파일명만 표시

    dialog.show_message(
        "경고",
        message,
        unreal.AppMsgType.OK,
        unreal.AppReturnType.OK
    )

def find_asset_by_name(asset_name):
    """에셋 이름으로 프로젝트에서 검색"""
    found_assets = unreal.EditorAssetLibrary.list_assets("/Game/", recursive=True)

    # 에셋 이름으로 검색
    for asset_path in found_assets:
        if asset_name in asset_path:  # 파일명이 경로에 포함되어 있는지 확인
            if unreal.EditorAssetLibrary.does_asset_exist(asset_path):
                return asset_path
    return None

def extract_filename(path):
    """경로에서 실제 파일명만 추출"""
    # 경로에서 마지막 부분만 가져옴
    filename = path.split('/')[-1]

    # 확장자가 있다면 제거
    if '.' in filename:
        filename = filename.split('.')[0]

    return filename

def check_duplicate_thumbnails(data):
    # 모든 PNG 파일 경로를 한 번만 가져옴
    all_assets = unreal.EditorAssetLibrary.list_assets("/Game/", recursive=True)
    png_paths = [path for path in all_assets if path.lower().endswith('.png')]

    # 각 썸네일 이름에 대한 경로 매핑
    thumbnail_paths = {}
    for path in png_paths:
        # 파일명만 추출 (확장자 제외)
        filename = path.split('/')[-1].split('.')[0]
        if filename not in thumbnail_paths:
            thumbnail_paths[filename] = []
        thumbnail_paths[filename].append(path)

    # 중복 체크
    duplicates = {name: paths for name, paths in thumbnail_paths.items() if len(paths) > 1}
    if duplicates:
        message = "다음 썸네일 파일들이 중복되어 있습니다:\n\n"
        for name, paths in duplicates.items():
            message += f"{name}:\n"
            for path in paths:
                message += f"  - {path}\n"
        unreal.EditorDialog.show_message(
            "경고",
            "썸네일 중복 발견",
            message
        )
        return True
    return False

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
    try:
        # CSV 파일 생성
        temp_dir = tempfile.gettempdir()
        temp_csv_path = os.path.join(temp_dir, "temp_character_preset.csv")

        fieldnames = ['Row Name', 'Thumbnail', 'DisplayName', 'Sex', 'Filename',
                     'Description', 'DescriptionKO', 'bIsEnabled',
                     'bIsExposedToLibrary', 'bIsUseableByS2M']

        with open(temp_csv_path, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                row_name = str(row.get('Row Name', '')).strip()
                if not row_name:
                    continue

                new_row = {
                    'Row Name': row_name,
                    'Thumbnail': str(row.get('Thumbnail', '')).strip(),
                    'DisplayName': str(row.get('DisplayName', '')).strip(),
                    'Sex': str(row.get('Sex', '')).strip(),
                    'Filename': str(row.get('Filename', '')).strip(),
                    'Description': str(row.get('Description', '')).strip(),
                    'DescriptionKO': str(row.get('Description (KO)', '')).strip(),
                    'bIsEnabled': str(row.get('bIsEnabled', 'true')).upper(),
                    'bIsExposedToLibrary': str(row.get('bIsExposedToLibrary', 'true')).upper(),
                    'bIsUseableByS2M': str(row.get('bIsUseableByS2M', 'true')).upper()
                }
                writer.writerow(new_row)

        # 데이터 테이블 임포트 설정
        struct_path = "/Script/Cinev.CinevCharacterPresetData"
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

        # 데이터 테이블 새로고침
        try:
            # 에셋 레지스트리 새로고침
            unreal.EditorAssetLibrary.reload_asset(TABLE_PATH)

            # 콘텐츠 브라우저 새로고침
            content_browser = unreal.get_editor_subsystem(unreal.ContentBrowserSubsystem)
            content_browser.refresh_content_browser()

            # 모든 레벨의 액터 새로고침
            editor_level_lib = unreal.EditorLevelLibrary
            all_actors = editor_level_lib.get_all_level_actors()
            for actor in all_actors:
                actor.rerun_construction_scripts()

            print("데이터 테이블과 콘텐츠 브라우저가 새로고침되었습니다.")
        except Exception as e:
            print(f"새로고침 중 오류 발생: {str(e)}")

        return True
    except Exception as e:
        print(f"데이터 처리 중 오류 발생: {str(e)}")
        return False

def reload_modules():
    """현재 모듈과 관련 모듈들을 리로드"""
    try:
        # 현재 모듈의 경로를 기반으로 모듈 이름 생성
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        # 모듈 리로드
        if 'scripts.tables.character_preset' in sys.modules:
            importlib.reload(sys.modules['scripts.tables.character_preset'])
        if 'scripts.common.utils' in sys.modules:
            importlib.reload(sys.modules['scripts.common.utils'])

        print("✅ 모듈이 성공적으로 리로드되었습니다.")
        return True
    except Exception as e:
        print(f"❌ 모듈 리로드 중 오류 발생: {str(e)}")
        return False

def import_table(sheet_id=SHEET_ID, gid=GID):
    # 먼저 모듈 리로드
    reload_modules()

    try:
        print(f"=== 캐릭터 프리셋 데이터 임포트 시작 ===")
        print("테이블 정보:")
        print(f"- Sheet ID: {sheet_id}")
        print(f"- GID: {gid}")
        print(f"- 테이블 경로: {TABLE_PATH}")

        # 구글 시트에서 데이터 가져오기
        url = f"https://script.google.com/macros/s/AKfycbxufEpdMUBw9Pz6geYd6_msxwCVLwNlezK13YgRRlIl3cZksOJ66ANYGtO3L-ncYNasEA/exec?sheetId={sheet_id}&gid={gid}"
        print(f"요청 URL: {url}")

        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            print(f"데이터 {len(data)}개 로드됨")
            if data:
                print(f"첫 번째 행 필드: {list(data[0].keys())}")

        # 모든 에셋 경로를 한 번만 가져옴
        print("\n프로젝트 에셋 스캔 중...")
        all_assets = unreal.EditorAssetLibrary.list_assets("/Game/", recursive=True)
        print(f"총 {len(all_assets)}개의 에셋 찾음")

        # 썸네일 에셋 필터링 (PNG 확장자 체크 제거)
        thumbnail_assets = []
        for path in all_assets:
            # Thumbnails/Character 폴더의 에셋만 검색
            if "/Thumbnails/Character/" in path or "/RnD/Common/Thumbnails/" in path:
                thumbnail_assets.append(path)
                print(f"썸네일 에셋 발견: {path}")
        print(f"총 {len(thumbnail_assets)}개의 썸네일 에셋 찾음")

        # 에셋 경로 매핑 생성
        asset_mapping = {}
        for path in thumbnail_assets:
            # 파일명만 추출
            filename = path.split('/')[-1]
            if '.' in filename:
                filename = filename.rsplit('.', 1)[0]  # 확장자 제거

            # 파일명을 키로 사용
            if filename not in asset_mapping:
                asset_mapping[filename] = []
            asset_mapping[filename].append(path)
            print(f"에셋 매핑: {filename} -> {path}")

        print(f"총 {len(asset_mapping)}개의 썸네일 매핑 생성됨")

        # 데이터 처리
        print("\n데이터 처리 시작...")
        for row in data:
            # Description (KO) 필드 처리
            description_ko = str(row.get('Description (KO)', '')).strip()
            if not description_ko:  # Description (KO)가 비어있으면 Description 값을 복사
                description_ko = str(row.get('Description', '')).strip()
            row['Description (KO)'] = description_ko

            thumbnail = str(row.get('Thumbnail', '')).strip()
            if not thumbnail:
                continue

            print(f"\n처리 중인 썸네일: {thumbnail}")

            # 썸네일 경로 생성
            if thumbnail.startswith('T_'):
                # T_로 시작하는 경우 RnD 폴더에서 검색
                expected_path = f"/Game/RnD/Common/Thumbnails/{thumbnail}.{thumbnail}"
            else:
                # 숫자인 경우 Character 폴더에서 검색
                expected_path = f"/Game/Thumbnails/Character/{thumbnail}.{thumbnail}"

            print(f"검색할 경로: {expected_path}")

            # 정확한 경로 매칭
            found = False
            for path in thumbnail_assets:
                if path.lower() == expected_path.lower():
                    row['Thumbnail'] = path
                    print(f"썸네일 매칭됨: {path}")
                    found = True
                    break

            if not found:
                print(f"[경고] 썸네일을 찾을 수 없음: {thumbnail} (예상 경로: {expected_path})")
                row['Thumbnail'] = 'None'

        # 중복이 있으면 경고창 표시
        if any(row['Thumbnail'] == 'None' for row in data):
            message = "다음 썸네일 파일들이 중복되어 있습니다:\n\n"
            for row in data:
                if row['Thumbnail'] == 'None':
                    message += f"썸네일: {row['Thumbnail']}\n"
            unreal.log_warning(message)

        # CSV 파일 생성
        print("\nCSV 파일 생성 중...")
        fieldnames = ['Row Name', 'Thumbnail', 'DisplayName', 'Sex', 'Filename',
                     'Description', 'Description (KO)', 'bIsEnabled',
                     'bIsExposedToLibrary', 'bIsUseableByS2M']

        temp_csv_path = os.path.join(tempfile.gettempdir(), 'temp_character_preset.csv')
        with open(temp_csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()

            for row in data:
                # 데이터 정리
                row_data = {
                    'Row Name': str(row.get('Row Name', '')).strip(),
                    'Thumbnail': str(row.get('Thumbnail', '')).strip(),
                    'DisplayName': str(row.get('DisplayName', '')).strip(),
                    'Sex': str(row.get('Sex', '')).strip(),
                    'Filename': str(row.get('Filename', '')).strip(),
                    'Description': str(row.get('Description', '')).strip(),
                    'Description (KO)': str(row.get('Description (KO)', '')).strip(),
                    'bIsEnabled': str(row.get('bIsEnabled', 'true')).upper(),
                    'bIsExposedToLibrary': str(row.get('bIsExposedToLibrary', 'true')).upper(),
                    'bIsUseableByS2M': str(row.get('bIsUseableByS2M', 'true')).upper()
                }
                writer.writerow(row_data)

        print(f"CSV 파일 생성됨: {temp_csv_path}")

        # 데이터 테이블 임포트 설정
        print("\n데이터 테이블 임포트 설정 중...")
        struct_path = "/Script/Cinev.CinevCharacterPresetData"
        row_struct = unreal.load_object(None, struct_path)

        if not row_struct:
            return {'success': False, 'error': f"구조체를 찾을 수 없습니다: {struct_path}"}

        print(f"구조체 로드됨: {struct_path}")

        # CSV 임포트 설정
        factory = unreal.CSVImportFactory()
        factory.automated_import_settings.import_row_struct = row_struct

        # 임포트 태스크 설정
        task = unreal.AssetImportTask()
        task.filename = temp_csv_path
        task.destination_path = "/Game/Core/DataTable/CharacterCustomize"
        task.destination_name = "DT_CinevCharacterPresetData"
        task.replace_existing = True
        task.automated = True
        task.save = True
        task.factory = factory

        print("임포트 태스크 설정 완료")

        # 데이터 테이블 임포트 실행
        print("데이터 테이블 임포트 실행 중...")
        asset_tools = unreal.AssetToolsHelpers.get_asset_tools()

        # 임포트 타임아웃 설정 (30초)
        import time
        start_time = time.time()
        timeout = 30  # 30초 타임아웃

        # 임포트 실행
        asset_tools.import_asset_tasks([task])

        # 임포트 완료 대기
        while time.time() - start_time < timeout:
            if unreal.EditorAssetLibrary.does_asset_exist(TABLE_PATH):
                print("데이터 테이블 임포트 완료!")
                break
            time.sleep(1)
            print("임포트 진행 중...")

        if time.time() - start_time >= timeout:
            print("임포트 타임아웃 발생!")
            return {'success': False, 'error': "임포트 타임아웃이 발생했습니다. 30초 후에도 완료되지 않았습니다."}

        # 데이터 테이블 새로고침
        try:
            # 에셋 레지스트리 새로고침
            unreal.EditorAssetLibrary.reload_asset(TABLE_PATH)

            # 콘텐츠 브라우저 새로고침
            content_browser = unreal.get_editor_subsystem(unreal.ContentBrowserSubsystem)
            content_browser.refresh_content_browser()

            # 모든 레벨의 액터 새로고침
            editor_level_lib = unreal.EditorLevelLibrary
            all_actors = editor_level_lib.get_all_level_actors()
            for actor in all_actors:
                actor.rerun_construction_scripts()

            print("데이터 테이블과 콘텐츠 브라우저가 새로고침되었습니다.")
        except Exception as e:
            print(f"새로고침 중 오류 발생: {str(e)}")

        # 임시 파일 삭제
        try:
            os.remove(temp_csv_path)
            print(f"임시 파일 삭제됨: {temp_csv_path}")
        except Exception as e:
            print(f"임시 파일 삭제 실패: {e}")

        print(f"데이터 테이블 업데이트 성공")
        return {'success': True, 'count': len(data)}

    except Exception as e:
        print(f"임포트 실패: {str(e)}")
        import traceback
        traceback.print_exc()
        return {'success': False, 'error': str(e)}

if __name__ == "__main__":
    if not check_unreal_environment():
        if 'tkinter' in sys.modules:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("오류", "이 스크립트는 언리얼 에디터 내에서 실행해야 합니다.")
            root.destroy()
        sys.exit(1)

    root = create_gui()
    root.mainloop()