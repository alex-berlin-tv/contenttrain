from config import settings
from model import FileState, NocoEpisode, NocoEpisodes, SourceState

import os
from pathlib import Path
import re


def do_update(episodes: NocoEpisodes):
   total = len(episodes.__root__) 
   count = 1
   tr_items = transcoded_items_present()
   print(tr_items)
   for episode in episodes.__root__:
    handle_item(episodes, episode, tr_items, count, total)
    count += 1


def handle_item(
    episodes: NocoEpisodes,
    episode: NocoEpisode,
    tr_items: dict[int, str],
    count: int,
    total: int
):
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id}, title: '{episode.title}'"
    if (not episode.server_index or \
       episode.server_index in ["X", ""]) and \
       episode.source_state != SourceState.UNKNOWN:
        print(f"{progress} Set SourceState to Unknown {description}")
        episodes.update_source_state(episode, SourceState.UNKNOWN)
    if episode.server_index and \
       episode.server_index.startswith("\\\\") and \
       episode.source_state != SourceState.DISA_SERVER:
        print(f"{progress} Set SourceState to DiSa-Server {description}")
        episodes.update_source_state(episode, SourceState.DISA_SERVER)
    if not episode.server_index and \
       episode.youtube_url and \
       episode.source_state != SourceState.YOUTUBE:
        print(f"{progress} Set SourceState to YouTube {description}")
        episodes.update_source_state(episode, SourceState.YOUTUBE)
    if episode.source_state == SourceState.DISA_SERVER and episode.server_index:
        suffix = Path(episode.server_index).suffix
        file_path = str(Path(episode.file_name()).with_suffix(suffix))
        if episode.source_file != file_path:
            print(f"{progress} Set Source File from Server Index {description}")
            episodes.update_source_file(episode, file_path)
    if (episode.file_on_edit_state == FileState.EXISTS or \
       episode.file_on_edit_state == FileState.DONE) and \
       episode.noco_id in tr_items and \
       not episode.is_transcoded:
        print(f"{progress} Set transcoded state to True {description}")
        episodes.update_is_transcoded(episode, True) 


def transcoded_items_present() -> dict[int, str]:
    rsl: dict[int, str] = {}
    files: list[str] = []
    for root, folders, f in os.walk(settings.transcoding_destination_folder): # type: ignore
        files = f
    pattern = re.compile(r"e-(\d+)_.*")
    for file in files:
        id = pattern.match(file)
        if not id:
            raise ValueError(f"couldn't parse id from filename {file}")
        rsl[int(id.group(1))] = file
    return rsl