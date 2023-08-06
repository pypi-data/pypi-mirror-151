from .prelude import *

from .timestamp import *


def snapshot() -> str:
    init_tree = repo.index.write_tree()
    timestamp = create_timestamp()

    try:
        signature = repo.get(repo.head.target).author # type: ignore
    except pygit2.GitError:
        raise Exception("Your current repository has no commits! Please commit something first.")
    
    # * Note that .write() is never called, so this doesn't modify the user-facing index
    repo.index.add_all()
    commit_hash = repo.create_commit(
        None,  # type: ignore
        signature,
        signature,
        timestamp,
        repo.index.write_tree(),
        [repo.head.target],
    )
    try:
        repo.create_tag(
            timestamp,
            commit_hash,
            pygit2.GIT_OBJ_COMMIT,
            signature,
            "GIT FLASHBACK SNAPSHOT",
        )
    except pygit2.AlreadyExistsError:
        pass
    
    repo.index.read_tree(init_tree)
    
    return timestamp

