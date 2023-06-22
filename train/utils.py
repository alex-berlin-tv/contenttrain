from pathlib import Path
from config import settings

import glob
import os
from pathlib import Path
import re


def folder_walk(path: Path) -> list[Path]:
    rsl: list[Path] = []
    for item in path.iterdir():
        if item.is_file():
            rsl.append(item.absolute())
        elif item.is_dir():
            try:
                rsl.extend(folder_walk(item))
            except PermissionError:
                continue
    return rsl


def items_present(folder: Path) -> dict[int, str]:
    rsl: dict[int, str] = {}
    folder = Path(folder) # type: ignore
    # files = [file for file in folder.iterdir() if file.is_file()]
    files = folder_walk(folder)
    print(files)
    pattern = re.compile(r"e-(\d+)_.*")
    for file in files:
        id = pattern.match(str(file.name))
        if id:
            rsl[int(id.group(1))] = str(file)
    return rsl


def print_id_files(items: dict[int, str], print_items: bool):
    if print_items:
        for key, value in items.items():
            print(f"{key}:\t {value}")