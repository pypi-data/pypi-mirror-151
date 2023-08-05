import requests
from ..utils import get_token
from ..config import PROJECT_LIST_URL
from alectiocli.src import console
from rich.console import Console
from rich.table import Table

rich_console = Console()


def show_table(response):
    table = Table(title="Your all projects")

    table.add_column("Proj Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Proj ID", style="cyan", no_wrap=False)
    table.add_column("Dataset Source", style="cyan", no_wrap=False)
    table.add_column("Task Type", style="cyan", no_wrap=False)
    table.add_column("Data Format", style="cyan", no_wrap=False)
    table.add_column("Train Length", style="cyan", no_wrap=False)

    for row in response["data"]:
        table.add_row(
            str(row["name"]),
            str(row["SK"].replace("PROJ#", "")),
            str(row["dataset_source"]),
            str(row["labeling_instructions"]["task_type"].replace("_", " ").upper()),
            str(row["data_info"]["format"]),
            str(row["train"]["length"]),
        )

    rich_console.print(table)


def get_project_list():
    with rich_console.status(
        "[bold green]Collecting the list of all your projects..."
    ) as status:
        token = get_token()
        headers = {"Authorization": str(token)}
        try:
            post_req_result = requests.get(PROJECT_LIST_URL, headers=headers)
        except:
            console.error("Something went wrong !!")
        if post_req_result.status_code == 200:
            show_table(post_req_result.json())
            # return post_req_result.json()

        else:
            console.error("Something went wrong !!")
