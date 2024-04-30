import unreal,importlib
from Lib import __lib_archeron__ as archeron

importlib.reload(archeron)

actors : list[unreal.Actor] = archeron.get_all_leveL_actors()

if len(actors) > 0 :
    for actor in actors :
        actor_tags = actor.get_editor_property('tags')
        actor_label = actor.get_actor_label()
        if len(actor_tags) == 0 or actor_tags[0] != 'ENV_Light' :     
                
            actor_tags = ['ENV_Light']
            if 'Ultra_Dynamic_Sky' in actor_label or 'Ultra_Dynamic_Weather' in actor_label:
                actor_tags = []
                actor.set_editor_property('tags', actor_tags)
            else : 
                actor.set_editor_property('tags', actor_tags)
            
            
        