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

def get_component_by_class(blueprint_to_find_components, component_class_to_find):
    components = []
    asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects = get_component_objects(asset_path)
    for each in component_objects:
        compare_class = (each.__class__ == component_class_to_find)
        if compare_class :
            components.append(each)
    return components

## 함수 선언부 

base_bp : str   = '/Game/TA/Users/Narr/_BP_Customisable'
actor_comp_assets = [] 



asset_list = unreal.EditorUtilityLibrary.get_selected_assets() # selected Editor Asset List 

asset_need_to_change = asset_list[0]
path_asset_need_to_change = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset_need_to_change)
comp_objs = get_component_objects(path_asset_need_to_change)
__static_mesh_component_to_change__ = comp_objs[2]

smesh_asset = __static_mesh_component_to_change__.get_editor_property('static_mesh')

component_objects = get_component_objects(base_bp)
static_mesh_comp = component_objects[1]
destination = path_asset_need_to_change


try:
    unreal.EditorAssetLibrary.delete_asset(destination)
    print('old asset deleted')
except:
    print('no pre-generated Asset')
static_mesh_comp.set_editor_property('static_mesh', smesh_asset)
duplicated_bp = unreal.EditorAssetLibrary.duplicate_asset(base_bp,destination)
