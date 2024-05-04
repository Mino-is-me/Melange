from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka 
from Lib import __lib_archeron__ as archeron
from Lib import __lib_stelle__ as stelle
import unreal, importlib
import time
import ctypes

importlib.reload(topaz)
importlib.reload(kafka)
importlib.reload(archeron)
importlib.reload(stelle)

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
desired_size = 2048
texture_paths = []
target_drive = 'E:/wip/'

for asset in selectedAssets:
    asset.set_editor_property('max_texture_size', 0)
    tex_size_x = asset.blueprint_get_size_x()
    if tex_size_x > desired_size :
        print('process asset: ', asset.get_name())
        tex_path = asset.get_path_name()
        texture_paths.append(tex_path)

print('export assets quantity: ', len(texture_paths))
print('export assets: ', texture_paths)
unreal.AssetToolsHelpers.get_asset_tools().export_assets(texture_paths, target_drive)
print('successfully completed', len(texture_paths))
