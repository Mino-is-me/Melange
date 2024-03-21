import unreal 
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)



actors = topaz.get_selected_level_actors()


for actor in actors :
    components = actor.get_components_by_class(unreal.StaticMeshComponent)
    for component in components :
        asset = component.static_mesh
        topaz.disable_ray_tracing(asset)
        print(str(asset) + ' : ray tracing disabled') 