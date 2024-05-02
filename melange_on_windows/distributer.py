from Lib import __lib_stelle__ as stelle
import subprocess, os, importlib

importlib.reload(stelle)

def __init__() -> None:
    '''
    # Description: Source Control Support 
    ## Don't use [UnrealPath], use [ExplorerPath] instead
    ### Example: /Game/[Asset] -> D:/CINEVStudio/CINEVStudio/Content/[Asset]
    '''
    print('Distributer Initialized')
    pass


engine_root = stelle.get_engine_root('5.3')
stelle.openFolder(engine_root)