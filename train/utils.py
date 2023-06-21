from config import settings

import glob
import os
import re

def transcoded_items_present() -> dict[int, str]:
    rsl: dict[int, str] = {}
    files: list[str] = glob.glob(os.path.join(settings.transcoding_destination_folder, "*")) # type: ignore
    pattern = re.compile(r"e-(\d+)_.*")
    for file in files:
        id = pattern.match(file)
        if id:
            rsl[int(id.group(1))] = file
    return rsl