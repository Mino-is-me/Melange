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
    
    return True

def executeImportTask(task):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([task])

    return True

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
for asset in selectedAssets:
    
    tex_size_x = asset.blueprint_get_size_x()
    if tex_size_x > 2048 :
        tex_path = asset.get_path_name()
        selected_asset_path = remap_uepath_to_filepath(tex_path)
        import_info = asset.get_editor_property('asset_import_data')
        source_file = import_info.get_first_filename()
        
        #이미지 저장할 드라이브 경로
        target_drive = 'D:/'
        source_drive = unreal.Paths.project_dir().split('/')[0] + '/'

        new_tex_path = remap_uepath_to_filepath(tex_path).replace(source_drive, target_drive)
  
        file_path: str
        hasPNG = source_file.lower().find('.png')
        hasTGA = source_file.lower().find('.tga')

        if hasPNG != -1:
            print('This is PNG')
            file_path = selected_asset_path.replace('E:/', 'D:/').replace('.uasset','.png')
            exporter = unreal.TextureExporterPNG()
        elif hasTGA != -1:
            print('This is TGA')
            exporter = unreal.TextureExporterTGA()
            file_path = selected_asset_path.replace('E:/', 'D:/').replace('.uasset','.png')
        else:
            # to-do > rgba채널 사용하는 텍스처면 tga로 아니면 png로 익스포트하게하기
            print('This is PNG')
            exporter = unreal.TextureExporterPNG()
            file_path = selected_asset_path.replace('E:/', 'D:/').replace('.uasset','.png')
        reimport_texture(tex_path, file_path)
    else:
        print('This texture is not over 1024px')