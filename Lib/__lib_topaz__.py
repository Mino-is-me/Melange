import unreal


__all__ = ['get_component_handles','get_component_objects','get_component_by_class',
           'get_component_by_var_name','get_selected_assets','get_selected_asset','get_selected_level_actors','get_selected_level_actor','cutoff_nanite_tri',
           'set_actor_tag_by_class','get_materials_from_staticmesh','is_translucent_exist','get_assets_in_folder','get_asset_filepath','get_cooked_dir','disable_ray_tracing',
           'get_asset_from_static_mesh_actor','get_textures_list_from_materials','get_all_texture_assets_from_material_instance','get_actor_bound_size','set_texture_size_by_bound',
           'log']

def __test__():
    unreal.log('Topaz Test')

def get_component_handles(blueprint_asset_path) -> unreal.Subsystem : ## 사용안해도됨, 다음 함수에서 호출해서 사용하는 함수, 핸들러 직접 물고싶으면 쓰셈 
    subsystem               : unreal.Subsystem      = unreal.get_engine_subsystem(unreal.SubobjectDataSubsystem)
    blueprint_asset         : unreal.Blueprint      = unreal.load_asset(blueprint_asset_path)
    subobject_data_handles  : unreal.Subsystem      = subsystem.k2_gather_subobject_data_for_blueprint(blueprint_asset)

    return subobject_data_handles

def get_component_objects(blueprint_asset_path : str) -> list[unreal.Object] : ## 컴포넌트 무식하게 다 긁어줌 
    objects : list[unreal.SubobjectDataSubsystem]                          = [] # init 
    handles : unreal.SubobjectDataHandle                                   = get_component_handles(blueprint_asset_path)
    for handle in handles:
        data = unreal.SubobjectDataBlueprintFunctionLibrary.get_data(handle)
        object = unreal.SubobjectDataBlueprintFunctionLibrary.get_object(data) 
        objects.append(object)

    return objects

def get_component_by_class(blueprint_to_find_components : unreal.Blueprint, component_class_to_find : unreal.Class) -> list[unreal.Object] : ## 컴포넌트중에 클래스 맞는것만 리턴해줌 
    '''
    Use Case :
        topaz.get_component_by_class([블루프린트(어셋)], [찾을 컴포넌트 클래스])
    주의점 :
        unreal.StaticMesh 등과 같은 어셋 오브젝트가 아니라
        unreal.StaticMeshComponent 등과 같은 컴포넌트 오브젝트를 넣어야 합니다.
    '''
    components = []
    asset_path          : list[str]             = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects   : list[unreal.Class]    = get_component_objects(asset_path)

    for each in component_objects:
        compare_class : bool = (each.__class__ == component_class_to_find)
        if compare_class :
            components.append(each)

    return components

def get_component_by_var_name(blueprint_to_find_components : unreal.Blueprint, component_name_to_find : str) : ##컴포넌트 이름으로 찾음 
    components = []
    asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(blueprint_to_find_components)
    component_objects = get_component_objects(asset_path)

    for each in component_objects:
        compare_name = (each.get_name()) == ( component_name_to_find + '_GEN_VARIABLE' )
        if compare_name :
            components.append(each)

    return components

def get_selected_assets(get_path : bool = False) -> list[unreal.Object]: #리스트로 선택된 오브젝트 리턴
    '''
    ## Use Case
    boo : list[unreal.objectbase_] = topaz.get_selected_assets()
    boo : list[unreal.objectbase_] = topaz.get_selected_assets(False)
    boo : list[str] = topaz.get_selected_assets(True)
    '''
    
    assets = unreal.EditorUtilityLibrary.get_selected_assets()
    
    if get_path : 
        asset_paths = []
        for asset in assets :
            asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
            asset_paths.append(asset_path)
        return asset_paths
    else :  
        return assets


def get_selected_asset(get_path : bool = False) -> unreal.Object: #단일 선택 오브젝트 리턴 
    '''
    ## Use Case
    boo : unreal.objectbase_ = topaz.get_selected_asset()
    boo : unreal.objectbase_ = topaz.get_selected_asset(False)
    boo : str = topaz.get_selected_asset(True)
    '''
    if get_path :
        assets = get_selected_assets(True)
    else : 
        assets = get_selected_assets(False)
    if len(assets) > 0:
        return assets[0]
    else:
        return None
    
    
