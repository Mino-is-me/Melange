import unreal 
from Lib import __lib_topaz__ as topaz
import os
import csv

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
    # Open the CSV file in write mode
    csv_file_path = csv_file_path + '/generated_by_stelle.csv'
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Create a CSV writer
        writer = csv.writer(csvfile)

        # Write the list to the CSV file
        # If data is a list of lists (multiple rows), use writerows
        writer.writerows(data)

    return True

def export_staticmesh_to_fbx( static_mesh : unreal.StaticMesh, fbx_file_path : str): #staticMeshExporter 
    exportTask = unreal.AssetExportTask()
    exportTask.automated = True
    exportTask.filename = fbx_file_path
    exportTask.object = static_mesh
    exportTask.options = unreal.FbxExportOption()
    exportTask.prompt = False

    fbxExporter = unreal.StaticMeshExporterFBX()
    exportTask.exporter = fbxExporter
    fbxExporter.run_asset_export_task(exportTask)

    return True

def openFolder( folder_path : str ):
    os.startfile(folder_path)
    return True

def list_logger(list : list) -> None : #리스트 로거
    for each in list :
        print(each)

unreal.log('Stelle initialised.')
