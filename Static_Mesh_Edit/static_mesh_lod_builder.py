import unreal 
## global statements start ##
selected : list = unreal.EditorUtilityLibrary.get_selected_assets() #get selected assets using editorUtilityLib
## global statements end ##


def static_mesh_lod_builder (__asssets : list ) -> bool :  
    lod_0 = unreal.EditorScriptingMeshReductionSettings(percent_triangles=1, screen_size=1)
    lod_1 = unreal.EditorScriptingMeshReductionSettings(percent_triangles=0.5, screen_size=0.5)
    lod_2 = unreal.EditorScriptingMeshReductionSettings(percent_triangles=0.25, screen_size=0.25)
    lod_3 = unreal.EditorScriptingMeshReductionSettings(percent_triangles=0.1, screen_size=0.1)
    lod_4 = unreal.EditorScriptingMeshReductionSettings(percent_triangles=0, screen_size=0.05)
    
    lo_ds = [lod_0, lod_1, lod_2, lod_3, lod_4]
    wrapped_reduction_option = unreal.EditorScriptingMeshReductionOptions(True, lo_ds)
    for each in __asssets :
        unreal.EditorStaticMeshLibrary.set_lods(each, wrapped_reduction_option)
        unreal.EditorStaticMeshLibrary.enable_section_cast_shadow(each, True, 0, 0)
        unreal.EditorStaticMeshLibrary.enable_section_cast_shadow(each, False, 1, 0)
        unreal.EditorStaticMeshLibrary.enable_section_cast_shadow(each, False, 2, 0)
        unreal.EditorStaticMeshLibrary.enable_section_cast_shadow(each, False, 3, 0)
        unreal.EditorStaticMeshLibrary.enable_section_cast_shadow(each, False, 4, 0)

        unreal.EditorAssetLibrary.save_loaded_asset(each)  ## save Loaded Asset in Iterator 
    return True 

static_mesh_lod_builder(selected)

#Memory Free here 
del selected 



