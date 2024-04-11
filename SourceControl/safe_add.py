from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka
import importlib

importlib.reload(topaz)
importlib.reload(kafka)

selected = topaz.get_selected_assets() 

for asset in selected : 
    git_obj = kafka.get_asset_git_path(asset)
    kafka.execute_console_command('gid add ',git_obj)

kafka.dialog_box('Add Complete', 'Check out mark will be created in 5~10 seconds.')