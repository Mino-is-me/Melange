import unreal 
from Lib import __lib_topaz__ as topaz

import importlib

importlib.reload(topaz)

selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
# print(selectedAssets[0])
for asset in selectedAssets:
    staticMeshsInBP = topaz.get_component_by_class(asset, unreal.StaticMeshComponent)

    directoryPath = asset.get_path_name()
    part = directoryPath.split('/')
    staticMeshesDirectory = '/'.join(part[:6]) + '/StaticMesh' 
    print(staticMeshesDirectory)

    for staticMesh in staticMeshsInBP:
        # print(staticMesh.static_mesh.get_name())
        arr = staticMesh.static_mesh.get_path_name().split('/')
        length = len(arr)
        staticMeshFilesName = arr[length-1]
        targetPath = staticMeshesDirectory + '/' + staticMeshFilesName
        sourcePath = staticMesh.static_mesh.get_path_name()
        print(sourcePath, "sourcePath")
        print(targetPath, "targetPath")
        if(targetPath != sourcePath):
            result = unreal.EditorAssetLibrary.rename_asset(sourcePath, targetPath)
            print(result)