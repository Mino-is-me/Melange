from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka
import importlib

importlib.reload(topaz)
importlib.reload(kafka)


message :str = message.replace(' ', '_') # replace space with '_'

selected:list[object] = topaz.get_selected_assets() 
git_paths :list[str] = []

for asset in selected : # add and commit 
    asset_path = kafka.get_asset_git_path(asset)
    git_paths.append(asset_path)

kafka.stage_assets(git_paths, 'safe commit & unlock test by Melange') # stage
command = 'git commit --m ' + '\'' + message + '\''
kafka.execute_console_command(command) # commit

kafka.execute_console_command('git push') # push

for git_obj in git_paths : # unlock after push 
    kafka.unlock_asset(git_obj)
    
kafka.dialog_box('Safe Commit Complete', 'Check out mark will disappear in 5~10 seconds.')

