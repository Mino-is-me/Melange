import unreal
import urllib.request
import json
import os
import stat

def check_unreal_environment():
    """언리얼 환경에서 실행 중인지 확인"""
    try:
        engine_version = unreal.SystemLibrary.get_engine_version()
        print(f"언리얼 엔진 버전: {engine_version}")
        return True
    except Exception as e:
        print(f"오류: 이 스크립트는 언리얼 에디터 내에서 실행해야 합니다. {str(e)}")
        return False

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

def set_file_writable(file_path):
    """파일을 쓰기 가능한 상태로 변경"""
    try:
        # 현재 파일 권한 가져오기
        current_permissions = os.stat(file_path).st_mode

        # 쓰기 권한 추가
        new_permissions = current_permissions | stat.S_IWRITE

        # 권한 변경
        os.chmod(file_path, new_permissions)
        return True
    except Exception as e:
        print(f"파일 권한 변경 중 에러 발생: {str(e)}")
        return False