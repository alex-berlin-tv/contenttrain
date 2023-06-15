from expand_paths import do_expand_paths
from folder_list import do_folder_list
from model import NocoEpisodes, SourceState
from youtube_download import do_youtube_download

import json
from pathlib import Path

import typer
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def copy_files():
    """Copies the files from the server to a local folder."""
    print("to be implemented")


@app.command()
def expand_paths(
    path: Annotated[Path, typer.Argument(help="path to file with tree-walk of server")]
):
    """Expand filepaths based on a given text file."""
    with open(path, "r") as f:
        paths = json.load(f)
    episodes = NocoEpisodes.from_nocodb()
    do_expand_paths(episodes, paths)


@app.command()
def folder_walk(
    path: Annotated[Path, typer.Argument(help="output path for file list")],
    text: Annotated[bool, typer.Option(help="write folders as text file")]=False,
    csv: Annotated[bool, typer.Option(help="write folders as csv file")]=False,
):
    """Reads content of source folder and lists containing files to a file."""
    do_folder_list(path, text, csv)


@app.command()
def update_transcoded():
    """Reads Media Encoder's output dir and updates the database accordingly."""
    print("to be implemented")


@app.command()
def youtube_download():
    """Download files from YouTube into the local folder."""
    episodes = NocoEpisodes.from_nocodb()
    do_youtube_download(episodes)


@app.command()
def update_source_state():
    episodes = NocoEpisodes.from_nocodb()
    for episode in episodes.__root__:
        if not episode.server_index or episode.server_index in ["X", ""]:
            episodes.update_source_state(episode, SourceState.unknown)
            continue
        if episode.server_index.startswith("\\\\"):
            episodes.update_source_state(episode, SourceState.disa_server)


if __name__ == "__main__":
    app()