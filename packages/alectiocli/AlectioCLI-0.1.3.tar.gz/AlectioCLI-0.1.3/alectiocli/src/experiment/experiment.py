import typer
from pathlib import Path
import os
import requests
import json
import yaml
from ..config import URL_CREATE_EXPERIMENT
from ..utils import load_yaml_doc
from ..utils import get_token
from ..utils import get_exp_token
import inquirer

from .helper import (
    final_auto_al_ml_driven_ruled_based_call,
    get_auto_al_info,
    get_ml_driven_info,
    create_experiment_api_request,
)
from datetime import datetime


def get_experiment_type_and_dict_manuevers(yaml_file: Path):
    """Creates 4 types of experiment.
       1. Auto curation
       2. ML Driven
       3. Rule Based
       4. Manual Curation


    Args:
        yaml_dict (dict): _description_

    Raises:
        typer.Exit: _description_

    Returns:
        _type_: _description_
    """

    token = get_token()
    if not token:
        raise typer.Exit()
    yaml_dict = load_yaml_doc(yaml_file)

    questions = [
        inquirer.List(
            "type",
            message="What is the type of curation",
            choices=["auto_al", "proprietary", "rule_based", "manual_curation"],
        )
    ]
    answers = inquirer.prompt(questions)
    type = answers.get("type")
    if type == "auto_al":
        is_alectio_qs = False
        yaml_dict["type"] = type
        yaml_dict["limits"] = False
        yaml_dict["is_alectio_qs"] = is_alectio_qs
        yaml_dict["n_loops"] = 10
        yaml_dict["epochs"] = 0
        yaml_dict["batch_size"] = 0
        final_dict = get_auto_al_info(yaml_dict)
        return_value = final_auto_al_ml_driven_ruled_based_call(final_dict, token)

    elif type == "proprietary":
        is_alectio_qs = True
        yaml_dict["type"] = type
        yaml_dict["limits"] = False
        yaml_dict["is_alectio_qs"] = is_alectio_qs
        yaml_dict["epochs"] = 0
        yaml_dict["batch_size"] = 0

        final_dict = get_ml_driven_info(yaml_dict)
        return_value = final_auto_al_ml_driven_ruled_based_call(final_dict, token)

    elif type == "rule_based":
        type = "design_own"
        is_alectio_qs = True
        yaml_dict["type"] = type
        yaml_dict["limits"] = False
        yaml_dict["is_alectio_qs"] = is_alectio_qs
        yaml_dict["epochs"] = 0
        yaml_dict["batch_size"] = 0

        final_dict = get_ml_driven_info(yaml_dict)
        return_value = final_auto_al_ml_driven_ruled_based_call(final_dict, token)

    elif type == "manual_curation":
        n_loops = typer.prompt(
            f"How many loops you would like to run for the experiment ?/n"
        )
        yaml_dict["n_loops"] = n_loops
        yaml_dict["type"] = type
        for qs in yaml_dict["qs"]:
            check_qs = yaml_dict["qs"][qs]["enable"]
            if check_qs:
                temp_data_loaded = yaml_dict.copy()
                temp_data_loaded["qs"] = [qs]
                temp_data_loaded["name"] = f'{temp_data_loaded["name"]}_{qs}'
                date = datetime.now()
                date = int(date.strftime("%Y%m%d%H%M%S"))
                temp_data_loaded["date"] = date
                result = create_experiment_api_request(token, temp_data_loaded)
                status = result["message"]
                experiment_id = result["data"]
                message = typer.style(
                    f"QS: {qs}\nstatus: {status}\nExperiment ID: {experiment_id}",
                    fg=typer.colors.GREEN,
                )
                typer.echo(message)

    return True


def run_experiment(python_file: Path, experiment_file: Path):
    """Run Experiment

    Args:
        python_file (python_file): _description_
        experiment_file (experiment_file): _description_

    Raises:
        typer.Exit: _description_
    """
    token = get_token()
    if not token:
        raise typer.Exit()
    data_loaded = load_yaml_doc(experiment_file)
    if data_loaded["type"] == "manual_curation":
        pass
    elif data_loaded["type"] == "auto_al":
        exp_token = get_exp_token(token, data_loaded["experiment_id"])["token"]
        os.system(f"python {python_file} --token {exp_token}")
        pass
