
import shutil, os, stat, subprocess

def remove_readonly(func, path, _):
    """Change the mode of path to writeable and retry the operation."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def get_engine_root (ue_ver : str ) -> str :
    '''
    ## Description: Get the engine root path
    '''
    program_files_dir = os.environ['PROGRAMFILES']
    #print(program_files_dir)
    engine_root = program_files_dir + '/Epic Games/UE_' + ue_ver + '/Engine/'
    
    return engine_root

def openFolder(folder_path: str):
    os.startfile(folder_path)
    return True

def execute_console_command(command:str, target:str ='', dir:str ='.') -> bool:
    '''
    #### Description: Execute the console command
    #### command : desired command
    #### target : target object, normally editor asset.
    #### dir : directory where the command should be executed.
    '''
    execute_command = command + ' ' + target
    print('Command : ' + execute_command)
    process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(command)
## function End 


def remove_readonly(func, path, _):
    "Clear the readonly bit and reattempt the removal"
    os.chmod(path, stat.S_IWRITE)
    func(path)

def remove_dir_force(dir_path: str):
    '''
    #### Description: Forcefully remove a directory and its contents
    #### dir_path : path to the directory to remove
    '''
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path, onerror=remove_readonly)

# Usage : remove_dir_force('C:/Users/username/Desktop/test')


engine_version : str = '5.3'
repo_url : str = 'https://gitlab.cinamon.me/cinev/customshader.git'

engine_root = get_engine_root(engine_version)
shader_root = engine_root + 'Shaders'

remove_dir_force(shader_root)

openFolder(engine_root)

clone_command = 'git clone ' + repo_url + ' ' + 'Shaders'

execute_console_command(clone_command, '', engine_root)






