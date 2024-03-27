import unreal
import importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_stelle__ as stelle
importlib.reload(topaz)
importlib.reload(stelle)

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
            
def report_unused_asset (folder_path : str) -> list[str]:
    workingPath = "/Game/"
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
#bulk_renamer(shit_list)
#stelle.write_list_to_csv(shit_list, r'D:/art_Narr_SpicePro/CINEVStudio/Content/Python/Debug')
###Initialised message when loaded ###
unreal.log('archeron initialised...')



