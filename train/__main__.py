from delete import do_delete
from import_files import do_import_files
from expand_paths import do_expand_paths
from folder_list import do_folder_list
from model import NocoEpisodes, FileState
from update import do_update
from youtube_download import do_youtube_download

import json
from pathlib import Path

import typer
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def delete_transcoded(
    disable_step: Annotated[bool, typer.Option(help="diasble confirm after every deletion")]=False,
):
    """Delete files in the transcoding source folder if they marked as transcoded."""
    episodes = NocoEpisodes.from_nocodb()
    do_delete(episodes, not disable_step)


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
def import_files():
    """Import files into media encoder's source folder."""
    episodes = NocoEpisodes.from_nocodb()
    do_import_files(episodes)


@app.command()
def update():
    episodes = NocoEpisodes.from_nocodb()
    do_update(episodes)


@app.command()
def youtube_download():
    """Download files from YouTube into the local folder."""
    episodes = NocoEpisodes.from_nocodb()
    do_youtube_download(episodes)


@app.command()
def upgrade():
    pass


if __name__ == "__main__":
    app()