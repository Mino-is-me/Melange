import unreal


current_world : object = unreal.EditorLevelLibrary.get_editor_world() #get current world 
day_light_level_path : str = "/Game/Lighting/Turntable/Character_Day" #prepared light level 
unreal.EditorLevelUtils.add_level_to_world(current_world,day_light_level_path,unreal.LevelStreamingAlwaysLoaded)

