# Should be executed at first


import os
from pathlib import Path

BASE_DIR = Path.cwd()

with open(".env", "w") as env_variables:
    env_variables.write(f"RootDirectory={BASE_DIR}")
