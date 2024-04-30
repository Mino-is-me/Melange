from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka 
from Lib import __lib_archeron__ as archeron
from Lib import __lib_stelle__ as stelle
import unreal, importlib

importlib.reload(topaz)
importlib.reload(kafka)
importlib.reload(archeron)
importlib.reload(stelle)

# Path: downsize/downsize_disk_size_of_textures.py

list_tex :list[unreal.Texture2D] = archeron.get_all_textures_in_folder('/Game/CitySample/Textures')


for tex in list_tex:
    tex_size_x = tex.blueprint_get_size_x()
    if tex_size_x > 1024 :
        tex_path = tex.get_path_name()
        new_tex_path = kafka.remap_uepath_to_filepath(tex_path)
        png_tex_path = new_tex_path.replace('.uasset','.png')
        topaz.export_texture_to_png(tex,png_tex_path)
        