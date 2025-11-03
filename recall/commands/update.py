import typer
from rich.console import Console


app = typer.Typer()


console = Console()


@app.command("update")
def update_project(project: str) -> None:
    console.print("Updating: {project}.")
