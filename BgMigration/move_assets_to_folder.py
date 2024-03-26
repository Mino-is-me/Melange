import unreal 
from BgMigration import __BgMigration_table__ as testtest
import importlib

importlib.reload(testtest)

print(testtest.datatable())

target_asset = "/Game/Customizing/Users/Deemo/MoveAssetsTest/NewBlueprint.NewBlueprint"
target_destination = "/Game/Customizing/Users/Deemo/MoveAssetsTest/hi/NewBlueprint.NewBlueprint"

source_path = target_asset
destination_path = target_destination

# asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()

# asset_data = asset_registry.get_asset_by_object_path(source_path)

# if asset_data:
#     result = unreal.EditorAssetLibrary.rename_asset(source_path, destination_path)
#     if result:
#         print("Asset moved successfully from", source_path, "to", destination_path)

#     else:
#         print("Failed to move asset.")
# else:
#     print("Asset not found at", source_path)