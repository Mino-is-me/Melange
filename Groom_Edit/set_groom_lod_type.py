import unreal 
from Lib import __lib_topaz__ as topaz
import importlib
importlib.reload(topaz)

origin = unreal.load_asset('/Game/Customizing/Character/senie_Test/Character/A_Head/A_Head_Brow.A_Head_Brow')

lodset = origin.hair_groups_lod
HairGroupLOD = lodset[0]

asset_list = topaz.get_selected_assets()

for each in asset_list: 
    isGroom = each.__class__ == unreal.GroomAsset 
    eachname = each.get_full_name()
    sourceFilename = each.get_editor_property("asset_import_data").get_first_filename()
    unreal.log(sourceFilename)
    #print(eachname)
    if isGroom and sourceFilename != '':
        _hair_groups_lod_ = []
        lodLength = len(each.hair_groups_lod)
        print(lodLength)
        for i in range(lodLength) :
            _hair_groups_lod_.append(HairGroupLOD)
        each.hair_groups_lod = _hair_groups_lod_
        print(len(_hair_groups_lod_))
        #unreal.EditorAssetLibrary.checkout_asset(eachname)
        

## 아직 버그있음 