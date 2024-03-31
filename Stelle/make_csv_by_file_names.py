import sys
import os 
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from Lib import __lib_stelle__ as stelle

files : list[str] = stelle.get_filenames(Path.cwd())
stelle.write_list_to_csv(files,os.getcwd())

