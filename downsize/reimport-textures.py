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
        
        #이미지 저장된 드라이브 경로
        target_drive = 'E:/wip/Game/'
        source_drive = 'E:/CINEVStudio/CINEVStudio/Content/'

        new_tex_path = remap_uepath_to_filepath(tex_path).replace(source_drive, target_drive)
  
        
        has_source = len(source_file) != 0
        hasPNG = source_file.lower().find('.png')
        hasTGA = source_file.lower().find('.tga')
        hasJPEG = source_file.lower().find('.jpeg') or source_file.lower().find('.jpg')
        file_path: str = ''
        if has_source:
            if hasPNG != -1:
                print('This is PNG')
                file_path = selected_asset_path.replace(source_drive, target_drive).replace('.uasset','.PNG')
            elif hasTGA != -1:
                print('This is TGA')
                file_path = selected_asset_path.replace(source_drive, target_drive).replace('.uasset','.PNG')
            elif hasJPEG != -1:
                print('This is JPEG')                
                file_path = selected_asset_path.replace(source_drive, target_drive).replace('.uasset','.JPEG')
        else:
            hasAlpha = False
            print('This is PNG')
            if hasAlpha:
                file_path = selected_asset_path.replace(source_drive, target_drive).replace('.uasset','.exr')
            else:
                file_path = selected_asset_path.replace(source_drive, target_drive).replace('.uasset','.PNG')
        
        reimport_texture(tex_path, file_path)
    else:
        print('This texture is not over 2048px')