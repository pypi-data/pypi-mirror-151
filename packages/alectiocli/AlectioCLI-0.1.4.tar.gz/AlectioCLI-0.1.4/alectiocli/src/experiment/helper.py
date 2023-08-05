from random import choices
import typer
from ..utils import get_exp_token

from pathlib import Path
import yaml
import os
from ..utils import load_yaml_doc
import requests
from ..config import URL_CREATE_EXPERIMENT
import json
import inquirer
from datetime import datetime


def get_auto_al_info(yaml_dict):
    """_summary_

    Args:
        yaml_dict (dict): Takes a dictinoary as dict

    Returns:
        _type_: _description_
    """

    max_records = yaml_dict["n_records"]
    limit_value = typer.prompt(
        f"Define a custom stopping criteria for your experiment?\nEnter integers value from 1 to {max_records} records present"
    )
    typer.echo("\n")

    if int(limit_value) > int(max_records):
        typer.echo(
            f"Limit value is greater than maximum records i.e. {max_records}\nPlease re-enter the limit value"
        )
        get_auto_al_info(yaml_dict)
    else:
        confirm = typer.confirm("Confirm ")
        info_dict = {}
        if not confirm:

            typer.echo("Taking to the previous step")
            get_auto_al_info(yaml_dict)

        info_dict = {
            "auto_al_info": {
                "type": "limit",
                "threshold": {
                    "limit_type": "records",
                    "limit_value": limit_value,
                    "limit_unit": None,
                },
            }
        }
        yaml_dict["auto_al_info"] = info_dict["auto_al_info"]

    return yaml_dict


def get_ml_driven_info(yaml_dict):
    max_records = yaml_dict["n_records"]
    n_loops = typer.prompt(
        f"How many loops you would like to run for the experiment ?/n"
    )
    limit = typer.prompt(f"Define limit per loop")
    total_selected_records = int(n_loops) * int(limit)
    if int(total_selected_records) > int(max_records):
        typer.echo(
            " you will run out of record before the end, Choose a lesser value of limit per loop"
        )
        get_ml_driven_info(yaml_dict)

    else:
        confirm = typer.confirm("Confirm ")
        info_dict = {}
        if not confirm:

            typer.echo("Taking to the previous step")
            get_ml_driven_info(yaml_dict)

        yaml_dict["n_records"] = total_selected_records
        yaml_dict["n_loops"] = n_loops

    return yaml_dict


def create_experiment_api_request(token, data):
    headers = {"Authorization": str(token), "Content-type": "application/json"}
    post_req_result = requests.post(
        URL_CREATE_EXPERIMENT, headers=headers, data=json.dumps(data)
    )
    return post_req_result.json()


def final_auto_al_ml_driven_ruled_based_call(final_dict, token):

    date = datetime.now()
    date = int(date.strftime("%Y%m%d%H%M%S"))
    final_dict["date"] = date
    result = create_experiment_api_request(token, final_dict)
    status = result["message"]
    project_id = result["data"]
    message = typer.style(
        f"status: {status}\Experiment ID: {project_id}", fg=typer.colors.GREEN
    )
    typer.echo(message)
    return True
