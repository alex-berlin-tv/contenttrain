from config import settings
from model import FileState, NocoEpisode, NocoEpisodes
from utils import transcoded_items_present

import os
from pathlib import Path


def do_delete(episodes: NocoEpisodes, do_step: bool):
    total = episodes.count_by_is_transcoded(True)
    count = 1
    tr_items = transcoded_items_present()
    print(tr_items)
    for episode in episodes.__root__:
        count = handle_item(episodes, episode, tr_items, do_step, count, total)


def handle_item(
    episodes: NocoEpisodes,
    episode: NocoEpisode,
    tr_items: dict[int, str],
    do_step: bool,
    count: int,
    total: int
):
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id}, title: '{episode.title}'"
    if not episode.is_transcoded or \
       episode.noco_id not in tr_items:
        return count
    source = Path(settings.transcoding_source_folder) / episode.source_file # type: ignore
    print(f"{progress} Delete transcoding source file {source}")
    if do_step:
        input(f"-> Press enter to proceed with the next item")
    os.remove(source)
    print(f"{progress} Set file on edit state to done {description}")
    episodes.update_file_on_edit_state(episode, FileState.DONE)
    return count + 1