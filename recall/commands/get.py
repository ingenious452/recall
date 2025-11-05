from typing import Annotated, Optional

import typer
from rich.console import Console

from recall.core import get_orchestrator
from recall.errors import RecallNotFoundError, RecallReadError


app = typer.Typer()


console = Console()


@app.command("get")
def recall_project(recall_id: Annotated[Optional[int], typer.Argument(help="open the directory by 'id'")] = None,
                   recall_name: Annotated[Optional[str], typer.Option("--name", help="open directory by 'name'")] = None,
) -> None:

    if recall_id and recall_name:
        raise typer.BadParameter(f"Cannot provide both recall_id and recall_name at the same time, please check help.")

    index = recall_id or recall_name

    if index is None:
        raise typer.BadParameter(f"Please provide either recall_id or recall_name, check --help.")

    try:
        orchest = get_orchestrator()
        a = orchest.get(index)
        print(f"path is: {a}")

    except RecallNotFoundError as e:
        console.print(e)
    except RecallReadError as e:
        console.print(e)