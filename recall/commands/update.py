from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.padding import Padding

from recall.core import get_orchestrator
from recall.errors import (
    RecallInitError, 
    RecallWriteError, 
    RecallReadError, 
    RecallNotFoundError
)


app = typer.Typer()


console = Console()


@app.command("update")
def update_recall(recall_name: Annotated[str, typer.Argument(help="Project name to be recalled.")],
                  recall_path: Annotated[Path, typer.Option("--path", "-p",
                                                            help="Path of the project folder to be updated")] = Path.cwd()) -> None:
    # take confirmation


    __ = typer.confirm(f"Are you sure you want to update '{recall_name}' path to {recall_path}?", abort=True)
    console.print(f"updating [cyan]'{recall_name}'[/cyan] to path: {recall_path} in index")


    try:
        orchest = get_orchestrator()
        indexed_path = orchest.update(recall_name.lower(), recall_path.as_posix())

        console.print(Padding(f"[green]success:[/green] [cyan]'{recall_name}'[/cyan], path: [grey53]{indexed_path}[/grey53] -> [blue]{recall_path}[/blue] updated in index.", (1, 0, 0, 0)))
    except RecallInitError as e:
        console.print(Padding(f"[yellow]warning:[/yellow] {e}, please run 'recall init' or use '-f' switch to force init.", (1, 0, 0, 0)))
    except RecallReadError as e:
        console.print(Padding(f"[red]error:[/red] unable to update [cyan]'{recall_name}'[/cyan] in index, {e}", (1, 0, 0, 0)))
    except RecallNotFoundError as e:
        console.print(Padding(f"[yellow]warning:[/yellow] no entry for [cyan]'{recall_name}'[/cyan] exists in index", (1, 0, 0,0)))
    except RecallWriteError as e:
        console.print(Padding(f"[red]error:[/red] unable to update [cyan]'{recall_name}'[/cyan] in index, {e}", (1, 0, 0, 0)))
    except Exception as e:
        console.print(Padding(f"[red]unexpected error:[/red] {e}", (1, 0, 0, 0)))
