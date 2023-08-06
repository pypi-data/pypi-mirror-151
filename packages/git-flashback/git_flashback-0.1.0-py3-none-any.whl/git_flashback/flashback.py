from .prelude import *

from .timestamp import *

import contextlib
from .gitimport import add_repository_to_path, GitImporter
import sys


class InvalidTimestampOrRef(Exception):
    pass


def flashback(timestamp_or_ref: str):
    assert isinstance(timestamp_or_ref, str)
    
    timestamp_or_ref = timestamp_or_ref.split("/")[-1]

    if git_head_matches_timestamp(timestamp_or_ref):
        return dummy_context_manager()
    else:
        return load_modules_from_git(timestamp_or_ref)
        


@contextlib.contextmanager
def dummy_context_manager():
    yield sys.modules


@contextlib.contextmanager
def load_modules_from_git(rev="HEAD", repo=".", in_repo_path=""):
    current_modules = sys.modules.copy()
    sys.modules.clear()
    sys.modules.update(init_modules)
    try:
        path = add_repository_to_path(repo, rev, in_repo_path)
    except KeyError:
        raise InvalidTimestampOrRef()

    final_modules = {}
    yield final_modules
    
    sys.path.remove(path)
    sys.path_hooks.remove(GitImporter)
    final_modules.update(sys.modules)
    sys.modules.clear()
    sys.modules.update(current_modules)
