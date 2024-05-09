from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka 
from Lib import __lib_archeron__ as archeron
from Lib import __lib_stelle__ as stelle
import unreal, importlib

importlib.reload(topaz)
importlib.reload(kafka)
importlib.reload(archeron)
importlib.reload(stelle)

# Path: downsize/downsize_disk_size_of_textures.py

list_tex :list[unreal.Texture2D] = archeron.get_all_textures_in_folder('/Game/CitySample/Textures')

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

def export_texture ( texture_asset : unreal.Texture2D, target_file_path : str, exporter) : #textureExporter
    exportTask = unreal.AssetExportTask()
    
    exportTask.automated = True
    
    exportTask.filename = target_file_path
    exportTask.object = texture_asset
    exportTask.options = exporter
    exportTask.prompt = False
    tgaExporter = exporter
    exportTask.exporter = tgaExporter
    tgaExporter.run_asset_export_task(exportTask)
    return True

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
ImagePathList = []

#선택된 이미지 익스포트
for asset in selectedAssets:
    tex_size_x = asset.blueprint_get_size_x()
    if tex_size_x > 1024 :
        tex_path = asset.get_path_name()
        import_info = asset.get_editor_property('asset_import_data')
        source_file = import_info.get_first_filename()
        
        hasPNG = source_file.lower().find('.png')
        hasTGA = source_file.lower().find('.tga')
        new_tex_path = remap_uepath_to_filepath(tex_path)

        if hasPNG != -1:
            png_tex_path = new_tex_path.replace('.uasset','.png')
            print('This is PNG')
            export_texture(asset, png_tex_path, unreal.TextureExporterPNG())
            print(png_tex_path)
            ImagePathList.append(png_tex_path)
        elif hasTGA != -1:
            print('This is TGA')
            tga_tex_path = new_tex_path.replace('.uasset','.tga')
            export_texture(asset, tga_tex_path, unreal.TextureExporterTGA())
            print(tga_tex_path)
            ImagePathList.append(tga_tex_path)
        else:
            print('This is not PNG or TGA Export to PNG') 
            png_tex_path = new_tex_path.replace('.uasset','.png')
            export_texture(asset, png_tex_path, unreal.TextureExporterPNG())
            ImagePathList.append(png_tex_path)
        
        # export_texture_to_png(asset,png_tex_path)

#이미지 사이즈 조정
for imagePath in ImagePathList:
    stelle.resize_image_file(imagePath, 1024, 1024, True)