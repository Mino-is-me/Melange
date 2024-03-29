import unreal
import importlib
from Lib import __lib_topaz__ as topaz

importlib.reload(topaz)

#topaz.get_selected_assets()

selected = topaz.get_selected_level_actor()

topaz.get_actor_bound_size(selected)