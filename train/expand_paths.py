from model import NocoEpisode, NocoEpisodes, SourceState

from typing import Optional


def do_expand_paths(episodes: NocoEpisodes, paths: dict[str, str]):
    for episode in episodes.__root__:
        handle_item(episodes, episode, paths)


def handle_item(episodes: NocoEpisodes, episode: NocoEpisode, paths: dict[str, str]):
    if not episode.server_index or episode.server_index == "X":
        return
    if episode.server_index.startswith("\\\\"):
        return
    path = find_path_for_filename(episode.server_index, episode.title, paths)
    if path:
        episodes.update_server_index(episode, path)
        episodes.update_source_state(episode, SourceState.disa_server)
    else:
        episodes.update_source_state(episode, SourceState.index_not_found)

def find_path_for_filename(server_index: str, title: str, paths: dict[str, str]) -> Optional[str]:
    rsl: Optional[str] = None
    if server_index in paths:
        rsl = paths[server_index]
    return rsl