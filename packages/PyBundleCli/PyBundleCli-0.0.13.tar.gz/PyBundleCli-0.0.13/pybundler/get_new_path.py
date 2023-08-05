from pathlib import Path
import os


def get_new_path():
    paths = list(Path('./dist').glob(r'*.tar.gz'))
    paths.sort(key=os.path.getmtime)
    return paths[-1]
