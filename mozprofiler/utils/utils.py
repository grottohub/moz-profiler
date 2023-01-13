import os
import re

import fileinput

from contextlib import contextmanager
from pathlib import Path
from typing import List, Tuple


def is_ignored(needle: str, ignore: List[str]) -> bool:
    for pattern in ignore:
        if re.search(pattern, needle):
            return True

    return False


def os_walk_with_ignore(starting_dir: str, ignore: List[str]) -> Tuple[str, List[str], List[str]]:
    for folder in os.walk(starting_dir):
        if not is_ignored(folder[0], ignore):
            print(f"FOLDER: {folder}")
            return folder
        else:
            return "ignored", [], []

    return "finished", [], []


def get_rc_file() -> str:
    home = Path.home()
    # Default to .bashrc
    rcfile = f"{home}/.bashrc"

    # Check for other shell rc files
    # TODO: add more
    if os.path.exists(f"{home}/.zshrc"):
        rcfile = f"{home}/.zshrc"

    return rcfile


@contextmanager
def load_rc_file_in_place():
    rcfile = get_rc_file()

    with fileinput.FileInput(rcfile, inplace=True, backup=".bak") as rc:
        yield rc
