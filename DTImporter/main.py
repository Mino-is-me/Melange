import unreal
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
import sys
from datetime import datetime
import json
import importlib  # 추가

# 현재 스크립트의 경로를 Python 경로에 추가
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 스크립트 모듈 임포트
try:
    from scripts.tables import meta_action, character_preset, unit_action_metadata, level_data, scene_level_data, facial_key_gameplay_tags, action_key_gameplay_tags, prop_asset
    from scripts.common.utils import check_unreal_environment
except ImportError as e:
    print(f"모듈 임포트 오류: {e}")
    print(f"현재 Python 경로: {sys.path}")
    print(f"현재 디렉토리: {current_dir}")
    sys.exit(1)

class ImportHistory:
    def __init__(self):
        self.history_file = "import_history.json"
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

    def add_entry(self, table_name, row_count):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            'timestamp': timestamp,
            'table_name': table_name,
            'row_count': row_count
        }
        self.history.insert(0, entry)
        if len(self.history) > 10:
            self.history.pop()
        self.save_history()
        return timestamp

class DataTableImporter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("데이터 테이블 임포터")

        # 에셋 라이브러리 초기화
        self.asset_library = unreal.EditorUtilityLibrary
        if not self.asset_library:
            print("에셋 라이브러리를 초기화할 수 없습니다.")

        # 설정 초기화
        self.meta_action_config = {
            "module": meta_action,
            "sheet_id": "1pJmY-9qeM85mW0X69SqVfck-YENJKnh-y-vrg_VN5BQ",
            "gid": "866191023",
            "table_path": "/Game/Core/DataTable/DT_MetaAction"
        }

        self.character_preset_config = {
            "module": character_preset,
            "sheet_id": "1D0yAS0QdlNbXWsYUKC1P8Tu9wnWapTMJhOUFx5YQDjo",
            "gid": "1354904481",
            "table_path": "/Game/Core/DataTable/CharacterCustomize/DT_CinevCharacterPresetData",
            "import_func": "import_table"  # 함수 이름 수정
        }

        self.unit_action_metadata_config = {
            "module": unit_action_metadata,
            "sheet_id": "1I4HCvuZkhIXRzQJcNj3teSioX5cxgi2NHZ3iEy76c4g",
            "gid": "0",
            "table_path": "/Game/Core/DataTable/DT_UnitActionMetaData"
        }

        self.level_data_config = {
            "module": level_data,
            "sheet_id": "1jeq0WdGMsOcAEtW_p__-daOn22ZFoCm67UWgLh6p6CA",
            "gid": "301417934",
            "table_path": "/Game/Core/DataTable/DT_LevelData"
        }

        self.scene_level_data_config = {
            "module": scene_level_data,
            "sheet_id": "19t28YoMTYX6jrA8tW5mXvsu7PMjUNco7VwQirzImmIE",
            "gid": "810949862",
            "table_path": "/Game/Core/DataTable/Maps/DT_SceneLevelData"
        }

        self.facial_key_gameplay_tags_config = {
            "module": facial_key_gameplay_tags,
            "sheet_id": "1E7VdiW8OndnToXPbxmhxW9a1quoOY1PqHIjNMZ5n5hg",
            "gid": "1098136304",
            "table_path": "/Game/Core/DataTable/GameplayTags/DT_TagDef_FacialKey"
        }

        self.action_key_gameplay_tags_config = {
            "module": action_key_gameplay_tags,
            "sheet_id": "1IPkguLmxUeet2eDBQ5itDTwch-36CFxZ-gYn6AmMlnE",
            "gid": "1018530766",
            "table_path": "/Game/Core/DataTable/GameplayTags/DT_TagDef_ActionKey"
        }

        self.prop_asset_config = {
            "module": prop_asset,
            "sheet_id": "1as2q_Me31jXwfMA6yFF3r6PrZxd0MREjSMGZRmfjcOg",
            "gid": "1372236030",
            "table_path": "/Game/Core/DataTable/DT_PropAsset"
        }

        self.tables = {
            "메타 액션": self.meta_action_config,
            "캐릭터 프리셋": self.character_preset_config,
            "유닛 액션 메타데이터": self.unit_action_metadata_config,
            "레벨 데이터": self.level_data_config,
            "씬 레벨 데이터": self.scene_level_data_config,
            "표정 키 게임플레이 태그": self.facial_key_gameplay_tags_config,
            "액션 키 게임플레이 태그": self.action_key_gameplay_tags_config,
            "프롭 에셋": self.prop_asset_config,
        }

        # tables 딕셔너리 생성 후 GUI 컴포넌트 생성
        self.create_gui_components()

        # GUI 컴포넌트 생성 후 모듈 리로드
        self.reload_modules()

        self.log("언리얼 엔진 버전: " + unreal.SystemLibrary.get_engine_version())

        self.history = ImportHistory()

        # 텍스트 태그 설정 (굵은 글씨용)
        self.log_text.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))

        # 에디터 서브시스템 초기화
        editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
        if not editor_subsystem:
            print("에디터 서브시스템을 찾을 수 없습니다.")
            return

    def create_gui_components(self):
        self.window = ttk.Frame(self)
        self.window.pack(fill=tk.BOTH, padx=10, pady=5)

        # 전체 선택 체크박스 추가
        select_all_frame = ttk.Frame(self.window)
        select_all_frame.pack(fill=tk.X, pady=2)

        self.select_all_var = tk.BooleanVar(value=False)
        select_all_checkbox = ttk.Checkbutton(
            select_all_frame,
            text="전체 선택",
            variable=self.select_all_var,
            command=self.toggle_all_tables
        )
        select_all_checkbox.pack(side=tk.LEFT)

        # 구분선 추가
        ttk.Separator(self.window, orient='horizontal').pack(fill=tk.X, pady=5)

        # 기존 테이블 체크박스들
        self.table_vars = {}
        self.checkbuttons = {}

        # 각 테이블에 대한 체크박스와 정보 표시
        for table_name, info in self.tables.items():
            table_frame = ttk.Frame(self.window)
            table_frame.pack(fill=tk.X, pady=2)

            # 체크박스 생성
            var = tk.BooleanVar(value=False)
            self.table_vars[table_name] = var

            # 체크박스 상태 변경 시 호출될 함수
            def on_checkbox_changed(*args, table_name=table_name):
                self.update_select_all_state()

            # 체크박스 이벤트 연결
            var.trace_add('write', on_checkbox_changed)

            checkbox = ttk.Checkbutton(
                table_frame,
                text=table_name,
                variable=var
            )
            checkbox.pack(side=tk.LEFT)
            self.checkbuttons[table_name] = checkbox

            # 테이블 경로 표시
            ttk.Label(
                table_frame,
                text=f"→ {info['table_path']}",
                foreground="gray"
            ).pack(side=tk.LEFT, padx=10)

            # Sheet ID와 GID 표시
            if info['sheet_id'] and info['gid']:
                ttk.Label(
                    table_frame,
                    text=f"(Sheet ID: {info['sheet_id']}, GID: {info['gid']})",
                    foreground="gray"
                ).pack(side=tk.LEFT)

        # 체크박스 의존성 설정
        self.setup_checkbox_dependencies()

        # 상태 표시 레이블
        self.status_label = tk.Label(self.window, text="", wraplength=700)
        self.status_label.pack(pady=10)

        # 로그 프레임
        log_frame = ttk.LabelFrame(self.window, text="작업 내역", padding="10")
        log_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 스크롤바와 텍스트를 포함할 프레임
        text_frame = ttk.Frame(log_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # 스크롤바 (우측에 배치)
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 로그 텍스트
        self.log_text = tk.Text(text_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # 스크롤바 연결
        self.log_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.log_text.yview)

        # 버튼 프레임
        button_frame = ttk.Frame(self.window, padding="10")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(
            button_frame,
            text="선택한 테이블 임포트",
            command=self.import_selected_tables,
            width=30
        ).pack(side=tk.RIGHT)

        # 사용 설명 추가
        usage_frame = ttk.LabelFrame(self.window, text="사용 방법", padding="10")
        usage_frame.pack(fill=tk.X, padx=10, pady=5)

        usage_text = """
1. 변환하고 싶은 데이터 테이블을 선택하세요:
   - 전체 선택 체크박스를 사용하여 모든 테이블을 한 번에 선택할 수 있습니다.
   - 개별적으로 원하는 테이블만 선택할 수도 있습니다.
   - '씬 레벨 데이터'를 선택하면 자동으로 '레벨 데이터'도 함께 선택됩니다.

2. '선택한 테이블 임포트' 버튼을 클릭하여 변환을 시작하세요.

3. 아래 작업 내역에서 진행 상황을 확인할 수 있습니다.
        """

        ttk.Label(usage_frame, text=usage_text, justify=tk.LEFT).pack(anchor=tk.W)

    def reload_modules(self):
        """모듈 리로드"""
        try:
            # 먼저 sys.modules에서 관련 모듈 제거
            module_names = [
                'scripts.tables.meta_action',
                'scripts.tables.character_preset',
                'scripts.tables.unit_action_metadata',
                'scripts.tables.level_data',
                'scripts.tables.scene_level_data',
                'scripts.tables.facial_key_gameplay_tags',
                'scripts.tables.action_key_gameplay_tags'
            ]

            for module_name in module_names:
                if module_name in sys.modules:
                    del sys.modules[module_name]

            # 모듈 다시 임포트
            from scripts.tables import meta_action, character_preset, unit_action_metadata, level_data, scene_level_data, facial_key_gameplay_tags, action_key_gameplay_tags

            # 설정 업데이트
            self.tables["메타 액션"]["module"] = meta_action
            self.tables["캐릭터 프리셋"]["module"] = character_preset
            self.tables["유닛 액션 메타데이터"]["module"] = unit_action_metadata
            self.tables["레벨 데이터"]["module"] = level_data
            self.tables["씬 레벨 데이터"]["module"] = scene_level_data
            self.tables["표정 키 게임플레이 태그"]["module"] = facial_key_gameplay_tags
            self.tables["액션 키 게임플레이 태그"]["module"] = action_key_gameplay_tags

            self.log("모듈 리로드 완료")
        except Exception as e:
            self.log(f"모듈 리로드 실패: {str(e)}")

    def refresh_unreal_editor(self):
        """언리얼 에디터 새로고침"""
        try:
            # UE 5.x 버전용
            editor_subsystem = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
            editor_subsystem.refresh_all_browsers()
            self.log("에디터 새로고침 완료")
        except:
            # 실패해도 메시지를 표시하지 않음
            pass

    def log(self, message):
        """로그 메시지 추가"""
        # 개발 관련 메시지 필터링
        if any(skip in message for skip in [
            "모듈 리로드",
            "언리얼 엔진 버전",
            "테이블 정보:",
            "Sheet ID:",
            "GID:",
            "테이블 경로:"
        ]):
            return

        # 사용자 친화적인 메시지로 변환
        if "=== 임포트 시작 ===" in message:
            table_name = message.split(" 임포트")[0].replace("=== ", "")
            message = f"\n📋 {table_name} 데이터 변환을 시작합니다..."
        elif "임포트 완료:" in message:
            count = message.split(":")[1].strip()
            message = f"✅ 성공적으로 변환되었습니다! {count}\n"
            # 굵은 글씨로 표시
            self.log_text.insert(tk.END, message, "bold")
            self.log_text.see(tk.END)
            return
        elif "오류 발생:" in message:
            message = f"❌ 변환 중 문제가 발생했습니다: {message.split(':')[1]}"

        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)

    def import_selected_tables(self):
        """선택된 테이블들 임포트"""
        # 먼저 모듈들을 리로드
        self.reload_modules()

        selected_tables = []
        # 먼저 레벨 데이터가 필요한 테이블들을 확인
        needs_level_data = False
        for name, var in self.table_vars.items():
            if var.get() and name == "씬 레벨 데이터":
                needs_level_data = True
                break

        # 테이블 선택 처리
        for name, var in self.table_vars.items():
            if var.get():
                # 레벨 데이터가 필요한 경우 먼저 추가
                if needs_level_data and name == "레벨 데이터":
                    selected_tables.append(name)
                # 씬 레벨 데이터 추가
                elif name == "씬 레벨 데이터":
                    selected_tables.append(name)
                # 다른 테이블들 추가 (레벨 데이터는 제외)
                elif name != "레벨 데이터":
                    selected_tables.append(name)

        if not selected_tables:
            messagebox.showwarning("경고", "임포트할 테이블을 선택해주세요.")
            return

        # 전체 진행 상황을 표시하는 SlowTask 생성
        total_tables = len(selected_tables)
        with unreal.ScopedSlowTask(total_tables, "데이터 테이블 임포트 중...") as slow_task:
            slow_task.make_dialog(True)  # 진행 상황 다이얼로그 표시

            for i, table_name in enumerate(selected_tables):
                # 현재 테이블 진행 상황 업데이트
                slow_task.enter_progress_frame(1, f"{table_name} 임포트 중... ({i+1}/{total_tables})")

                self.log(f"\n=== {table_name} 임포트 시작 ===")
                try:
                    table_info = self.tables[table_name]

                    # 디버깅 정보 추가
                    self.log(f"테이블 정보:")
                    self.log(f"- Sheet ID: {table_info['sheet_id']}")
                    self.log(f"- GID: {table_info['gid']}")
                    self.log(f"- 테이블 경로: {table_info['table_path']}")

                    # character_preset은 다른 함수 이름을 사용
                    if table_name == "캐릭터 프리셋":
                        result = table_info["module"].import_table(
                            table_info["sheet_id"],
                            table_info["gid"]
                        )
                    else:
                        # 모듈의 임포트 함수 호출
                        result = table_info["module"].import_table(
                            table_info["sheet_id"],
                            table_info["gid"]
                        )

                    # 결과 처리
                    if isinstance(result, dict):
                        if result.get('success'):
                            count = result.get('count', 0)
                            self.history.add_entry(table_name, count)
                            self.log(f"임포트 완료: {count}개의 행이 처리되었습니다.")
                        else:
                            error = result.get('error', '알 수 없는 오류')
                            self.log(f"임포트 실패: {error}")
                    elif isinstance(result, tuple):
                        success, count = result
                        if success:
                            self.history.add_entry(table_name, count)
                            self.log(f"임포트 완료: {count}개의 행이 처리되었습니다.")
                        else:
                            self.log(f"임포트 실패: {count}")
                    else:
                        self.log("알 수 없는 결과 형식")

                except Exception as e:
                    self.log(f"오류 발생: {str(e)}")
                    import traceback
                    self.log(traceback.format_exc())

                # 사용자가 취소했는지 확인
                if slow_task.should_cancel():
                    self.log("사용자가 임포트를 취소했습니다.")
                    break

        # 모든 테이블 임포트 후 에디터 새로고침
        self.refresh_unreal_editor()

    def on_scene_level_data_checked(self, checked):
        """DT_SceneLevelData 체크박스 이벤트 핸들러"""
        level_data_checkbox = self.find_checkbox("DT_LevelData")
        if level_data_checkbox:
            level_data_checkbox.setChecked(checked)
            level_data_checkbox.setEnabled(not checked)

    def on_level_data_checked(self, checked):
        """DT_LevelData 체크박스 이벤트 핸들러"""
        scene_level_data_checkbox = self.find_checkbox("DT_SceneLevelData")
        if scene_level_data_checkbox and scene_level_data_checkbox.isChecked():
            return False  # 체크 해제 방지
        return True

    def setup_checkbox_dependencies(self):
        """체크박스 의존성 설정"""
        scene_level_var = self.table_vars.get("씬 레벨 데이터")
        level_data_var = self.table_vars.get("레벨 데이터")

        if scene_level_var and level_data_var:
            def on_scene_level_changed(*args):
                is_checked = scene_level_var.get()
                # 레벨 데이터 체크박스 처리
                level_data_checkbox = self.checkbuttons.get("레벨 데이터")
                if level_data_checkbox:
                    if is_checked:
                        level_data_var.set(True)
                        level_data_checkbox.state(['disabled'])
                    else:
                        level_data_checkbox.state(['!disabled'])
                        level_data_var.set(False)  # 씬 레벨 데이터 체크 해제시 레벨 데이터도 체크 해제

            def on_level_data_changed(*args):
                # 씬 레벨 데이터가 체크된 상태에서는 레벨 데이터 체크 해제 방지
                if scene_level_var.get() and not level_data_var.get():
                    level_data_var.set(True)

            # 이벤트 연결
            scene_level_var.trace_add('write', on_scene_level_changed)
            level_data_var.trace_add('write', on_level_data_changed)

    def update_select_all_state(self):
        """모든 테이블의 체크 상태를 확인하여 전체 선택 체크박스 상태 업데이트"""
        all_checked = all(var.get() for var in self.table_vars.values())
        self.select_all_var.set(all_checked)

    def toggle_all_tables(self):
        """전체 선택/해제 토글"""
        is_checked = self.select_all_var.get()

        # 전체 해제할 때는 씬 레벨 데이터를 먼저 해제
        if not is_checked:
            scene_level_var = self.table_vars.get("씬 레벨 데이터")
            if scene_level_var:
                scene_level_var.set(False)

        # 나머지 테이블들의 상태 변경
        for table_name, var in self.table_vars.items():
            var.set(is_checked)

            # 레벨 데이터 체크박스 상태 처리
            if table_name == "레벨 데이터":
                checkbox = self.checkbuttons.get(table_name)
                if checkbox:
                    if not is_checked:
                        checkbox.state(['!disabled'])  # 활성화
                        var.set(False)  # 강제로 체크 해제
                    elif is_checked and self.table_vars.get("씬 레벨 데이터", tk.BooleanVar()).get():
                        checkbox.state(['disabled'])

