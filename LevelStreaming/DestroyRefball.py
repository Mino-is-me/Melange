import unreal

# 삭제할 블루프린트 액터의 경로
blueprint_path = '/Game/Environment/BP_RefBall.BP_RefBall'

# 삭제할 액터 클래스의 레퍼런스 얻기
actor_class_ref = unreal.EditorAssetLibrary.load_blueprint_class(blueprint_path)

# 레벨의 모든 액터를 가져오기
actors = unreal.EditorLevelLibrary.get_all_level_actors()

# 액터들을 반복 처리하며, 특정 액터 찾기
for actor in actors:
    # 액터의 클래스를 가져옴
    actor_class = actor.get_class()
    
    # 액터의 클래스와 삭제할 블루프린트의 클래스가 일치하는지 확인
    if actor_class == actor_class_ref:
        # 액터 파괴
        unreal.EditorLevelLibrary.destroy_actor(actor)

print("All BP_RefBall actors destroyed.")
