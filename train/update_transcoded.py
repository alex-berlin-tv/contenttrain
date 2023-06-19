from config import settings
from model import NocoEpisodes, SourceState

import os


def do_update_transcoded():
    pass


def get_transcoded():
    for root, folders, files in os.walk(settings.transcoding_destination_folder): # type: ignore
        for file in files:
            print(extract_id(file))


def extract_id(file: str) -> int:
    return 0