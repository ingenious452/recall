import typer
from rich.console import Console


app = typer.Typer()


console = Console()


@app.command("init")
def init_recall(project: str) -> None:
    console.print("Opening: {project}.")
