from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka
import importlib, unreal 

importlib.reload(topaz)


selected_assets : unreal.Object = topaz.get_selected_assets()
asset_names_not_root_motion : str = ''
asset_names_root_motion : str = ''

for asset in selected_assets :
    if asset.__class__ == unreal.AnimSequence :
        root_motion_enabled : bool = asset.get_editor_property('enable_root_motion')
        
        
        if not root_motion_enabled :
            asset.set_editor_property('enable_root_motion', True)
            asset_names_not_root_motion = asset_names_not_root_motion + asset.get_name() + '\n' 

        else :
            print(f'Root Motion Already Enabled for {asset.get_name()}')
            asset_names_root_motion = asset_names_root_motion + asset.get_name() + '\n'
            
            
kafka.dialog_box('Root Motion Validator', asset_names_root_motion + 'are OK'  + '\n' + asset_names_not_root_motion + 'are Root Motion Enabled')   