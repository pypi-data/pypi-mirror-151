import typer
from pathlib import Path
import os
import requests
from ..config import URL_CREATE_PROJECT
from ..utils import get_token, load_yaml_doc
from .helper import (
    create_sample_yaml_for_experiment,
    manual_curation_experiment,
    create_hybrid_labeling_yaml_file,
)


def create_project_api_request(token, data, files):

    headers = {"Authorization": str(token)}
    post_req_result = requests.post(
        URL_CREATE_PROJECT, headers=headers, files=files, data=data
    )
    return post_req_result.json()


def create_project_on_prem(yaml_file: Path, label_map: Path):
    """
    Creates project for On prem

    :param yaml_file: Takes input a sample yaml file
    :param yaml_file: Takes input a json file containing classes/ label_map

    """
    token = get_token()

    if not token:
        raise typer.Exit()
    data_loaded = load_yaml_doc(yaml_file)
    if label_map.is_file:
        if os.path.splitext(label_map)[1] == ".json":
            files = {"class_labels": open(label_map, "rb")}
        else:
            message = typer.style(
                "Wrong file type: Please Enter a [dot]json file",
                fg=typer.colors.WHITE,
                bg=typer.colors.RED,
            )
            return typer.echo(message)
            raise typer.Exit()
    else:
        message = typer.style("Not a file", fg=typer.colors.WHITE, bg=typer.colors.RED)
        return typer.echo(message)

    result = create_project_api_request(token, data_loaded, files)

    status = result["message"]
    project_id = result["project_id"]
    if status == "project successfully created":
        folder_name = "Alectio_cli_sample_yamls"
        current_working_directory = os.getcwd()
        folder_path = os.path.join(current_working_directory, folder_name)
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        create_sample_yaml_for_experiment(folder_path, project_id)
        manual_curation_experiment(folder_path, project_id)
        create_hybrid_labeling_yaml_file(folder_path, project_id)

    messge = typer.style(
        f"status: {status}\nProject ID: {project_id}", fg=typer.colors.GREEN
    )

    typer.echo(messge)
    typer.secho(f"Sample yaml files are located at {folder_path}", fg=typer.colors.BLUE)
    return True
