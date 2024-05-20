import unreal 
import os
import shutil

def copy_files(source_folder, destination_folder):
    files = os.listdir(source_folder)

    for file in files:
        source_file = os.path.join(source_folder, file)
        destination_file = os.path.join(destination_folder, file)
        try:
            shutil.copy2(source_file, destination_file)
        except PermissionError:
            print(f"Permission denied for file: {source_file}. Skipping this file.")


projectPath = unreal.Paths.project_dir()
saveGamesPath = projectPath + "/Saved/SaveGames/"
customizePath = projectPath + "/CustomizePresets/"

copy_files(saveGamesPath, customizePath)

print("Files copied successfully!")



