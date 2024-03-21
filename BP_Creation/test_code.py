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

def get_component_by_var_name(blueprint_to_find_components : unreal.Blueprint, component_name_to_find : str) :
    components = []
    asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects = get_component_objects(asset_path)

    for each in component_objects:
        compare_name = (each.get_name()) == ( component_name_to_find + '_GEN_VARIABLE' )
        if compare_name :
            components.append(each)
    return components

## 함수 선언부 

##TestCode Start 
asset_list = unreal.EditorUtilityLibrary.get_selected_assets()
asset = asset_list[0]

StaticMeshComps = get_component_by_class(asset, unreal.StaticMeshComponent)
TempComp = get_component_by_var_name(asset, 'BP_InteractionPointComponent1')

print(TempComp)