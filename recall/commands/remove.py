import typer
from rich.console import Console


app = typer.Typer()


console = Console()


@app.command("remove")
def remove_project(project: str) -> None:
    console.print("Removing: {project}.")
