

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
    #print('Git Path = ' + git_path)
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

def get_git_username():
    '''
    ## Description: Get the Git username
    '''
    command = ['git', 'config', '--global', 'user.name']
    git_username = subprocess.check_output(command).decode().strip()
    print('Git Username = ' + git_username)
    return git_username
    
def get_selected_asset_source_path(asset:object) -> str:
    '''
    ## Description: Get the source path of the selected asset
    '''
    source_path = unreal.EditorAssetLibrary.get_path_name(asset)
    print(source_path)
    return source_path

def get_asset_git_path(asset:object) -> str:
    '''
    ## Description: Get the git path of the asset
    '''
    if asset.__class__ == unreal.World :
        source_path = get_selected_asset_source_path(asset)
        projectPath = unreal.Paths.project_dir()
        #print(projectPath)
        filepath = source_path.replace('/Game/', projectPath + 'Content/')
        name = filepath.rsplit('.', 1)[0]
        name = name + '.umap'
        print(name)
        return name
    else :
        name = get_selected_asset_source_path(asset)
        name = remap_uepath_to_filepath(name)
        print(name)
        return name 
    
    
def execute_console_command(command:str, target:str ='') -> bool:
    '''
    #### Description: Execute the console command
    #### command : desired command
    #### target : target object, normaly editor asset.
    '''
    dir = get_git_path() 
    target = target.replace(dir, '')
    execute_command = command + ' ' + target
    print('Command : ' + execute_command)
    process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(command)

def dialog_box(title:str, message:str) -> None:
    '''
    ## Description: Show the dialog box
    '''
    unreal.EditorDialog.show_message(title, message, unreal.AppMsgType.OK)
    
     
def lock_asset(asset:str) -> None:
    '''
    ## Description: Lock the asset
    '''
    dir = get_git_path()
    asset = asset.replace(dir, '')
    command = 'git lfs lock ' + asset
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(command)

def unlock_asset(asset:str) -> None:
    dir = get_git_path()
    asset = asset.replace(dir, '')
    print(asset)
    command = 'git lfs unlock ' + asset
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(command)
    
def stage_assets(assets:list[str], commit_message:str) -> None:
    '''
    ## Description: Commit the asset
    '''
    dir = get_git_path()
    for asset in assets :  
        asset = asset.replace(dir, '')
        command = 'git add ' + asset
        process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
        output, error = process.communicate()
        print(command)
    
def unlock_user_assets(user:str) -> None:
    '''
    ## Description: Unlock all assets locked by a specific user
    '''
    dir = get_git_path()

    # Get a list of all locked files
    command = 'git lfs locks'
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    locked_files = output.decode().split('\n')
    
    print(locked_files)

    # Unlock each file locked by the specified user
    for file in locked_files:
        if file and user in file:
            file = file.split(' ')[0]  # Get the file path
            command = 'git lfs unlock ' + file
            process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, cwd=dir)
            output, error = process.communicate()
            print(command)
