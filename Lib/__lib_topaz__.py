import unreal

def __test__():
    unreal.log('Topaz Test')

def get_component_handles(blueprint_asset_path) -> unreal.Subsystem : ## 사용안해도됨, 다음 함수에서 호출해서 사용하는 함수, 핸들러 직접 물고싶으면 쓰셈 
    subsystem               : unreal.Subsystem      = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    blueprint_asset         : unreal.Blueprint      = unreal.load_asset(blueprint_asset_path)
    subobject_data_handles  : unreal.Subsystem      = subsystem.k2_gather_subobject_data_for_blueprint(blueprint_asset)

    return subobject_data_handles

def get_component_objects(blueprint_asset_path : str) -> list[unreal.Object] : ## 컴포넌트 무식하게 다 긁어줌 
    objects : list[unreal.SubobjectDataSubsystem]                          = [] # init 
    handles : unreal.SubobjectDataHandle                                   = get_component_handles(blueprint_asset_path)
    for handle in handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data) 
        objects.append(object)

    return objects

def get_component_by_class(blueprint_to_find_components : unreal.Blueprint, component_class_to_find : unreal.Class) -> list[unreal.Object] : ## 컴포넌트중에 클래스 맞는것만 리턴해줌 
    components = []
    asset_path          : list[str]             = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects   : list[unreal.Class]    = get_component_objects(asset_path)

    for each in component_objects:
        compare_class : bool = (each.__class__ == component_class_to_find)
        if compare_class :
            components.append(each)

    return components

def get_component_by_var_name(blueprint_to_find_components : unreal.Blueprint, component_name_to_find : str) : ##컴포넌트 이름으로 찾음 
    components = []
    asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects = get_component_objects(asset_path)

    for each in component_objects:
        compare_name = (each.get_name()) == ( component_name_to_find + '_GEN_VARIABLE' )
        if compare_name :
            components.append(each)

    return components

def get_selected_assets() -> list[unreal.Object]: #리스트로 선택된 오브젝트 리턴
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    return assets

def get_selected_asset() -> unreal.Object: #단일 선택 오브젝트 리턴 
    assets = get_selected_assets()
    if len(assets) > 0:
        return assets[0]
    else:
        return None
    
def get_selected_level_actors() -> list[unreal.Actor]: #리스트로 선택된 액터 리턴 
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    return actors

def get_selected_level_actor() -> unreal.Actor: #단일 액터 리턴 
    actors = get_selected_level_actors()
    if len(actors) > 0:
        return actors[0]
    else:
        return None

def cutoff_nanite_tri(_static_mesh_ : unreal.StaticMesh) -> float : #나나이트가 특정 트라이 이상일때 나나이트 트라이 퍼센테이지 리턴해줌, legacy
    if _static_mesh_ is not None :
        tri = _static_mesh_.get_num_triangles(0)
        apprx_nanite_tri = tri * 27 
        if apprx_nanite_tri > 1000000 : 
            __desired_triangle_percentage__ = 0.09
        else :
            __desired_triangle_percentage__ = 0.25
    return __desired_triangle_percentage__

def set_actor_tag_by_class(actor : unreal.Actor, seek_class : unreal.Class, desired_tag : str) : #액터에 태그 추가
    actor_tags = actor.tags
    print(actor.get_class())
    if desired_tag not in actor_tags : 
        if actor.__class__ == seek_class :
            print('Tag Added')
            actor_tags.append(desired_tag)
            actor.set_actor_tags(actor_tags)
        else :
            print('Tag Not Added')

def get_materials_from_staticmesh (static_mesh : unreal.StaticMesh, only_blend_mode : bool ) -> list[unreal.MaterialInterface] : #스태틱메쉬에서 메테리얼 리스트로 리턴 
    materials = []
    blendmodes = []
    for i in range(static_mesh.get_num_sections(0)):
        materials.append(static_mesh.get_material(i))
        blendmodes.append(static_mesh.get_material(i).get_blend_mode())
    if only_blend_mode :
        return blendmodes
    else :
        return materials
    
def is_translucent_exist(blendmodes : list[unreal.BlendMode]) -> bool : #트랜스루센트가 있는지 확인
    for blendmode in blendmodes :
        if blendmode == unreal.BlendMode.BLEND_TRANSLUCENT :
            return True
    return False

def get_assets_in_folder(folder_path : str) -> list[str]: #폴더안에 있는 에셋들 리스트로 리턴 
    assets = unreal.EditorAssetLibrary.list_assets(folder_path, True, False)
    return assets

def get_asset_filepath(asset : unreal.Object) -> str: #에셋파일 경로 리턴 
    asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
    return asset_path

def get_cooked_dir () -> str : #Saved 디렉토리 리턴 
    saved_dir = unreal.Paths.project_saved_dir()
    cooked_dir = saved_dir + 'Cooked/Windows'
    print(cooked_dir)
    return cooked_dir


def disable_ray_tracing(static_mesh : unreal.StaticMesh) -> None : #레이트레이싱 끄기
    is_ray_tracing = static_mesh.get_editor_property('support_ray_tracing')
    if is_ray_tracing :
        static_mesh.set_editor_property('support_ray_tracing', False)
        print(static_mesh.get_editor_property('support_ray_tracing'))

###Initialised message when loaded ###
unreal.log('Topaz initialised...')
