from pathlib import Path

import typer
from typing_extensions import Annotated


app = typer.Typer()


@app.command()
def download_files():
    print("to be implemented")


@app.command()
def expand_paths(
    path: Annotated[Path, typer.Argument]
):
    """Expand filepaths based on a given text file."""
    print("to be implemented")

if __name__ == "__main__":
    app()