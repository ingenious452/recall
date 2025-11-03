import typer
from rich.console import Console


app = typer.Typer()


console = Console()


@app.command("remove")
def remove_recall(project: str) -> None:
    console.print("Removing: {project}.")
