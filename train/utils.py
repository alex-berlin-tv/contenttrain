from pathlib import Path
from config import settings

import glob
import os
import re

def transcoded_items_present() -> dict[int, str]:
    rsl: dict[int, str] = {}
    folder = Path(settings.transcoding_destination_folder) # type: ignore
    files = [file.name for file in folder.iterdir() if file.is_file()]
    pattern = re.compile(r"e-(\d+)_.*")
    for file in files:
        id = pattern.match(str(file))
        if id:
            rsl[int(id.group(1))] = str(file)
    return rsl


def print_transcoded_items(items: dict[int, str], print_items: bool):
    if print_items:
        for key, value in items.items():
            print(f"{key}:\t {value}")