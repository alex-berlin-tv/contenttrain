from expand_paths import do_expand_paths
from model import NocoEpisodes

from pathlib import Path

import typer
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def download_files():
    """Copies the files from the server to a local folder."""
    print("to be implemented")


@app.command()
def expand_paths(
    path: Annotated[Path, typer.Argument(help="path to file with tree-walk of server")]
):
    """Expand filepaths based on a given text file."""
    with open(path, "r") as f:
        paths = [line.strip() for line in f.readlines()]
    episodes = NocoEpisodes.from_nocodb()
    do_expand_paths(episodes, paths)


@app.command()
def update_transcoded():
    """Reads Media Encoder's output dir and updates the database accordingly."""
    print("to be implemented")


if __name__ == "__main__":
    app()