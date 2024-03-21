import unreal



def get_component_handles(blueprint_asset_path):
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)

    blueprint_asset = unreal.load_asset(blueprint_asset_path)
    subobject_data_handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint_asset)
    return subobject_data_handles

def get_component_objects(blueprint_asset_path):
    objects = []
    handles = get_component_handles(blueprint_asset_path)
    for handle in handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        objects.append(object)
    return objects

## 함수 선언부 

base_bp : str   = '/Game/TA/Users/Narr/_BP_Customisable'
actor_comp_assets = []



level_actors = unreal.EditorLevelLibrary.get_selected_level_actors() # 레벨에서 액터 선택했을 경우 

actor_comp = level_actors[0].get_editor_property('static_mesh_component')
actor_comp_asset = actor_comp.get_editor_property('static_mesh')
actor_comp_assets.append(actor_comp_asset)
if len(level_actors) > 0 : #레벨 Actor를 Select했을 경우 
    for each in actor_comp_assets : 
        component_objects = get_component_objects(base_bp)
        static_mesh_comp = component_objects[1]
        __static_mesh__ = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(each)
        __static_mesh_path_ = __static_mesh__.rsplit('/', 1)[0]
        __static_mesh_name_ = __static_mesh__.rsplit('/', 1)[1]
        __static_mesh_name_ = __static_mesh_name_.rsplit('.',1)[0]
        __static_mesh_name_ = __static_mesh_name_.replace('SM_','BP_')
        destination = __static_mesh_path_ + '/' + __static_mesh_name_
        try:
            unreal.EditorAssetLibrary.delete_asset(destination)
        except:
            print('no pre-generated Asset')
        static_mesh_comp.set_editor_property('static_mesh',each)
        duplicated_bp = unreal.EditorAssetLibrary.duplicate_asset(base_bp,destination)
