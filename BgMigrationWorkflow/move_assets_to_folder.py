import unreal 
from Lib import __lib_topaz__ as topaz
import importlib

importlib.reload(topaz)


assets = topaz.get_selected_assets()

# Connect to the Unreal Editor
editor = unreal.EditorAssetLibrary()

target_asset = "/Game/Customizing/Users/Deemo/MoveAssetsTest/NewBlueprint.NewBlueprint"
target_destination = "/Game/Customizing/Users/Deemo/MoveAssetsTest/hi/NewBlueprint.NewBlueprint"

# editor.duplicate_asset(target_asset, target_destination)
# Specify the source and destination paths for the assets
source_path = target_destination
destination_path = target_asset

# # Get the asset registry
# asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# # Get the asset data for the asset to move
# asset_data = asset_registry.get_asset_by_object_path(source_path)

unreal.EditorAssetLibrary.rename_asset(source_path, destination_path)
# if asset_data:
#     # Move the asset to the destination path
#     if result:
#         print("Asset moved successfully from", source_path, "to", destination_path)
        
#     else:
#         print("Failed to move asset.")
# else:
#     print("Asset not found at", source_path)