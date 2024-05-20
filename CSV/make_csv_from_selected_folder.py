from Lib import __lib_kafka__ as kafka
from Lib import __lib_stelle__ as stelle
import unreal, importlib 

importlib.reload(kafka)
importlib.reload(stelle)

# Get the selected folder path
abs_path = unreal.Paths.project_content_dir()
selected_folder_path : str = unreal.EditorUtilityLibrary.get_selected_folder_paths()[0]
selected_folder_path = selected_folder_path.replace('All/Game/', '')
abs_path = abs_path + selected_folder_path
abs_path = abs_path.replace('//', '/')

print(abs_path)



files : list[str] = stelle.get_filenames(abs_path)
file_modified_dates : list[str] = []


files_and_files_modified_date : list[list[str]] = [[]]

for i in range(len(files)):
    file_modified_date = stelle.get_file_edit_time(abs_path + '/' + files[i]) + ' ' + files[i]
    files_and_files_modified_date.append([files[i], file_modified_date])

csv : object = stelle.write_list_to_csv(files_and_files_modified_date, abs_path)

print(files_and_files_modified_date)


kafka.dialog_box('CSV 파일이 생성되었습니다.', '파일 경로 : ' + abs_path + '/generated_by_stelle.csv')

stelle.openFolder(abs_path)