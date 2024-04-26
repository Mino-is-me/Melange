import unreal

# Specify the path of the texture file you want to reimport
texture_path = "D:/CINEVStudio/CINEVStudio/Content/MetaHumans/Common/Models/FaceTexture-8k/chr_0014/head_wm1_normal_map.png"

# Reimport the texture asset
selectedAssets = unreal.EditorUtilityLibrary.get_selected_assets()
selectedAsset = selectedAssets[0]

print(selectedAsset)
AssetImportData = selectedAsset.get_editor_property('asset_import_data')
print('AssetImportData', AssetImportData)
source_data = AssetImportData.get_editor_property('source_data')
extract_filenames = AssetImportData.extract_filenames()
get_first_filename = AssetImportData.get_first_filename()
print('sourceFile ', source_data)
print('extract_filenames ', extract_filenames)
print('get_first_filename ', get_first_filename)
# .get_editor_property('source_file')

print('HO!')
# AssetImportData.scripted_add_file_name()
# print(AssetImportData.scripted_add_file_name)
