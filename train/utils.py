from pathlib import Path
from config import settings

import glob
import os
import re

def transcoded_items_present() -> dict[int, str]:
    rsl: dict[int, str] = {}
    folder = Path(settings.transcoding_destination_folder) # type: ignore
    files = [file for file in folder.iterdir() if file.is_file()]
    print(files)
    pattern = re.compile(r"e-(\d+)_.*")
    for file in files:
        id = pattern.match(str(file))
        if id:
            rsl[int(id.group(1))] = str(file)
    return rsl