def get_selected_level_actors() -> list[unreal.Actor]: #리스트로 선택된 액터 리턴 
    actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    return actors


def get_selected_level_actor() -> unreal.Actor: #단일 액터 리턴 
    actors = get_selected_level_actors()
    if len(actors) > 0:
        return actors[0]
    else:
        return None


def cutoff_nanite_tri(_static_mesh_ : unreal.StaticMesh) -> float : #나나이트가 특정 트라이 이상일때 나나이트 트라이 퍼센테이지 리턴해줌, legacy
    if _static_mesh_ is not None :
        tri = _static_mesh_.get_num_triangles(0)
        apprx_nanite_tri = tri * 27 
        if apprx_nanite_tri > 1000000 : 
            __desired_triangle_percentage__ = 0.09
        else :
            __desired_triangle_percentage__ = 0.25
    return __desired_triangle_percentage__

def set_actor_tag_by_class(actor : unreal.Actor, seek_class : unreal.Class, desired_tag : str) : #액터에 태그 추가
    actor_tags = actor.tags
    print(actor.get_class())
    if desired_tag not in actor_tags : 
        if actor.__class__ == seek_class :
            print('Tag Added')
            actor_tags.append(desired_tag)
            actor.set_actor_tags(actor_tags)
        else :
            print('Tag Not Added')

def get_materials_from_staticmesh (static_mesh : unreal.StaticMesh, only_blend_mode : bool ) -> list[unreal.MaterialInterface] : #스태틱메쉬에서 메테리얼 리스트로 리턴 
    materials = []
    blendmodes = []
    for i in range(static_mesh.get_num_sections(0)):
        materials.append(static_mesh.get_material(i))
        blendmodes.append(static_mesh.get_material(i).get_blend_mode())
    if only_blend_mode :
        return blendmodes
    else :
        return materials
    
def is_translucent_exist(blendmodes : list[unreal.BlendMode]) -> bool : #트랜스루센트가 있는지 확인
    for blendmode in blendmodes :
        if blendmode == unreal.BlendMode.BLEND_TRANSLUCENT :
            return True
    return False

def get_assets_in_folder(folder_path : str) -> list[str]: #폴더안에 있는 에셋들 리스트로 리턴 
    assets = unreal.EditorAssetLibrary.list_assets(folder_path, True, False)
    return assets

def get_asset_filepath(asset : unreal.Object) -> str: #에셋파일 경로 리턴 
    asset_path = unreal.EditorAssetLibrary.get_path_name_for_loaded_asset(asset)
    return asset_path

def get_cooked_dir () -> str : #Saved 디렉토리 리턴 
    saved_dir = unreal.Paths.project_saved_dir()
    cooked_dir = saved_dir + 'Cooked/Windows'
    print(cooked_dir)
    return cooked_dir


def disable_ray_tracing(static_mesh : unreal.StaticMesh) -> None : #레이트레이싱 끄기
    is_ray_tracing = static_mesh.get_editor_property('support_ray_tracing')
    if is_ray_tracing :
        static_mesh.set_editor_property('support_ray_tracing', False)
        print(static_mesh.get_editor_property('support_ray_tracing'))


def get_asset_from_static_mesh_actor (actor : unreal.Actor) -> unreal.StaticMesh : #액터에서 스태틱메쉬 리턴 
    static_mesh = actor.static_mesh_component.static_mesh
    return static_mesh

def get_textures_list_from_materials(materials : list[unreal.MaterialInterface]) -> list[unreal.Texture] : #메테리얼에서 텍스쳐 리스트로 리턴 
    textures = []
    for material in materials :
        for i in range(material.get_num_texture_parameters()):
            textures.append(material.get_texture_parameter_name(i))
    return textures

def get_actor_bound_size(actor : unreal.Actor) -> float : #액터 바운드 사이즈를 퓨어하게 리턴
    bound = actor.get_actor_bounds(False, True)
    pure_bound = bound[0]
    distance = pure_bound.distance(bound[1])
    length = pure_bound.length()
    print('distance = ' + str(distance))
    print('length = ' + str(length))
    
    return distance


