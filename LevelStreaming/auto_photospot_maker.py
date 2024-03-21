import unreal 

levels = unreal.EditorUtilityLibrary.get_selected_assets()


for each in levels :
    each_name = each.get_path_name()
    print(each_name)
    unreal.EditorLevelLibrary.load_level(each_name)
    actors = unreal.EditorLevelLibrary.get_all_level_actors()

    for actor in actors :
        tags =  actor.get_editor_property('tags')
        if tags == [] :
            label = actor.get_actor_label()
            new_tags = [label]
            actor.set_editor_property('tags',new_tags)

