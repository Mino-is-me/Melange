import unreal

def remap_uepath_to_filepath(uepath: str) -> str: #언리얼 패스 -> 파일 패스로 변환
    '''
    ## Description: Remap the Unreal Engine path to the file path
    '''
    projectPath = unreal.Paths.project_dir()
    #print(projectPath)
    filepath = uepath.replace('/Game/', projectPath + 'Content/')
    name = filepath.rsplit('.', 1)[0]
    name = name + '.uasset'
    return name

def reimport_texture ( selected_asset_path: str, file_path : str) :
    # textureFactory = unreal.Texture2DFactoryNew()
    textureFactory = unreal.ReimportTextureFactory()

    importTask = unreal.AssetImportTask()
    importTask.automated = True
    importTask.filename = file_path

    length = len(selected_asset_path.split('/'))
    
    destination_name = selected_asset_path.split('/')[length-1].split('.')[0]
    destination_path = selected_asset_path.rsplit('/', 1)[0] + '/'

    importTask.destination_name = destination_name
    importTask.destination_path = destination_path

    print('destination_name ', destination_name)
    print('destination_path ', destination_path)

    importTask.replace_existing = True
    importTask.save = True
    importTask.factory = textureFactory
    
    executeImportTask(importTask)
    # textureFactory.set_editor_property('asset_import_task', importTask)
    print('HO!')
    
    return True

def executeImportTask(task):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
for asset in selectedAssets:
    
    tex_size_x = asset.blueprint_get_size_x()
    if tex_size_x > 1024 :
        tex_path = asset.get_path_name()
        selected_asset_path = remap_uepath_to_filepath(tex_path)
        file_path = selected_asset_path.replace('E:/', 'D:/').replace('.uasset','.png')

        print("텍스처 에셋 절대 경로 ", selected_asset_path)
        print("텍스처 에셋 경로 ", tex_path)
        print("파일 경로 ",  file_path)

        reimport_texture(tex_path, file_path)
    else:
        print('This texture is not over 1024px')