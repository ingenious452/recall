import typer
from rich.console import Console

from pathlib import Path


app = typer.Typer()


console = Console()


@app.command("add")
def add_project(project: str, project_path: Path) -> None:
    console.print("Adding: {project} at {path}.")
