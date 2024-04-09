import unreal, importlib
from Lib import __lib_topaz__ as topaz
importlib.reload(topaz)

selected = topaz.get_selected_assets()

for asset in selected:
    unreal.MaterialEditingLibrary.recompile_material(asset)
    pass