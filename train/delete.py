from config import settings
from model import FileState, NocoEpisode, NocoEpisodes
from utils import print_id_files, items_present

import os
from pathlib import Path


def do_delete(episodes: NocoEpisodes, do_step: bool, print_tr_items: bool):
    total = episodes.count_by_is_transcoded(True)
    count = 1
    raw_items = items_present(settings.transcoding_source_folder) # type: ignore
    tr_items = items_present(settings.transcoding_destination_folder) # type: ignore
    print_id_files(tr_items, print_tr_items)
    for episode in episodes.__root__:
        count = handle_item(episodes, episode, raw_items, tr_items, do_step, count, total)


def handle_item(
    episodes: NocoEpisodes,
    episode: NocoEpisode,
    raw_items: dict[int, str],
    tr_items: dict[int, str],
    do_step: bool,
    count: int,
    total: int
):
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id}, title: '{episode.title}'"
    if not episode.is_transcoded or \
       episode.noco_id not in tr_items or \
       episode.file_on_edit_state == FileState.DONE:
        return count
    if not episode.noco_id not in raw_items:
        print(f"Error could not find item in source {description}")
    source = raw_items[episode.noco_id]
    print(f"{progress} Delete transcoding source file {source}")
    if do_step:
        print(source)
        input(f"-> Press enter to proceed with the next item")
    os.remove(source)
    print(f"{progress} Set file on edit state to done {description}")
    episodes.update_file_on_edit_state(episode, FileState.DONE)
    return count + 1