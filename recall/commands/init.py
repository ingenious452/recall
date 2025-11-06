from pathlib import Path
from typing import Optional, Annotated

import typer
from rich.console import Console

from recall.config import config
from recall.core import init_service


app = typer.Typer()


console = Console()


@app.command("init")
def init_recall(db_file: Annotated[Optional[Path], 
                                   typer.Option("--db-file", 
                                                help="Database file path initialization.")] = None,
                 logs_dir: Annotated[Optional[Path],
                                    typer.Option("--logs-dir",
                                                 help="Logs directory path.")] = None, 
                 force: Annotated[bool, 
                                  typer.Option("--force", "-f", 
                                               help="Force initialization app.")] = False) -> None:

    if not config.INITIALIZED or force:
        init_service(db_file, logs_dir)
        console.print("[green]successfully[/green] initialized")
    else:
        console.print("[dim]already initialized. use -f switch to force initialize[/dim]")
