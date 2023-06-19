from config import settings

import csv
import json
import os
from pathlib import Path


def do_folder_list(output: Path, as_text: bool, as_csv):
    if as_text and as_csv:
        print("NOUP choose between csv and txt")
        return
    rsl: dict[str, str] = {}
    for root, folders, files in os.walk(settings.file_server_location): # type: ignore
        folder = Path(root)
        for file in files:
            rsl[os.path.splitext(file)[0]] = str(folder / Path(file))
    with open(output, "w") as file:
        if as_text:
           for item in rsl.values():
            file.write(item + "\n") 
        elif as_csv:
            writer = csv.writer(file)
            writer.writerow(["Dateiname", "Pfad"])
            for file_name in rsl:
                writer.writerow([file_name, rsl[file_name]])
        else:
            json.dump(rsl, file)