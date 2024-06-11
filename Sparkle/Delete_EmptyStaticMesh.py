import unreal
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)

selected_Level_Actors = topaz.get_selected_level_actors()


for each in selected_Level_Actors :

    if each.__class__ == unreal.StaticMeshActor :
        static_mesh_component = each.static_mesh_component
        get_static_mesh = static_mesh_component.static_mesh

        if get_static_mesh == None :
            print(each.get_actor_label(),"Static Mesh is Empty")
            unreal.EditorLevelLibrary.destroy_actor(each)

        else :
            pass     

    else :
        pass