def set_texture_size_by_bound(bound_size : float, texture : unreal.Texture ) -> None : #텍스쳐 사이즈 바운드 사이즈로 설정
    
    size_small : float = 100.0
    size_medium : float = 1000.0
    size_large : float = 10000.0

    print(bound_size)

    if bound_size < size_small : # in case of small size actor 
        texture.set_editor_property('max_texture_size', 512)

    elif bound_size >= size_small and bound_size < size_medium : # in case of medium size actor
        texture.set_editor_property('max_texture_size', 1024)

    elif bound_size >= size_medium and bound_size < size_large : # in case of large size actor
        texture.set_editor_property('max_texture_size', 2048)

    else : # in case of huge size actor
        texture.set_editor_property('max_texture_size', 2048)
        print('Size is too large, but maximum texture size is set to 2048')


def get_all_texture_assets_from_material_instance(material_instance : unreal.MaterialInstance) -> list[unreal.Texture] : #메테리얼 인스턴스에서 텍스쳐 리스트로 리턴 
    textures = []
    for i in range(material_instance.get_num_texture_parameters()):
        textures.append(material_instance.get_texture_parameter_name(i))
    return textures

def export_staticmesh_to_fbx( static_mesh : unreal.StaticMesh, fbx_file_path : str): #staticMeshExporter 
    exportTask = unreal.AssetExportTask()
    exportTask.automated = True
    exportTask.filename = fbx_file_path
    exportTask.object = static_mesh
    exportTask.options = unreal.FbxExportOption()
    exportTask.prompt = False

    fbxExporter = unreal.StaticMeshExporterFBX()
    exportTask.exporter = fbxExporter
    fbxExporter.run_asset_export_task(exportTask)

    return True


    
def reimport_texture ( texture_asset: unreal.Texture2D, tga_file_path : str) : #textureReimporter
    importTask = unreal.AssetImportTask()
    importTask.automated = True
    importTask.filename = tga_file_path
    importTask.destination_path = unreal.Paths.project_content_dir()
    importTask.replace_existing = True
    importTask.save = True
    importTask.factory = unreal.TextureFactory()
    importTask.options = unreal.TextureFactory()
    
    textureFactory = unreal.TextureFactory()
    importTask.factory = textureFactory
    textureFactory.run_asset_import_task(importTask)
    
    return True

class export_texture_task :
    
    def __init__(self) :
        pass
    
    def png (self, texture_asset : unreal.Texture2D, file_path : str) : #textureExporter
        
        exportTask = unreal.AssetExportTask()
        exportTask.automated = True
        exportTask.filename = file_path
        exportTask.object = texture_asset
        exportTask.options = unreal.TextureExporterPNG()
        exportTask.prompt = False
        Exporter = unreal.TextureExporterPNG()
        exportTask.exporter = Exporter
        Exporter.run_asset_export_task(exportTask)
    
        return True

    def tga (self, texture_asset : unreal.Texture2D, file_path : str) : #textureExporter
        
        exportTask = unreal.AssetExportTask()
        exportTask.automated = True
        exportTask.filename = file_path
        exportTask.object = texture_asset
        exportTask.options = unreal.TextureExporterTGA()
        exportTask.prompt = False
        Exporter = unreal.TextureExporterTGA()
        exportTask.exporter = Exporter
        Exporter.run_asset_export_task(exportTask)
        
        return True

    def jpeg (self, texture_asset : unreal.Texture2D, file_path : str) : #textureExporter
        
        exportTask = unreal.AssetExportTask()
        exportTask.automated = True
        exportTask.filename = file_path
        exportTask.object = texture_asset
        exportTask.options = unreal.TextureExporterJPEG()
        exportTask.prompt = False
        Exporter = unreal.TextureExporterJPEG()
        exportTask.exporter = Exporter
        Exporter.run_asset_export_task(exportTask)
        
        return True
    
    def exr (self, texture_asset : unreal.Texture2D, file_path : str) :
        
        exportTask = unreal.AssetExportTask()
        exportTask.automated = True
        exportTask.filename = file_path
        exportTask.object = texture_asset
        exportTask.options = unreal.TextureExporterEXR()
        exportTask.prompt = False
        Exporter = unreal.TextureExporterEXR()
        exportTask.exporter = Exporter
        Exporter.run_asset_export_task(exportTask)
        
        return True
    
def expoert_selected_asset (asset : unreal.Object, destination : str) :
    
    asset_path : str = asset.get_path_name()
    unreal.AssetToolsHelpers.get_asset_tools().export_to_disk(asset_path, destination)
    
    return True

###Initialised message when loaded ###
unreal.log('Topaz initialised...')



