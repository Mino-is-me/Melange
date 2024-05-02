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
    print(name)
    return name

def reimport_texture ( tex_ue_file_path: str, file_path : str) :
    # textureFactory = unreal.Texture2DFactoryNew()
    textureFactory = unreal.ReimportTextureFactory()

    importTask = unreal.AssetImportTask()
    importTask.automated = True
    importTask.filename = file_path

    length = len(tex_ue_file_path.split('/'))
    
    destination_name = tex_ue_file_path.split('/')[length-1].split('.')[0]
    destination_path = tex_ue_file_path.rsplit('/', 1)[0] + '/'

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
#이미지 저장된 드라이브 경로
texture_folder = 'E:/wip/Game/'
source_drive = 'E:/CINEVStudio/CINEVStudio/Content/'

desired_size = 2048

for asset in selectedAssets:
    tex_asset: unreal.Texture2D = asset
    tex_width = tex_asset.blueprint_get_size_x()
    if tex_width > desired_size :
        tex_path = tex_asset.get_path_name()
        tex_ue_file_path = remap_uepath_to_filepath(tex_path)

        import_info: unreal.AssetImportData = tex_asset.get_editor_property('asset_import_data')
        are_sources = len(import_info.extract_filenames()) > 0
        source_file = import_info.get_first_filename()
        has_source = len(source_file) != 0
        
        new_tex_path = remap_uepath_to_filepath(tex_path).replace(source_drive, texture_folder)
        
        hasPNG = source_file.lower().find('.png')
        hasTGA = source_file.lower().find('.tga')
        hasJPEG = source_file.lower().find('.jpeg')
        hasJPG = source_file.lower().find('.jpg')
        file_path: str = ''
        
        if has_source:
            if hasPNG != -1:
                print('This is PNG')
                file_path = tex_ue_file_path.replace(source_drive, texture_folder).replace('.uasset','.PNG')
            elif hasTGA != -1:
                print('This is TGA')
                file_path = tex_ue_file_path.replace(source_drive, texture_folder).replace('.uasset','.TGA')
            elif hasJPEG != -1:
                print('This is JPEG')                
                file_path = tex_ue_file_path.replace(source_drive, texture_folder).replace('.uasset','.PNG')
            elif hasJPG != -1:
                print('This is JPG')                
                file_path = tex_ue_file_path.replace(source_drive, texture_folder).replace('.uasset','.PNG')
        else:
            hasAlpha = False
            print('This is PNG')

            if hasAlpha:
                file_path = tex_ue_file_path.replace(source_drive, texture_folder).replace('.uasset','.exr')
            else:
                print('hihi')
                file_path = tex_ue_file_path.replace(source_drive, texture_folder).replace('.uasset','.PNG')
        reimport_texture(tex_path, file_path)
        unreal.EditorAssetLibrary.save_asset(tex_asset.get_path_name())
        
    else:
        print('This texture is not over 2048px')