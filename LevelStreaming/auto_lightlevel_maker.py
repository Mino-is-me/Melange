import unreal 
from Lib import __lib_archeron__ as archeron

actors : list[unreal.Actor] = archeron.get_all_leveL_actors()

if len(actors) > 0 :
    for actor in actors :
        #print(actor.get_actor_label())
        actor_label = actor.get_actor_label()
        
        actor_tags = actor.get_editor_property('tags')
        
        if actor_label == 'Ultra_Dynamic_Weather' or actor_label == 'Ultra_Dynamic_Weather2' or actor_label == 'Ultra_Dynamic_Sky' or 'Ultra_Dynamic_Sky2':
            pass
        else :
            if len(actor_tags) == 0 :
                actor_tags = ['ENV_Light']
                actor.set_editor_property('tags',actor_tags)
            
            
        
        
        