def validate_asset_path(asset_path):
    if not asset_path:
        return True

    asset = unreal.load_asset(asset_path)
    return asset is not None

def validate_thumbnail_path(path):
    if not path or path.strip() == "":
        return True  # 빈 경로는 유효하다고 처리

    # /Game/ 으로 시작하지 않는 경로 처리
    if not path.startswith("/Game/"):
        path = f"/Game/{path}"

    asset = unreal.load_asset(path)
    return asset is not None

def checkout_and_make_writable(asset_path):
    """에셋을 소스 컨트롤에서 checkout하고 쓰기 가능하게 만듦"""
    try:
        # 에셋이 존재하는지 확인
        if not unreal.EditorAssetLibrary.does_asset_exist(asset_path):
            print(f"에셋이 존재하지 않음: {asset_path}")
            return False

        # 에셋 로드
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        if not asset:
            print(f"에셋을 로드할 수 없음: {asset_path}")
            return False

        # 에셋의 실제 파일 경로 가져오기
        package_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
        if not package_path:
            print(f"에셋 경로를 찾을 수 없음: {asset_path}")
            return False

        # 파일 쓰기 가능하게 만들기
        if not set_file_writable(package_path):
            print(f"파일을 쓰기 가능하게 만들 수 없음: {package_path}")
            return False

        print(f"에셋이 쓰기 가능하게 설정됨: {asset_path}")
        return True
    except Exception as e:
        print(f"에셋 설정 중 오류 발생: {str(e)}")
        return False

