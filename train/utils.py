from config import settings

import os
import re

IGNORE = ["desktop.ini"]


def transcoded_items_present() -> dict[int, str]:
    rsl: dict[int, str] = {}
    files: list[str] = []
    for root, folders, f in os.walk(settings.transcoding_destination_folder): # type: ignore
        files = f
    pattern = re.compile(r"e-(\d+)_.*")
    for file in files:
        if file in IGNORE:
            continue
        id = pattern.match(file)
        if not id:
            raise ValueError(f"couldn't parse id from filename {file}")
        rsl[int(id.group(1))] = file
    return rsl