import typer
from rich.console import Console


app = typer.Typer()


console = Console()


@app.command("view")
def view_projects() -> None:
    console.print("Listing all the projects")
