import os
import json
import typer
import yaml
import requests
from pathlib import Path
from .config import APP_NAME, URL_TOKEN_VALIDATE, URL_GET_EXP_TOKEN


def get_config_path():
    app_dir = typer.get_app_dir(APP_NAME)

    config_path: Path = Path(app_dir)
    if not config_path.exists():
        config_path.mkdir(parents=True, exist_ok=True)
    return config_path


def get_token():
    config_path = get_config_path()
    token_path = config_path / ".token"
    if not token_path.exists():
        typer.echo(
            "Token doesn't exist! Please use `alectio-cli login` to get the token"
        )
        return False
    else:
        token = token_path.read_text()

        status = validate_token(token)

        if status["status"] == "success":
            return token
        else:
            token_path.unlink()
            typer.echo("Invalid token. Please use `alectio-cli login` to get the token")
            return False


def validate_token(token):
    headers = {"Authorization": str(token)}
    try:
        post_req_result = requests.get(URL_TOKEN_VALIDATE, headers=headers)

    except:
        return {"status": "failed"}
    if post_req_result.status_code == 200:
        return post_req_result.json()
    else:
        return {"status": "failed"}


def load_yaml_doc(yaml_file: Path):
    """
    Loads yaml file into a python dict and checks for validation
    Note : ` yaml.safe_load(stream)` is used to remove trailing zeroes from yaml file.
    """
    if yaml_file.is_file:
        if os.path.splitext(yaml_file)[1] == ".yaml":
            with open(yaml_file, "r") as stream:
                try:
                    return yaml.safe_load(stream)
                except yaml.YAMLError as exception:
                    raise exception
        else:
            message = typer.style(
                "Wrong file type: Please Enter a [dot]yaml file",
                fg=typer.colors.WHITE,
                bg=typer.colors.RED,
            )
            raise typer.Exit(message)
    else:
        message = typer.style("Not a file", fg=typer.colors.WHITE, bg=typer.colors.RED)
        raise typer.Exit(message)


def get_exp_token(token, exp_id):
    headers = {"Authorization": str(token), "Content-type": "application/json"}
    data = {"experiment_id": exp_id}
    try:
        post_req_result = requests.post(
            URL_GET_EXP_TOKEN, headers=headers, data=json.dumps(data)
        )
    except:
        return {"status": "failed"}
    if post_req_result.status_code == 200:
        return post_req_result.json()
    else:
        print(post_req_result.text)
        return {"status": "failed"}
