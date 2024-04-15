

import unreal
import math

def get_viewport_camera() -> tuple[unreal.Vector, unreal.Rotator]:
    viewport_cam_info = unreal.EditorLevelLibrary.get_level_viewport_camera_info()
    return viewport_cam_info

viewport_camera_info = get_viewport_camera()

if viewport_camera_info:
    # 카메라의 위치 정보를 가져옴
    camera_position = viewport_camera_info[0]
    # 카메라의 회전 정보를 가져옴
    camera_rotation = viewport_camera_info[1]
    camera_rotation.yaw += 180  # Yaw 회전값에 180도 추가

    # 카메라 회전을 기반으로 회전된 방향 벡터를 계산 (앞쪽 방향)
    forward_vector = unreal.Vector(math.cos(math.radians(camera_rotation.yaw)) * math.cos(math.radians(camera_rotation.pitch)),
                                   math.sin(math.radians(camera_rotation.yaw)) * math.cos(math.radians(camera_rotation.pitch)),
                                   math.sin(math.radians(camera_rotation.pitch)))

    # 이동할 거리 설정
    offset_distance = -300.0
    
    # 이동할 거리만큼 앞으로 이동한 위치 계산, Pitch 값에 10을 곱하여 Z축 조정
    z_adjust = math.sin(math.radians(camera_rotation.pitch)) * 500
    spawn_position = camera_position + forward_vector * offset_distance
    spawn_position.z += z_adjust

    # 레퍼볼 블루프린트 클래스 로드
    actor_class = unreal.EditorAssetLibrary.load_blueprint_class('/Game/Environment/BP_RefBall.BP_RefBall')

    # 수정된 위치와 회전을 사용하여 액터 스폰
    spawn_actor = unreal.EditorLevelLibrary.spawn_actor_from_class(actor_class, spawn_position, camera_rotation)






