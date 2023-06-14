from model import NocoEpisode, NocoEpisodes

from typing import Optional


def do_expand_paths(episodes: NocoEpisodes, paths: list[str]):
    for episode in episodes.__root__:
        handle_item(episodes, episode, paths)


def handle_item(episodes: NocoEpisodes, episode: NocoEpisode, paths: list[str]):
    if not episode.server_index or episode.server_index == "X":
        return
    if episode.server_index.startswith("\\\\"):
        return
    path = find_path_for_filename(episode.server_index, episode.title, paths)
    if path:
        episodes.update_server_index(episode.noco_id, path)

def find_path_for_filename(server_index: str, title: str, paths: list[str]) -> Optional[str]:
    rsl: Optional[str] = None
    for path in paths:
        if server_index in path:
            if rsl:
                print(f"there is more than one result for index {server_index}, cancel operation for {title}")
                return None
            rsl = path
    return rsl