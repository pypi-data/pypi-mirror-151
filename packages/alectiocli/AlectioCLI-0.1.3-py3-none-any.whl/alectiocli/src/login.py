import typer
from pathlib import Path
from .utils import get_config_path
from .config import SSO_URL


def check_token_file():
    config_path = get_config_path()
    token_path = config_path / ".token"
    if not token_path.exists():
        return False
    else:
        return True


def store_token(token):
    config_path = get_config_path()
    token_path = config_path / ".token"
    token_path.write_text(token)
    typer.echo("Successfully stored token.")
    return True


def retrieve_token(refresh):
    token = check_token_file()
    if (not token) or (refresh):
        typer.echo("Logging in to Alectio, retrieving token")
        typer.launch(SSO_URL)
        token = typer.prompt("Token ID: ")
        status = store_token(token)
    else:
        status = True
        typer.echo("Token already exists!")
    return status
