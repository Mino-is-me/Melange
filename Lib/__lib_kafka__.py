

import unreal
import importlib
from Lib import __lib_topaz__ as topaz 
import Sparkle as sparkle 

importlib.reload(topaz)

def __self__() -> None:
    '''
    # Description: Source Control Support 
    ## Don't use [UnrealPath], use [ExplorerPath] instead
    ### Example: /Game/[Asset] -> D:/CINEVStudio/CINEVStudio/Content/[Asset]
    '''
    pass

def remap_uepath_to_filepath(uepath: str) -> str: #언리얼 패스 -> 파일 패스로 변환
    '''
    ## Description: Remap the Unreal Engine path to the file path
    '''
    projectPath = unreal.Paths.project_dir()
    print(projectPath)
    filepath = uepath.replace('/Game/', projectPath)
    name = filepath.rsplit('.', 1)[0]
    return name

def get_selected_asset_source_path() -> str:
    '''
    ## Description: Get the source path of the selected asset
    '''
    selected_assets = topaz.get_selected_assets()
    if len(selected_assets) > 0:
        asset = selected_assets[0]
        source_path = unreal.EditorAssetLibrary.get_path_name(asset)
        return source_path
    else:
        return None

path = get_selected_asset_source_path()

newpath = remap_uepath_to_filepath(path)

print(path,newpath)

#revert_if_unchanged(newpath)

qq = unreal.SourceControl.revert_unchanged_file(newpath, True)

print(qq)