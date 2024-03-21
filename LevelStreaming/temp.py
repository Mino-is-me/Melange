import unreal 

level_actors = unreal.EditorLevelLibrary.get_all_level_actors()

actors = level_actors
for actor in actors :
    tags =  actor.get_editor_property('tags')
    label = actor.get_actor_label()

    if label == 'Ultra_Dynamic_Weather' or label == 'Ultra_Dynamic_Weather2' :
        print(tags)
        if actor.actor_has_tag('Env_Light') :
            actor.tags = []
            print('Tag Deleted')




for actor in actors :
    label = actor.get_actor_label()
    tags =  actor.get_editor_property('tags')
    if label == 'Ultra_Dynamic_Weather' or label == 'Ultra_Dynamic_Weather2' :
       print(tags)