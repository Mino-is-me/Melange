import unreal
import importlib
from Lib import __lib_topaz__ as topaz
from Lib import __lib_kafka__ as kafka

selected = topaz.get_selected_asset()

#topaz.get_selected_assets()

selected = topaz.get_selected_level_actor()

topaz.get_actor_bound_size(selected)