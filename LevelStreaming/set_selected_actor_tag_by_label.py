import unreal 

selected = unreal.EditorLevelLibrary.get_selected_level_actors()

for each in selected :
    tags =  each.get_editor_property('tags')
    if tags == [] :
        label = each.get_actor_label()
        new_tags = [label]
        each.set_editor_property('tags',new_tags)
        #each.set_editor_property('tags', [])