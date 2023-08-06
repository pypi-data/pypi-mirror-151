from typing import List, Optional

from .bash_client import execute_cmd


def get_diff_compared_to(branch: Optional[str]) -> List[str]:
    cmd = "git diff --name-only"

    if branch:
        cmd = f'{cmd} {branch}'

    return execute_cmd(cmd)


def get_last_commit_hash() -> str:
    cmd = 'git rev-parse --short HEAD '
    return execute_cmd(cmd)[0]
