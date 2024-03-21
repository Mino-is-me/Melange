import unreal


def get_project_dir () -> str :
    path : str = unreal.Paths.game_source_dir()
    path = path.replace ('CINEVStudio/Source/', 'CINEVStudio/Content/Python/')
    return path 


root_path : str = get_project_dir()
print(root_path)