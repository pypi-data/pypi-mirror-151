import sys
init_modules = sys.modules.copy()

import pygit2
from typing import * # type: ignore
from types import ModuleType
from io import BufferedWriter

repo = pygit2.Repository(".") 
