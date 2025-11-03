from pathlib import Path
from typing import Optional, Annotated

import typer
from rich.console import Console

from recall.config import config
from recall.core import database


app = typer.Typer()


console = Console()


@app.command("init")
def init_recall(db_file: Annotated[Optional[Path], 
                                   typer.Option("--db-file", 
                                                help="Database file path initialization.")] = None,
                 log_dir: Annotated[Optional[Path], 
                                    typer.Option("--log-dir", 
                                                 help="Logs directory path.")] = None, 
                 force: Annotated[bool, 
                                  typer.Option("--force", "-f", 
                                               help="Force initialization app.")] = False) -> None:

    if not config.INITIALIZED or force:
        config.init_config(db_file, log_dir)
        database.init_database(Path(config.DATABASE_FILE))
        console.print("[green]Successfully[/green] intialized recall.")
    else:
        console.print("[dim]Already initialized.[/dim]")
