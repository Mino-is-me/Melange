

import unreal
import importlib
import subprocess
from Lib import __lib_topaz__ as topaz 

importlib.reload(topaz)

def __init__() -> None:
    '''
    # Description: Source Control Support 
    ## Don't use [UnrealPath], use [ExplorerPath] instead
    ### Example: /Game/[Asset] -> D:/CINEVStudio/CINEVStudio/Content/[Asset]
    '''
    print('Kafka Initialized')
    pass

def get_git_path() -> str:
    '''
    ## Description: Get the path of the git
    '''
    git_path = unreal.Paths.project_content_dir()
    git_path = git_path.rsplit('/', 3)[0] + '/'
    print('Git Path = ' + git_path)
    return git_path

def remap_uepath_to_filepath(uepath: str) -> str: #언리얼 패스 -> 파일 패스로 변환
    '''
    ## Description: Remap the Unreal Engine path to the file path
    '''
    projectPath = unreal.Paths.project_dir()
    #print(projectPath)
    filepath = uepath.replace('/Game/', projectPath + 'Content/')
    name = filepath.rsplit('.', 1)[0]
    name = name + '.uasset'
    print(name)
    return name

    
def get_selected_asset_source_path(asset:object) -> str:
    '''
    ## Description: Get the source path of the selected asset
    '''
    source_path = unreal.EditorAssetLibrary.get_path_name(asset)
    print(source_path)
    return source_path
     
def lock_asset(asset:str) -> None:
    '''
    ## Description: Lock the asset
    '''
    dir = get_git_path()
    asset = asset.replace(dir, '')
    command = 'git lfs lock ' + asset
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(output)

def unlock_asset(asset:str) -> None:
    dir = get_git_path()
    asset = asset.replace(dir, '')
    print(asset)
    command = 'git lfs unlock ' + asset
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(output)
 

