import unreal 

textures:list[unreal.Texture2D] = unreal.EditorUtilityLibrary.get_selected_assets()

if not textures:
    unreal.log_warning("No textures selected.")
for texture in textures:
    texture.mip_gen_settings = unreal.TextureMipGenSettings.TMGS_SHARPEN4
    texture.set_editor_property('mip_gen_settings', unreal.TextureMipGenSettings.TMGS_SHARPEN4)
    #texture.post_edit_change()
    print(f"Set Mip Gen Settings for {texture.get_name()} to TMGS_SHARPEN4")