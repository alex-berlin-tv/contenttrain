from csv import Error
from config import settings
from model import NocoEpisode, NocoEpisodes, SourceState

from pathlib import Path

import ffmpeg


def do_transcode(episodes: NocoEpisodes):
    total = episodes.count_by_is_copied(True)
    count = 0
    print(total)
    for episode in episodes.__root__:
        count = handle_item(episodes, episode, count, total)


def handle_item(episodes: NocoEpisodes, episode: NocoEpisode, count: int, total: int) -> int:
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id}, title: '{episode.title}'"
    if episode.is_transcoded:
        print(f"{progress} Already transcoded {description}")
        return count + 1
    print(f"{progress} Transcode {description}")
    try:
        ffmpeg(episode)
    except Error as e:
        print(e)
        return count + 1
    # episodes.update_is_transcoded(episode, True)
    return count + 1


def ffmpeg(episode: NocoEpisode):
    if episode.source_state == SourceState.disa_server and episode.server_index:
        Path(episode.server_index).suffix
    source = Path(settings.transcoding_source_folder) / Path(episode.file_name()) # type: ignore
    destination = Path(settings.transcoding_destination_folder) / Path(episode.file_name()) # type: ignore
    print(source)