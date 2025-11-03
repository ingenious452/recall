import typer

from typing import Annotated, Optional
from rich.console import Console

from recall.commands import get, add, update, view, remove
from recall import __version__, __app_name__



HELP_DESCRIPTION = "A powerful, ultra-fast command-line tool for navigating to your most important project directories instantly."


app = typer.Typer(no_args_is_help=True, help=HELP_DESCRIPTION)



console = Console()



def version_callback(value: bool):
    if value:
        console.print(f"{__app_name__} v.[green]{__version__}[/green]")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, 
         version: Annotated[Optional[bool], 
                            typer.Option("--version", "-v", 
                                         callback=version_callback, 
                                         is_eager=True, help=f"show the current {__app_name__} version")] = None,
):
    pass



app.add_typer(get.app, )
app.add_typer(view.app)
app.add_typer(add.app)
app.add_typer(remove.app)
app.add_typer(update.app)


if __name__ == "__main__":
    app()