import typer
from rich.console import Console


app = typer.Typer()


console = Console()


@app.command("get")
def get_project(project: str) -> None:
    console.print("Opening: {project}.")
