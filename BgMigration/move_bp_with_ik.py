import unreal
from Lib import __lib_topaz__ as topaz

import importlib

importlib.reload(topaz)

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()

for asset in selectedAssets:
    hasIK = False
    objectsInBP = topaz.get_component_objects(asset.get_path_name())
    for objectInBP in objectsInBP:
        hasInteractionPoint = objectInBP.get_name().find('InteractionPoint')
        
        if hasInteractionPoint != -1:
            hasIK = True
            break
    if hasIK:
        directoryPath = asset.get_path_name()
        part = directoryPath.split('/')
        staticMeshesDirectory = '/'.join(part[:6]) + '/IK/' 
        bpFileName = asset.get_name()
        sourcePath = directoryPath
        targetPath = staticMeshesDirectory + '/' + bpFileName
        
        result = unreal.EditorAssetLibrary.rename_asset(sourcePath, targetPath)
        print(result)
    else:
        print ('This asset does not have IK')
    
