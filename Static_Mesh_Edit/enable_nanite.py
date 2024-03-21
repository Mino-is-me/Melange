import unreal 
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)

selected : list = topaz.get_selected_assets() #get selected assets using editorUtilityLib

for staticMesh in selected : 
    meshNaniteSettings : bool = staticMesh.get_editor_property('nanite_settings')
    blendModes = topaz.get_materials_from_staticmesh(staticMesh, True)
    is_translucent_exist = topaz.is_translucent_exist(blendModes)
    if meshNaniteSettings.enabled == False and not is_translucent_exist : 
        meshNaniteSettings.enabled = True # On nanite setting 
        unreal.StaticMeshEditorSubsystem().set_nanite_settings(staticMesh,meshNaniteSettings, apply_changes=True) #apply changes
        print('Nanite is Enabled')
    else :
        print('Nanite is already Enabled or this static mesh contains translucent material.')