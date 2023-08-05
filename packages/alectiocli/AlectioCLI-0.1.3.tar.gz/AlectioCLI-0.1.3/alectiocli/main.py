import typer
from .src.login import retrieve_token
from .src.project.project import create_project_on_prem
from .src.project.project_list import get_project_list
from .src.project.delete_project import delete_project
from .src.experiment.experiment import (
    get_experiment_type_and_dict_manuevers,
    run_experiment,
)
import pyfiglet
from termcolor import colored
from .src.hybrid_labeling.hybrid_labeling import create_hybrid_labeling_task
from pathlib import Path
# result = pyfiglet.figlet_format("ALECTIO-CLI", font = "slant" )
# print(colored(result,'cyan',attrs=['bold']))

app = typer.Typer()

project_app = typer.Typer()
app.add_typer(project_app, name="project")
experiment_app = typer.Typer()
app.add_typer(experiment_app, name="experiment")






@app.callback()
def callback():
    """
    AlectioCLI
    """


@app.command()
def login(refresh: bool = False):
    """
    Login to Alectio
    """
    status = retrieve_token(refresh)
    if not status:
        typer.echo("Error storing token")


@project_app.command("create")
def project_creation(yaml_file: Path, label_file: Path):

    """
    Creating Project
    """

    message = typer.style(
        "Creating Project ...",
        fg=typer.colors.BLUE,
    )
    typer.echo(message)
    status = create_project_on_prem(yaml_file, label_file)


@project_app.command("hybrid-labeling")
def create_hybrid_labeling(yaml_file: Path):
    """
    Creating Hybrid Labeling Task
    """

    message = typer.style(
        "Creating Hybrid Labeling Task ...",
        fg=typer.colors.MAGENTA,
    )
    typer.echo(message)
    status = create_hybrid_labeling_task(yaml_file)


@experiment_app.command("create")
def experiment_creation(yaml_file: Path):

    """
    Creating Experiment
    """

    message = typer.style(
        "Creating Experiment ...",
        fg=typer.colors.MAGENTA,
    )
    typer.echo(message)
    status = get_experiment_type_and_dict_manuevers(yaml_file)


@experiment_app.command("run")
def experiment_run(python_file: Path, experiment_file: Path):

    """
    Run the Experiment
    """

    message = typer.style(
        "Running the Experiment ...",
        fg=typer.colors.MAGENTA,
    )
    typer.echo(message)
    status = run_experiment(python_file, experiment_file)


@project_app.command("list")
def show_project_list():
    """
    show project list(all private project)
    """
    get_project_list()


@project_app.command("delete")
def delete_proj(proj_id: str):
    """
    Delete Project
    """
    delete_project(proj_id=proj_id)
