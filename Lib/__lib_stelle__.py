import os
import csv
import subprocess

__all__ = [
    "substring",
    "get_filenames",
    "write_list_to_csv",
    "openFolder",
    "resize_image_file"
]


def substring(_str: str, _from: str, _to: str) -> str:
    _str = r"{}".format(_str)
    new_str = _str.replace(_from, _to, -1)
    print(new_str)
    return new_str


def get_filenames(directory_path) -> list[str]:
    # Get a list of file names in the directory
    filenames = os.listdir(directory_path)
    return filenames


def write_list_to_csv(data: list, csv_file_path: str) -> csv:
    """
    Write a list of data to a CSV file, with each element in the list as a row in the CSV file.
    사용법 :
        write_list_to_csv( ['a','b','c','d','e'], 'C:/Users/username/Desktop' ) ...
        이렇게 하면 C:/Users/username/Desktop/generated_by_stelle.csv 파일이 생성되고, a,b,c,d,e 가 각각 한 줄씩 들어가게 된다.
    """
    # Open the CSV file in write mode
    csv_file_path = csv_file_path + "/generated_by_stelle.csv"
    with open(csv_file_path, "w", newline="") as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)
        for each in data:
            each = [each]
            writer.writerow(each)

    return True


def get_this_abs_directory() -> str:  # 현재 파일 경로 반환
    return os.path.dirname(os.path.realpath(__file__))


def openFolder(folder_path: str):
    os.startfile(folder_path)
    return True

def resize_image_file(image_path: str, new_width: int, new_height: int):
    from PIL import Image
    img = Image.open(image_path)
    img = img.resize((new_width, new_height))
    img.save(image_path)
    return True

def execute_console_command(command:str, target:str ='') -> bool:
    '''
    #### Description: Execute the console command
    #### command : desired command
    #### target : target object, normaly editor asset.
    '''
    execute_command = command + ' ' + target
    print('Command : ' + execute_command)
    process = subprocess.Popen(execute_command, stdout=subprocess.PIPE, shell=True, cwd=dir)
    output, error = process.communicate()
    print(command)
    
def get_engine_root (ue_ver : str ) -> str :
    '''
    ## Description: Get the engine root path
    '''
    program_files_dir = os.environ['PROGRAMFILES']
    print(program_files_dir)
    engine_root = program_files_dir + '/Epic Games/UE_' + ue_ver + '/Engine/'
    
    return engine_root

print("Stelle initialised.")
