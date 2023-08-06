from .prelude import *

from datetime import datetime


def create_timestamp() -> str:
    return datetime.now().isoformat(timespec="seconds").replace("-", "").replace(":", "")


def git_head_matches_timestamp(timestamp: str) -> bool:
    return (
        repo.describe(
            describe_strategy=pygit2.GIT_DESCRIBE_TAGS, show_commit_oid_as_fallback=True
        )
        == timestamp
    )