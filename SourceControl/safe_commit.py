from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka
import importlib

importlib.reload(topaz)
importlib.reload(kafka)

selected = topaz.get_selected_assets() 

for asset in selected : # add and commit 
    asset_path = kafka.get_selected_asset_source_path(asset)
    asset_path = kafka.remap_uepath_to_filepath(asset_path)
    kafka.commit_asset(asset_path, message)

kafka.execute_console_command('git push') # push to remote repository

for asset in selected : # unlock assets
    asset_path = kafka.get_selected_asset_source_path(asset)
    asset_path = kafka.remap_uepath_to_filepath(asset_path)
    kafka.unlock_asset(asset_path)
    pass
