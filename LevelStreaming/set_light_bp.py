import unreal 

level_actors = unreal.EditorLevelLibrary.get_selected_level_actors()

light_function = unreal.EditorAssetLibrary.load_asset('/Game/TA/Users/Narr/M_Light_Global')

for i in level_actors :
    i.set_light_function_material(light_function)
    unreal.log('Light Function Assigned ')