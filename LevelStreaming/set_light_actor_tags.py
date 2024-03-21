import unreal 

level_actors = unreal.EditorLevelLibrary.get_all_level_actors()

actors = level_actors
for actor in actors :
    label = actor.get_actor_label()
    tags =  actor.get_editor_property('tags')
    if label == 'Ultra_Dynamic_Weather' :
        
        tags = [] 
        