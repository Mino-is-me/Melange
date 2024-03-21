import unreal 
selected : list = unreal.EditorUtilityLibrary.get_selected_assets()

def setNaniteSetting (__selected : list ) -> bool :  
    fallbackTrianglePercent = unreal.GeometryScriptNaniteOptions(fallback_percent_triangles = 10.0)
    # fallbackTrianglePercent = 0.1

    for asset in __selected:
        meshNaniteSettings = asset.get_editor_property('nanite_settings')
        if meshNaniteSettings.enabled == True:
            meshNaniteSettings.fallback_percent_triangles = 0.1
            meshNaniteSettings.keep_percent_triangles = 0.1
            unreal.StaticMeshEditorSubsystem().set_nanite_settings(asset, meshNaniteSettings, apply_changes=True)
        # unreal.MeshNaniteSettings.set_editor_property(asset, fallbackTrianglePercent)       
    
    return True


setNaniteSetting(selected)

del selected 



