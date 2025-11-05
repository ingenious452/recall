from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.padding import Padding


from recall.core import get_orchestrator
from recall.errors import (
    RecallWriteError,
    RecallReadError, 
    RecallInitError, 
    RecallExistsError
)


app = typer.Typer()


console = Console()


# Repository manager which act as intermediary between cli and database.
@app.command("add")
def add_recall(recall_name: Annotated[str, typer.Argument(help="recall name to add to index.")],
               recall_path: Annotated[Path, typer.Option("--path", "-p", help="path to add to index.")] = Path.cwd()) -> None:

    # TODO: Duplicate path can be added with different project name.
    console.print(f"adding [cyan]'{recall_name}'[/cyan], path: [grey53]{recall_path}[/grey53] to index")
    # console.print(f"path: [grey53]{recall_path}[/grey53]")
    # we don't need to validate that some data has been passed as "" to recall name and path cause it will be validated by recall name and path
    # lower the case for recall name and convert Path to str

    try:
        orchest = get_orchestrator()
        orchest.add(recall_name.lower(), recall_path.as_posix())
        console.print(Padding(f"[green]success:[/green] [cyan]'{recall_name}'[/cyan] added to index.", (1, 0, 0, 0)))
    except RecallInitError as e:
        console.print(Padding(f"[yellow]warning:[/yellow] {e}, please run 'recall init' or use '-f' switch to force init.", (1, 0, 0, 0)))
    except RecallExistsError:
        console.print(Padding(f"[yellow]warning:[/yellow] entry for [cyan]'{recall_name}'[/cyan] already exists in index.", (1, 0, 0, 0)))
    except RecallReadError as e:
        console.print(Padding(f"[red]error:[/red] unable to add [cyan]'{recall_name}'[/cyan] to index, {e}", (1, 0, 0, 0)))
    except RecallWriteError as e:
        console.print(Padding(f"[red]error:[/red] unable to add [cyan]'{recall_name}'[/cyan] to index, {e}", (1, 0, 0, 0)))
    except Exception as e:
        console.print(Padding(f"[red]unexpected error:[/red] {e}", (1, 0, 0, 0)))
