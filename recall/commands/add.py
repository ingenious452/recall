import typer
from rich.console import Console
from rich.padding import Padding

from pathlib import Path

from recall.core import get_recaller
from recall import ERRORS

app = typer.Typer()


console = Console()

# Repository manager which act as intemediary between cli and database.
@app.command("add")
def add_recall(recall_name: str, recall_path: Path) -> None:
    recaller = get_recaller()
    # TODO: Duplicate path can be added with different project name.
    console.print(f"Registering [grey53]'{recall_name}'[/grey53] to index..")
    console.print(f"Path: [grey53]{recall_path}[/grey53]")
    __, error = recaller.save(recall_name, recall_path.as_posix())
    if error:
        console.print(Padding(f"[red]Error:[/red] Unable to add [grey53]'{recall_name}'[/grey53] to index, {ERRORS[error]}", (1, 0, 0, 0)))
    else:
        console.print(Padding(f"[green]Success:[/green] [grey53]'{recall_name}'[/grey53] added to index.", (1, 0, 0, 0)))