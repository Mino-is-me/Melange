
from Lib import __lib_stelle__ as stelle
import importlib

importlib.reload(stelle)

def __init__() -> None:
    print('Distributer Initialized')
    pass

engine_version = '5.3'

engine_root = stelle.get_engine_root(engine_version)
shader_root = engine_root + 'shaders'
print(shader_root)
stelle.openFolder(shader_root)