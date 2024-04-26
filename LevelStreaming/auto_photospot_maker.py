import unreal,importlib
from Lib import __lib_archeron__ as archeron

importlib.reload(archeron)

actors : list[unreal.Actor] = archeron.get_all_leveL_actors()

if len(actors) > 0 :
    for actor in actors :
        print(actor.get_actor_label())
        actor_label = actor.get_actor_label()
        
        actor_tags = actor.get_editor_property('tags')
        
        if len(actor_tags) == 0 :
            actor_tags = [actor_label]
            actor.set_editor_property('tags',actor_tags)
        
        
        
        
        