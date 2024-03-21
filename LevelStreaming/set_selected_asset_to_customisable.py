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


asset_list = unreal.EditorUtilityLibrary.get_selected_assets() # selected Editor Asset List 

asset = asset_list[0]

if len(asset_list) > 0 : 
        for each in asset_list : 
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
