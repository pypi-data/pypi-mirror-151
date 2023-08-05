from rich.console import Console
from rich.table import Table
import typer
import requests
from alectiocli.src import console
from ..config import MARKETPLACE_RECOMMENDATION_URL
from ..utils import get_token
import json
import inquirer


# rich console
rich_console = Console()
market_place_list = [
    [
        {
            "partner_keyname": "HITL",
            "calc_price_per_row": 0.0,
            "calc_accuracy_per_row": 95.0,
            "calc_time_per_row": 36.0,
            "n_annotators": 200,
        },
        1548.0,
    ],
    [
        {
            "partner_keyname": "INFOSCRIBE",
            "calc_price_per_row": 0.02,
            "calc_accuracy_per_row": 95.0,
            "calc_time_per_row": 36.0,
            "n_annotators": 1000,
        },
        1459.0,
    ],
    [
        {
            "partner_keyname": "DAIVERGENT",
            "calc_price_per_row": 0.2,
            "calc_accuracy_per_row": 98.0,
            "calc_time_per_row": 10.0,
            "n_annotators": 1,
        },
        773.0,
    ],
    [
        {
            "partner_keyname": "RBC",
            "calc_price_per_row": 0.05,
            "calc_accuracy_per_row": 90.0,
            "calc_time_per_row": 36.0,
            "n_annotators": 200,
        },
        670.0,
    ],
    [
        {
            "partner_keyname": "STEPWISE",
            "calc_price_per_row": None,
            "calc_accuracy_per_row": 95.0,
            "calc_time_per_row": 36.0,
            "n_annotators": 1,
        },
        550.0,
    ],
]


def show_table(market_place_data):
    table = Table(title="Avaailable MarketPlace Partners")

    table.add_column("Partner Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Calc Price/Row", style="magenta")
    table.add_column("Calc Accuracy/Row", style="green")
    table.add_column("Calc time/Row", style="green")
    table.add_column("Total Available Annotator", justify="right", style="green")

    for row in market_place_data:
        table.add_row(
            str(row[0]["partner_keyname"]),
            str(row[0]["calc_price_per_row"]),
            str(row[0]["calc_accuracy_per_row"]),
            str(row[0]["calc_time_per_row"]),
            str(row[0]["n_annotators"]),
        )
    console = Console()
    console.print(table)


def call_recommendation_API(annotation_type, project_id, task_type, retry_count=0):
    retry_count = retry_count + 1
    if retry_count > 3:
        raise typer.Exit()
    # take user CLI input
    price_point = int(typer.prompt("Total Point for Price?"))
    time_point = int(typer.prompt("Total Point for Time?"))
    accuracy_point = int(typer.prompt("Total Point for Accuracy?"))

    if price_point + time_point + accuracy_point > 12:
        console.warning("You have exceeded the maximum score")
        call_recommendation_API(
            annotation_type, project_id, task_type, retry_count=retry_count
        )
    elif price_point + time_point + accuracy_point < 12:
        console.warning("Total sum of points is less than 12")
        call_recommendation_API(
            annotation_type, project_id, task_type, retry_count=retry_count
        )

    # recommendation API call
    payload = {
        "annotation_type": annotation_type,
        "n_records": 500,  # hard coded for now
        "project_id": project_id,
        "task_type": task_type,
        "user_accuracy_points": accuracy_point,
        "user_price_points": price_point,
        "user_time_points": time_point,
    }

    token = get_token()
    headers = {"Authorization": str(token), "content-type": "application/json"}
    done = False
    with rich_console.status("[bold green]Working on tasks...") as status:
        while not done:
            post_req_result = requests.post(
                MARKETPLACE_RECOMMENDATION_URL,
                headers=headers,
                data=json.dumps(payload),
            )
            if post_req_result.status_code == 200:
                done = True
    return post_req_result.json()


def select_market_place_recommendation(
    annotation_type, project_id, task_type, choice: str = "1"
):
    if choice == "1":
        recommended_market_place = call_recommendation_API(
            annotation_type, project_id, task_type
        )
        recommended_market_place_list = recommended_market_place["data"]
        show_table(recommended_market_place_list)

        # select multiple market place
        selected_market_place = inquirer.prompt(
            [
                inquirer.Checkbox(
                    "market_place",
                    message="Select market place",
                    choices=[
                        x[0]["partner_keyname"] for x in recommended_market_place_list
                    ],
                )
            ]
        )
    elif choice == "2":
        show_table(market_place_list)
        # select multiple market place
        selected_market_place = inquirer.prompt(
            [
                inquirer.Checkbox(
                    "market_place",
                    message="Select market place",
                    choices=[x[0]["partner_keyname"] for x in market_place_list],
                )
            ]
        )
    return selected_market_place["market_place"]
