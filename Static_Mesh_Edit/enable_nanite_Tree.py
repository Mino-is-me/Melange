
import unreal 
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)

selected : list = topaz.get_selected_assets() #get selected assets using editorUtilityLib

for staticMesh in selected : 
    meshNaniteSettings : bool = staticMesh.get_editor_property('nanite_settings')
    blendModes = topaz.get_materials_from_staticmesh(staticMesh, True)
    is_translucent_exist = topaz.is_translucent_exist(blendModes)
    nanite_settings = unreal.MeshNaniteSettings

    if meshNaniteSettings.enabled == True and nanite_settings.preserve_area == False :
        nanite_settings.set_editor_property('preserve_area', True) 
        unreal.StaticMeshEditorSubsystem().set_nanite_settings(staticMesh,meshNaniteSettings, apply_changes=True) #apply changes
        print('Preserve Area is Enabled.')
        

    
    else :
        meshNaniteSettings.enabled == False and not is_translucent_exist
        meshNaniteSettings.enabled = True # On nanite setting
        nanite_settings : unreal.MeshNaniteSettings     = staticMesh.get_editor_property('nanite_settings')
        nanite_settings.enabled = True
        nanite_settings.set_editor_property('preserve_area', True) 
        unreal.StaticMeshEditorSubsystem().set_nanite_settings(staticMesh,meshNaniteSettings, apply_changes=True) #apply changes
        print('Nanite is Enabled and Preserve Area is Enabled.')
