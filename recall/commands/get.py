import typer
from rich.console import Console
from rich.padding import Padding

from recall.core import get_recaller
from recall import ERRORS

app = typer.Typer()


console = Console()


@app.command("get")
def recall_project(recall_name: str) -> None:
    recaller = get_recaller()
    project, error = recaller.open(recall_name)
    if error:
        console.print(Padding(f"[red]Error:[/red] Unable to get [grey53]'{project['project_name']}' at {project['project_path']}[/grey53], {ERRORS[error]}", (1, 0, 0, 0)))
    else:
        console.print(Padding(f"[green]Success:[/green] got [grey53]'{project['project_name']}' at {project['project_path']}[/grey53]", (1, 0, 0, 0)))
