import unreal
import importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_stelle__ as stelle
importlib.reload(topaz)
importlib.reload(stelle)

__all__ = ['get_all_leveL_actors','assetValidator','bulk_renamer','spine_breaker','unused_asset_notifier']

def get_all_leveL_actors() -> list[unreal.Actor]: #리스트로 선택된 액터 리턴
    actors = unreal.EditorLevelLibrary.get_all_level_actors()
    return actors

def assetValidator(folder_path : str) -> list[str] : #Returns a list of assets that are too long
    need_to_return = []
    assets = topaz.get_assets_in_folder(folder_path)
    for asset in assets:
        file_len = len(asset)
        if file_len > 235 :
            need_to_return.append(asset)
            print('Asset Name : ' + asset + ' is too long. Please rename it.' + ' Length : ' + str(file_len) )
    return need_to_return

def bulk_renamer(asset_path_list : str) -> None:
    for i in asset_path_list:
        #print(i)
        if '_BaseColor' in i:
            newName = i.replace('_BaseColor','_D')
        elif '_Normal' in i:
            newName = i.replace('_Normal','_N')
        elif '_OcclusionRoughnessMetallic' in i:
            newName = i.replace('_OcclusionRoughnessMetallic','_ORM')
        else:
            newName = i
        unreal.EditorAssetLibrary.rename_asset(i,newName)
        print('Renamed ' + i + ' to ' + newName)

def spine_breaker():
    all_actors = get_all_leveL_actors()
    for actor in all_actors:
        if actor.get_class() == unreal.StaticMeshActor() :
            print('staticmeshactor')
            
        elif actor.get_class() == unreal.blueprint() :
            print('blueprint')
            #spine_breaker(topaz.get_selected_level_actor())
            
            
def unused_asset_notifier(workingPath : str) -> list[str]: #검증 덜됨 
    need_to_return = []
    @unreal.uclass()
    class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
        pass

    editorAssetLib = GetEditorAssetLibrary();

    allAssets = editorAssetLib.list_assets(workingPath, True, False)

    if (len(allAssets) > 0):
        for asset in allAssets:
            deps = editorAssetLib.find_package_referencers_for_asset(asset, False)
            if (len(deps) == 0):
                print (">>>%s" % asset)
                need_to_return.append(asset)
    return need_to_return

def get_all_textures_in_folder (working_path : str) -> list[unreal.Texture2D]:
    need_to_return = []
    
    @unreal.uclass()
    class GetEditorAssetLibrary(unreal.EditorAssetLibrary):
        pass

    editorAssetLib = GetEditorAssetLibrary();

    allAssets : list[str] = editorAssetLib.list_assets(working_path, True, False)
    if (len(allAssets) > 0):
        for asset in allAssets:
            loaded_asset = editorAssetLib.load_asset(asset)
            #print(loaded_asset.__class__)
            if loaded_asset.__class__ == unreal.Texture2D:
                #print('yes')
                need_to_return.append(loaded_asset)
    print(str(len(need_to_return)) + ' textures found')
    return need_to_return
    
## Todo : get only Selected Sublevel actors 
def get_actors_selected_sublevel () -> list[unreal.Actor]: ## WIP 
    selected_actors = unreal.EditorLevelLibrary.get_selected_level_actors()
    return selected_actors



###Initialised message when loaded ###
unreal.log('archeron initialised...')
