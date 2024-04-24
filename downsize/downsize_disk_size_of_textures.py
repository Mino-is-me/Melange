from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka 
from Lib import __lib_archeron__ as archeron
import unreal, importlib

importlib.reload(topaz)
importlib.reload(kafka)
importlib.reload(archeron)

# Path: downsize/downsize_disk_size_of_textures.py

list_tex :list[unreal.Texture2D] = archeron.get_all_textures_in_folder('/Game/CitySample')

print(list_tex)