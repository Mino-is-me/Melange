from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka 
from Lib import __lib_archeron__ as archeron
from Lib import __lib_stelle__ as stelle

import unreal, importlib
import ctypes

from downsize import step0_settings as settings

importlib.reload(topaz)
importlib.reload(kafka)
importlib.reload(archeron)
importlib.reload(stelle)
importlib.reload(settings)

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
texture_paths = []
desired_size = settings.desired_size
wip_folder = settings.wip_folder

for asset in selectedAssets:
    tex_size_x = asset.blueprint_get_size_x()
    if tex_size_x > desired_size :
        tex_path = asset.get_path_name()
        texture_paths.append(tex_path)

unreal.AssetToolsHelpers.get_asset_tools().export_assets(texture_paths, wip_folder)
print('successfully completed', len(texture_paths))

# ...

ctypes.windll.user32.MessageBoxW(0, "Script completed successfully!", "Notification", 0)