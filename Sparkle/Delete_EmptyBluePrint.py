

import unreal
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)


all_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

for actor in all_actors:

    actor_class = actor.get_class()
    if isinstance(actor_class, unreal.BlueprintGeneratedClass):
        
        actor_components = actor.get_components_by_class(unreal.ActorComponent)
        has_static_mesh_component = False
        all_empty = True #초기 True설정 

        for component in actor_components:
            if isinstance(component, unreal.StaticMeshComponent):
                has_static_mesh_component = True
                
                static_mesh = component.static_mesh #SM없으면 패스
                if static_mesh is None:
                    pass

                elif static_mesh != None : #SM있으면 all_empty = False로
                    all_empty = False


        if not has_static_mesh_component:
            all_empty = False

        if all_empty == True : 
            print("Blueprint Actor:", actor.get_actor_label(), "<<<")
            unreal.EditorLevelLibrary.destroy_actor(actor)

    else:
        pass


