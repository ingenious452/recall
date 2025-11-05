import typer

from rich.console import Console
from rich.padding import Padding
from rich.table import Table

from recall.errors import RecallInitError, RecallReadError
from recall.core import get_orchestrator


app = typer.Typer()


console = Console()


@app.command("show")
def show_recall() -> None:
    try:
        orchest = get_orchestrator()

        entries = orchest.show()

        if len(entries) == 0:
            console.print("[red]no entries found[/red], use 'recall add' to add an entry.")
        else:
            project_table = Table(title="[blue]Recall Index[/blue]", show_header=True, header_style="bold magenta")
            project_table.add_column("ID", style="dim", width=3)
            project_table.add_column("Name", style="green")
            project_table.add_column("Path", style="yellow", width=50)
            # project_table.add_column("Status", justify="center")
            for index, project in enumerate(entries.items(), start=1):
                project_table.add_row(str(index), project[0], project[1])
            console.print(project_table)

    except RecallInitError as e:
        console.print(
            Padding(f"[yellow]warning:[/yellow] {e}, please run 'recall init' or use '-f' switch to force init.",
                    (1, 0, 0, 0)))
    except RecallReadError as e:
        console.print(
            Padding(f"[red]error:[/red] unable to retrieve entries, {e}", (1, 0, 0, 0)))
    except Exception as e:
        console.print(Padding(f"[red]unexpected error:[/red] {e}", (1, 0, 0, 0)))
