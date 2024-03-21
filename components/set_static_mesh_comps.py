import unreal

def get_component_handles(blueprint_asset_path): ## 사용안해도됨, 다음 함수에서 호출해서 사용하는 함수, 핸들러 직접 물고싶으면 쓰셈 
    subsystem = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)

    blueprint_asset = unreal.load_asset(blueprint_asset_path)
    subobject_data_handles = subsystem.k2_gather_subobject_data_for_blueprint(blueprint_asset)
    return subobject_data_handles

def get_component_objects(blueprint_asset_path : str): ## 컴포넌트 무식하게 다 긁어줌 
    objects = []
    handles = get_component_handles(blueprint_asset_path)
    for handle in handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data)
        objects.append(object)
    return objects

def get_component_by_class(blueprint_to_find_components : unreal.Blueprint, component_class_to_find : unreal.Class): ## 컴포넌트중에 클래스 맞는것만 리턴해줌 
    components : list[unreal.Object]    = []
    asset_path : list[str]              = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects = get_component_objects(asset_path)
    for each in component_objects:
        compare_class = (each.__class__ == component_class_to_find)
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


def cutoff_nanite_tri(_static_mesh_ : unreal.StaticMesh) :
    if _static_mesh_ is not None :
        tri = _static_mesh_.get_num_triangles(0)
        apprx_nanite_tri = tri * 27 
        if apprx_nanite_tri > 1000000 : 
            __desired_triangle_percentage__ = 0.09
        else :
            __desired_triangle_percentage__ = 0.25
    return __desired_triangle_percentage__


assets = unreal.EditorUtilityLibrary.get_selected_assets()
## execution here ##
#__desired_triangle_percentage__ : float = 0.33

assets = unreal.EditorUtilityLibrary.get_selected_assets()
## execution here ##
for each in assets :
    if each.__class__ == unreal.Blueprint : 
        comps = get_component_by_class(each, unreal.StaticMeshComponent)
        for comp in comps :
            static_mesh     : unreal.StaticMesh                 = comp.static_mesh
            if static_mesh is not None : 

                __desired_triangle_percentage__ = cutoff_nanite_tri(static_mesh)

                nanite_settings : unreal.MeshNaniteSettings     = static_mesh.get_editor_property('nanite_settings')
                nanite_settings.enabled = True
                nanite_settings.keep_percent_triangles = __desired_triangle_percentage__ 
                static_mesh.set_editor_property('nanite_settings', nanite_settings)
            #print(nanite_settings.keep_percent_triangles)
                
    if each.__class__ == unreal.StaticMesh : 
        if each is not None : 

            __desired_triangle_percentage__ = cutoff_nanite_tri(each)

            nanite_settings : unreal.MeshNaniteSettings     = each.get_editor_property('nanite_settings')
            nanite_settings.enabled = True
            nanite_settings.set_editor_property('keep_percent_triangles', __desired_triangle_percentage__) 
            each.set_editor_property('nanite_settings', nanite_settings)



print('OK')