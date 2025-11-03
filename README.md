# Recall

Have you ever have problem managing large number of project when you are not sure 
in which directory has the project you were working on 

> recall help you keep track of all your project directory from command line


## How to use

1. Open directory

```cmd
recall -o <project_name>
```

2. Save directory

```cmd
recall save <project_name> --path <project_path>
```
```--path``` defaults to the **current working directory**

3. Delete directory

```cmd
recall delete <project_name>
```

4. Update directory
```cmd
recall update <project_name> --path <updated_project_path>
```
```--path``` defaults to the **current working directory**

5. List directories
```cmd
recall list
```

> upgrading the application to

some important changes I need 
1. ability to open and close task by index
2. show the recently used task
3. sort tasks by order

from rich.console import Console
from rich.table import Table

console = Console()

todo_table = Table(title="Weekly Tasks", show_header=True, header_style="bold magenta")
todo_table.add_column("ID", style="dim", width=4)
todo_table.add_column("Task Description", style="white")
todo_table.add_column("Status", justify="center")

# Add rows (your list items)
todo_table.add_row("1", "Review image selection logic", "[green]Done[/green]")
todo_table.add_row("2", "Implement menu bar functionality", "[green]Done[/green]")
todo_table.add_row("3", "Refactor Tkinter grid layout", "[yellow]Pending[/yellow]")
todo_table.add_row("4", "Write image processing documentation", "[red]Urgent[/red] ❗")

console.print(todo_table)


| **Error Case** | Error Message | ```text
$ recall get unknown-project
[bold cyan]Fetching project:[/bold cyan] unknown-project...
[red]Error:[/red] Project 'unknown-project' not found in index.
``` |

---

### 2. Management Command: `recall add`

**Goal:** Register a new project location, using both manual path and the `--current` flag.


Command,argparse Action,Description
recall <project_name>,Positional Argument,Primary Function: Fetches the directory for the <project_name> and immediately opens it in the system file explorer.
recall --help,Global Flag,Displays the overall application help text.


| Command | Output Type | Sample Output |
| :--- | :--- | :--- |
| `recall add new-app -p /mnt/storage/new-app` | Success | ```text
$ recall add new-app -p /mnt/storage/new-app
[bold yellow]Registering Project:[/bold yellow] [green]new-app[/green]
Path: /mnt/storage/new-app
[green]Success:[/green] Project 'new-app' added to index.
``` |
| `recall add recall-cli --current` | Success (Auto-path) | ```text
$ recall add recall-cli --current
[bold yellow]Registering Project:[/bold yellow] [green]recall-cli[/green]
Path: /D/python/recall
[green]Success:[/green] Project 'recall-cli' added to index.
``` |

---

### 3. Management Command: `recall remove <name>`

**Goal:** Delete a record, using a confirmation prompt for safety (since we set `prompt=...` on the Typer option).

| Command | Output Type | Sample Output |
| :--- | :--- | :--- |
| `recall remove legacy-script` | Confirmation | ```text
$ recall remove legacy-script
Are you sure you want to delete this project record? [y/N]: y
[red]Record deleted:[/red] legacy-script
``` |
| `recall remove legacy-script` | Cancellation | ```text
$ recall remove legacy-script
Are you sure you want to delete this project record? [y/N]: N
[yellow]Deletion cancelled.[/yellow]
``` |
| **Error Case** | Error Message | ```text
$ recall remove not-in-db
[red]Error:[/red] Project 'not-in-db' not found. Nothing deleted.
``` |

---

### 4. Management Command: `recall list`

**Goal:** Display all indexed projects using a clean Rich Table.

| Command | Output Type | Sample Output |
| :--- | :--- | :--- |
| `recall list` | Rich Table | ```text
$ recall list

[bold blue]             Recall Project Index             [/bold blue]
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [bold magenta]Project Name[/bold magenta]         ┃ [bold magenta]Location (Path)[/bold magenta]           ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ [cyan]recall-ingenious[/cyan]    │ /D/python/recall             │
│ [cyan]dashboard-api[/cyan]       │ /home/user/backend/api       │
│ [cyan]my-new-app[/cyan]          │ /mnt/storage/new-app         │
└─────────────────────┴──────────────────────────────┘
``` |
| `recall list --name-only` | Plain Text | ```text
$ recall list --name-only
recall-ingenious
dashboard-api
my-new-app
``` |
| `recall list dash` | Filtered Table | ```text```
$ recall list dash

[bold blue]             Recall Project Index             [/bold blue]
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ [bold magenta]Project Name[/bold magenta]         ┃ [bold magenta]Location (Path)[/bold magenta]           ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ [cyan]dashboard-api[/cyan]       │ /home/user/backend/api       │
└─────────────────────┴──────────────────────────────┘
``` |

Command,argparse Argument,Description
recall list,(No Args),"Displays all project names and their associated paths in a clean, readable table (great use case for Rich Tables!)."
recall list --name-only,Flag,"Displays only the project names, one per line (useful for piping into other shell commands)."
recall list <pattern>,Positional Argument,Displays project records whose names contain a specific search <pattern>.
---

This structured output makes it clear to the user what the command did, what the result was, and provides professional-looking tables and messaging.




#TODO: implement a caching


# important

1. if you only have a single registered command the program will directly execute it when you run the program

2. if no command are registered then it will give error runtimeerror

3. if you have multiple registere command it will show missing command when run without command

4. I want to see the help with it




# what i learnt

when we type any command in the terminal it is parsed by the program

all the argument and it's options are parsed

when we use `is_eager` true it parses the option it sees first and then execute it first before parsing other commands
