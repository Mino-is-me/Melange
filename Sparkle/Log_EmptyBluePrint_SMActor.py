

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

        for component in actor_components:
            if isinstance(component, unreal.StaticMeshComponent):
                has_static_mesh_component = True
                
                static_mesh = component.static_mesh
                if static_mesh is None:
                    print("Blueprint Actor:", actor.get_actor_label())
                    print("Empty:", component.get_name())
        print("--------------------------------------------")

        
        
        if not has_static_mesh_component:
            pass

    else:
        pass


