import json
import requests
from ..utils import get_token
from ..config import DELETE_PROJECT_URL
from alectiocli.src import console
from rich.console import Console

rich_console = Console()


def delete_project(proj_id: str):

    try:
        with rich_console.status("[bold green]Deleting your project...") as status:
            payload = {"project_id": proj_id}
            token = get_token()
            headers = {"Authorization": str(token)}
            post_req_result = requests.get(
                DELETE_PROJECT_URL,
                headers=headers,
                data=json.dumps(payload),
            )

    except:
        console.error("Something wrong happend !")
        console.info(
            "Make sure, the proj_id is correct.\nuse `alectio-cli project list` to get the correct proj_id"
        )

    if post_req_result.status_code == 200:
        if post_req_result.json()["status"] != "success":
            console.error("Something wrong happend !")
            console.info(
                "Make sure, the proj_id is correct.\nuse `alectio-cli project list` to get the correct proj_id"
            )

        console.success(f"Project with ID: {proj_id} deleted successfully")
    else:
        console.error("Something wrong happend !")
        console.info(
            "Make sure, the proj_id is correct.\nuse `alectio-cli project list` to get the correct proj_id"
        )
