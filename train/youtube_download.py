from config import settings
from model import FileState, NocoEpisodes, NocoEpisode, SourceState

from pathlib import Path

from yt_dlp import YoutubeDL,  YoutubeDL


def do_youtube_download(episodes: NocoEpisodes):
    total = episodes.count_by_source_state(SourceState.YOUTUBE)
    count = 1
    for episode in episodes.__root__:
        count = handle_item(episodes, episode, count, total)


def handle_item(episodes: NocoEpisodes, episode: NocoEpisode, count: int, total: int) -> int:
    progress = f"[{count}/{total}]"
    description = f"item e-{episode.noco_id} from {episode.youtube_url}, title: '{episode.title}'"
    if episode.source_state != SourceState.YOUTUBE:
        return count
    if not episode.youtube_url or episode.youtube_url == "":
        print(f"No YouTube URL for item with id e-{episode.noco_id} and title '{episode.title}' ignoring this entry")
        return count + 1
    if episode.file_on_edit_state == FileState.EXISTS:
        print(f"{progress} Already downloaded {description}")
        return count + 1
    print(f"{progress} Download {description}")
    base = Path(settings.transcoding_source_folder) # type: ignore
    options = {
        'outtmpl': f"{base}/{episode.file_name()}.%(ext)s",
    }
    with YoutubeDL(options) as ydl:
        ydl.download([episode.youtube_url])
    episodes.update_file_on_edit_state(episode, FileState.EXISTS)
    return count + 1