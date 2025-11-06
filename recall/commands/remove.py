from typing import Annotated

import typer
from rich.console import Console
from rich.padding import Padding

from recall.core import get_orchestrator
from recall.errors import (
    RecallWriteError, 
    RecallInitError, 
    RecallReadError, 
    RecallNotFoundError
)


app = typer.Typer()


console = Console()


@app.command("remove")
def remove_recall(recall_name: Annotated[str, typer.Argument(help="name to be removed from index")]) -> None:

    # console.print(f"path: [grey53]{recall_path}[/grey53]")
    # we don't need to validate that some data has been passed as "" to recall name and path cause it will be validated by recall name and path
    # lower the case for recall name and convert Path to str

    __ = typer.confirm(f"are you sure you want to remove {recall_name} from index?", abort=True)
    console.print(f"[bold]removing[/bold] [cyan]'{recall_name}'[/cyan] from index")


    try:
        orchest = get_orchestrator()
        indexed_path = orchest.remove(recall_name.lower())
        console.print(Padding(f"[green]success:[/green] [cyan]'{recall_name}'[/cyan], path: [grey53]{indexed_path}[/grey53] removed from index.", (1, 0, 0, 0)))
    except RecallInitError as e:
        console.print(Padding(f"[yellow]warning:[/yellow] {e}, please run 'recall init' or use '-f' switch to force init.", (1, 0, 0, 0)))
    except RecallReadError as e:
        console.print(Padding(f"[red]error:[/red] unable to remove [cyan]'{recall_name}'[/cyan] from index, {e}", (1, 0, 0, 0)))
    except RecallNotFoundError as e:
        console.print(Padding(f"[yellow]warning:[/yellow] no entry for [cyan]'{recall_name}'[/cyan] exists in index", (1, 0, 0, 0)))
    except RecallWriteError as e:
        console.print(Padding(f"[red]error:[/red] unable to remove [cyan]'{recall_name}'[/cyan] from index, {e}", (1, 0, 0, 0)))
    except Exception as e:
        console.print(Padding(f"[red]unexpected error:[/red] {e}", (1, 0, 0, 0)))
