from model import NocoEpisode, NocoEpisodes, SourceState

from pathlib import Path


def do_update(episodes: NocoEpisodes):
   total = len(episodes.__root__) 
   count = 1
   for episode in episodes.__root__:
    handle_item(episodes, episode, count, total)
    count += 1


def handle_item(episodes: NocoEpisodes, episode: NocoEpisode, count: int, total: int):
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id}, title: '{episode.title}'"
    if not episode.server_index or \
       episode.server_index in ["X", ""] and \
       episode.source_state != SourceState.unknown:
        print(f"{progress} Set SourceState to Unknown {description}")
        episodes.update_source_state(episode, SourceState.unknown)
    if episode.server_index and \
       episode.server_index.startswith("\\\\") and \
       episode.source_state != SourceState.disa_server:
        print(f"{progress} Set SourceState to DiSa-Server {description}")
        episodes.update_source_state(episode, SourceState.disa_server)
    if not episode.server_index and \
       episode.youtube_url and \
       episode.source_state != SourceState.youtube:
        print(f"{progress} Set SourceState to YouTube {description}")
        episodes.update_source_state(episode, SourceState.youtube)
    if episode.source_state == SourceState.disa_server and episode.server_index:
        print(f"{progress} Set Source File from Server Index {description}")
        suffix = Path(episode.server_index).suffix
        file_path = str(Path(episode.file_name()).with_suffix(suffix))
        if episode.source_file != file_path:
            episodes.update_source_file(episode, file_path)
