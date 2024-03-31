import os
import csv

__all__ = ['get_assets_in_folder','get_selected_level_actor','substring','get_filenames','write_list_to_csv','openFolder']

def substring( _str : str , _from : str , _to : str ):
    _str = r"{}".format(_str)
    new_str = _str.replace(_from,_to,-1)
    print(new_str)
    return new_str

def get_filenames(directory_path):
    # Get a list of file names in the directory
    filenames = os.listdir(directory_path)
    return filenames

def write_list_to_csv( data : list , csv_file_path : str ): 
    '''
    Write a list of data to a CSV file, with each element in the list as a row in the CSV file.
    사용법 :
        write_list_to_csv( ['a','b','c','d','e'], 'C:/Users/username/Desktop' ) ... 
        이렇게 하면 C:/Users/username/Desktop/generated_by_stelle.csv 파일이 생성되고, a,b,c,d,e 가 각각 한 줄씩 들어가게 된다.
    '''
    # Open the CSV file in write mode
    csv_file_path = csv_file_path + '/generated_by_stelle.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)
        for each in data:
            each = [each]
            writer.writerow(each)

    return True

def get_this_abs_directory() -> str : #현재 파일 경로 반환 
    return (os.path.dirname(os.path.realpath(__file__)))


def openFolder( folder_path : str ):
    os.startfile(folder_path)
    return True

print('Stelle initialised.')
