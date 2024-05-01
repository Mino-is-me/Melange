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

for asset in selectedAssets:
    tex_size_x = asset.blueprint_get_size_x()
    print('tex_size_x: ', tex_size_x)
    if tex_size_x > desired_size :
        tex_path = asset.get_path_name()
        texture_paths.append(tex_path)

print('export assets quantity: ', len(texture_paths))
print('export assets: ', texture_paths)
unreal.AssetToolsHelpers.get_asset_tools().export_assets(texture_paths, 'E:/wip')
print('successfully completed', len(texture_paths))
