from config import settings
from model import NocoEpisodes, NocoEpisode, SourceState

import shutil
from pathlib import Path


def do_import_files(episodes: NocoEpisodes):
    total = episodes.count_by_source_state(SourceState.disa_server) 
    count = 1
    for episode in episodes.__root__:
        count = handle_item(episodes, episode, count, total)


def handle_item(episodes: NocoEpisodes, episode: NocoEpisode, count: int, total: int) -> int:
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id}, title: '{episode.title}'"
    if episode.source_state != SourceState.disa_server:
        return count
    if not episode.server_index or episode.server_index == "":
        print(f"No server_index path for item with id e-{episode.noco_id} and title '{episode.title}' ignoring this entry")
        return count + 1
    if episode.is_copied:
        print(f"{progress} Already copied {description}")
        return count + 1
    print(f"{progress} Copy {description}")
    source = episode.local_server_source_path()
    destination = Path(settings.transcoding_source_folder) / Path(episode.file_name()).with_suffix(source.suffix) # type: ignore
    if not source:
        return count + 1
    shutil.copy(
        str(source),
        str(destination)
    )
    episodes.update_is_copied(episode, True)
    return count + 1