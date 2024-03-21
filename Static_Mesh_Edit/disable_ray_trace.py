import unreal 
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)


assets = topaz.get_selected_assets()

for selected in assets :
    if selected.__class__ == unreal.Blueprint:
        print('Blueprint')
        comps = topaz.get_component_by_class(selected, unreal.StaticMeshComponent)
        for i in comps :
            asset = i.static_mesh
            topaz.disable_ray_tracing(asset)
            #print(str(asset) + ' : ray tracing disabled')
    elif selected.__class__ == unreal.StaticMesh:
        print('static mesh')
        topaz.disable_ray_tracing(selected)
    else :
        print('do nothing')


 