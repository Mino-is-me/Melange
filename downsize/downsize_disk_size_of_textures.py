from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka 
from Lib import __lib_archeron__ as archeron
from Lib import __lib_stelle__ as stelle
import unreal, importlib

importlib.reload(topaz)
importlib.reload(kafka)
importlib.reload(archeron)
importlib.reload(stelle)

# Path: downsize/downsize_disk_size_of_textures.py

assets_paths : list[str] = topaz.get_selected_assets(True)

unreal.AssetToolsHelpers.get_asset_tools().export_assets(assets_paths, 'D:/wip')
 