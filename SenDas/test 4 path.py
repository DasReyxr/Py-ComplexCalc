import os
from pathlib import Path, PurePath
RUTA = "D:\Wkn"
Lis_dir= Path(RUTA)
path_dirname= os.path.dirname(os.path.abspath(RUTA))
print(f"Path Dir nei {path_dirname}")