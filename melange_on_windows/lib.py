import os
import csv
import subprocess
from datetime import datetime

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

def get_file_edit_time(file_path: str) -> str:
    """
    Get the last edit time of the file.
    사용법 :
        get_file_edit_time('C:/Users/username/Desktop/test.txt') ...
        이렇게 하면 test.txt 파일의 마지막 수정 시간을 반환한다.
    """
    edit_time = os.path.getmtime(file_path)
    edit_time = datetime.fromtimestamp(edit_time).strftime('%Y-%m-%d %H:%M:%S')
    return edit_time

def write_list_to_csv(data: list, csv_file_path: str) -> bool:
    """
    Write a list of data to a CSV file, with each element in the list as a row in the CSV file.
    If the list is 2-dimensional, each inner list is written as a row.
    """
    # Open the CSV file in write mode
    csv_file_path = csv_file_path + "/generated_by_stelle.csv"
    with open(csv_file_path, "w", newline="") as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)
        for row in data:
            # If the data is a 2-dimensional list, each inner list is written as a row
            if isinstance(row, list):
                writer.writerow(row)
            # If the data is a 1-dimensional list, each element is written as a row
            else:
                writer.writerow([row])

    return True

def read_csv_to_list(csv_path : str) -> list[str] : #csv파일에서 에셋 리스트로 리턴 
    with open(csv_path, 'r') as f:
        lines = f.readlines()
    return lines

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
    #print(program_files_dir)
    engine_root = program_files_dir + '/Epic Games/UE_' + ue_ver + '/Engine/'
    
    return engine_root

print("Stelle initialised.")
