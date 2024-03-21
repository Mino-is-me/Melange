import unreal 
import os



save_data_dir = ( unreal.Paths.project_saved_dir() ) + 'SaveGames/'

print(save_data_dir)

path = os.path.realpath(save_data_dir)
os.startfile(path)