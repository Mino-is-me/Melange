from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka
import importlib

importlib.reload(topaz)
importlib.reload(kafka)

selected = topaz.get_selected_assets() 

for asset in selected :
    asset_path = kafka.get_selected_asset_source_path(asset)
    asset_path = kafka.remap_uepath_to_filepath(asset_path)
    kafka.execute_console_command('git add', asset_path)