def import_table(sheet_id, sheet_name, data_table_path):
    try:
        with unreal.ScopedSlowTask(100, "데이터 테이블 업데이트 중...") as slow_task:
            slow_task.make_dialog(True)

            # 구글 시트 데이터 가져오기
            slow_task.enter_progress_frame(20, "구글 시트에서 데이터 로딩 중...")
            worksheet = get_worksheet(sheet_id, sheet_name)
            if worksheet is None:
                return False

            # 데이터 유효성 검사
            slow_task.enter_progress_frame(20, "썸네일 경로 검증 중...")
            invalid_paths = []
            records = worksheet.get_all_records()
            for row in records:
                if 'ThumbnailPath' in row:
                    thumb_path = row['ThumbnailPath']
                    if thumb_path and not validate_thumbnail_path(thumb_path):
                        invalid_paths.append(thumb_path)

            if invalid_paths:
                error_msg = "다음 썸네일 경로가 존재하지 않습니다:\n" + "\n".join(invalid_paths)
                unreal.log_warning(error_msg)
                # 계속 진행할지 사용자에게 물어보기
                if not unreal.EditorDialog.show_message(
                    "경고",
                    f"{len(invalid_paths)}개의 썸네일 경로가 유효하지 않습니다.\n계속 진행하시겠습니까?",
                    "YesNo"  # 문자열로 변경
                ):
                    return False

            # 잠시 대기하여 프로그레스 바가 보이도록
            unreal.SystemLibrary.delay(None, 0.1)

            # CSV 파일 생성 (25%)
            slow_task.enter_progress_frame(25, "CSV 파일 생성 중...")
            temp_csv_path = create_temp_csv(worksheet)
            if not temp_csv_path:
                return False

            # 데이터 테이블 업데이트 (25%)
            slow_task.enter_progress_frame(25, "데이터 테이블 업데이트 중...")
            data_table = load_data_table(data_table_path)
            if not data_table:
                return False

            # 임포트 실행 및 마무리 (25%)
            slow_task.enter_progress_frame(25, "데이터 임포트 완료 중...")
            success = import_csv_to_data_table(temp_csv_path, data_table)

            # 임시 파일 삭제
            try:
                os.remove(temp_csv_path)
                unreal.log("임시 파일 삭제됨: " + temp_csv_path)
            except:
                pass

            return success

    except Exception as e:
        unreal.log_error(f"데이터 테이블 업데이트 중 오류 발생: {str(e)}")
        return False

def main():
    if not check_unreal_environment():
        messagebox.showerror("오류", "이 스크립트는 언리얼 에디터 내에서 실행해야 합니다.")
        sys.exit(1)

    app = DataTableImporter()
    app.mainloop()

if __name__ == "__main__":
    main()