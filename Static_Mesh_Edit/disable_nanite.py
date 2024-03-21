import unreal 
selected : list = unreal.EditorUtilityLibrary.get_selected_assets() #get selected assets using editorUtilityLib

for staticMesh in selected : 
    meshNaniteSettings : bool = staticMesh.get_editor_property('nanite_settings')
    print 
    if meshNaniteSettings.enabled : #if true
        meshNaniteSettings.enabled = False #off nanite setting 
        unreal.StaticMeshEditorSubsystem().set_nanite_settings(staticMesh,meshNaniteSettings, apply_changes=True)
    else :
        print('Nanite is Disabled')