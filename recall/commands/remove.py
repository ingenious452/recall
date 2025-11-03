import typer
from rich.console import Console


from recall.core import get_recaller
from recall import ERRORS

app = typer.Typer()


console = Console()


@app.command("remove")
def remove_recall(recall_name: str) -> None:
    recaller = get_recaller()
    project, error = recaller.delete(recall_name)
    if error:
        console.print(f"[red]Error:[/red] Project '{project['project_name']}', {ERRORS[error]}. Nothing deleted.")
        # print(f'Deleting project name: "{project['project_name']}", path: "{project['project_path']}" failed with {ERRORS[error]}')
    else:
        console.print(f"[red]Record deleted:[/red] {project['project_name']}")

        # print(f'Deleted project name: "{project['project_name']}", path: "{project['project_path']}" successfully!')