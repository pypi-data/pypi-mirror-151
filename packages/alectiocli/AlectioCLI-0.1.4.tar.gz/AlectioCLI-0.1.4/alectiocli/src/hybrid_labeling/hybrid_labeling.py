from random import choices
import requests
from pathlib import Path
import typer
from rich.console import Console
from datetime import datetime
import json
import inquirer
from alectiocli.src import console
from ..utils import get_token, load_yaml_doc
from .marketplace_recommendation import select_market_place_recommendation
from ..config import BACKEND_URL, AUTOLABEL_CLASS, INSTRUCTION_UPLOAD_URL
from ..utils import get_token
from .helper import upload_instruction_doc

rich_console = Console()


def ask_qualitycheck_questions():

    request_body = {}
    request_body["anomaly_criteria"] = {}
    console.message("Select quality checking for the labeling result: ")
    choices = [
        "Automatic quality checking",
        "Proceed without quality checking",
        "Pause without quality checking",
        "Relabel certain amount of data without quality checking and then proceed",
    ]
    quality_check_type_options = [
        inquirer.List(
            "quality_check_type",
            message="Select quality check method:",
            choices=choices,
        ),
    ]
    quality_check_type = inquirer.prompt(quality_check_type_options)[
        "quality_check_type"
    ]
    if quality_check_type == choices[3]:
        request_body["type"] = "relabel_amount_then_proceed"
        value = int(typer.prompt(f"What percentage of data to be relabeled (eg. 30)? "))
        request_body["amount_percentage"] = value
    if quality_check_type == choices[1]:
        request_body["type"] = "proceed_without_checking"
        request_body["amount_percentage"] = None
    if quality_check_type == choices[2]:
        request_body["type"] = "pause"
        request_body["amount_percentage"] = None

    if quality_check_type == choices[0]:
        request_body["type"] = "auto_quality_checking"
        request_body["amount_percentage"] = None
        request_body["action"] = {}

        console.message("Define anomaly criteria")
        console.info(
            "Alectio will check each labels and find anomalies based on the criteria you defined."
        )
        criteria_choice = ["Width", "Height", "Area", "Aspect Ratio"]
        criteria_choice_types = inquirer.prompt(
            [
                inquirer.Checkbox(
                    "criteria_types",
                    message="Select criteria types: ",
                    choices=criteria_choice,
                )
            ]
        )

        def ask_criteria_range(criteria_name, retry_count=0):
            retry_count = retry_count + 1

            if retry_count > 4:
                console.error("you exceed retry limit, try sometime letter !")

            lower_point = int(
                typer.prompt(f"Lowest value of {criteria_name}: (eg. 40): ")
            )
            if lower_point < 0:
                console.warning(
                    "Put the value again\nLower range value should be more than or equals to 0"
                )
                ask_criteria_range(criteria_name, retry_count)
            max_point = int(typer.prompt(f"Max value of {criteria_name}: (eg. 40): "))
            if max_point > 100 and max_point < lower_point:
                console.warning(
                    "Put the value again\nMax value should be less than 100 and greater than above Lower range value"
                )
                ask_criteria_range(criteria_name, retry_count)

            return [lower_point, max_point]

        if "Width" in criteria_choice_types["criteria_types"]:
            value_range = ask_criteria_range("Width")
            request_body["anomaly_criteria"]["width"] = value_range

        if "Height" in criteria_choice_types["criteria_types"]:
            value_range = ask_criteria_range("Height")
            request_body["anomaly_criteria"]["height"] = value_range
        if "Area" in criteria_choice_types["criteria_types"]:
            value_range = ask_criteria_range("Area")
            request_body["anomaly_criteria"]["area"] = value_range
        if "Aspect Ratio" in criteria_choice_types["criteria_types"]:
            value_range = ask_criteria_range("Aspect Ratio")
            request_body["anomaly_criteria"]["aspect_ratio"] = value_range

        # Define when to take action
        console.message("Define when to take action: ")
        whenaction_choice = [
            "When any anomaly is detected",
            "when X% labels are detected as anomalies",
        ]
        chosen_whenaction = inquirer.prompt(
            [
                inquirer.List(
                    "chosen_whenaction",
                    message="When to take any action: ",
                    choices=whenaction_choice,
                )
            ]
        )["chosen_whenaction"]
        if chosen_whenaction == whenaction_choice[1]:
            value = int(typer.prompt(f"Put the value of X: (eg. 40): "))
            request_body["action"]["when"] = value
        else:
            request_body["action"]["when"] = 0

        # Define what action to take
        console.message("Define what action to take: ")
        action_choices = ["Pause and warn me", "Relabel automatically"]
        chosen_action = inquirer.prompt(
            [
                inquirer.List(
                    "chosen_action",
                    message="What action do you want to take: ",
                    choices=action_choices,
                )
            ]
        )["chosen_action"]

        if chosen_action == action_choices[1]:
            value = int(
                typer.prompt(f"Define maximum number of relabeling processes (eg. 3): ")
            )
            request_body["action"]["what"] = "relable_automatic"
            request_body["action"]["number_of_relabel_times"] = value
        else:
            request_body["action"]["what"] = "pause"
            request_body["action"]["number_of_relabel_times"] = None
    return request_body


def create_hybrid_labeling_task(yaml_file: Path):
    # load yaml file
    config = load_yaml_doc(yaml_file)
    # make request body
    request_body = {}
    request_body["task_name"] = config["task_name"]
    project_id = config["project_id"]
    request_body["task_description"] = config["task_description"]
    task_type = config["task_type"]
    request_body["task_type"] = task_type
    annotation_type = config["annotation_type"]
    request_body["annotation_type"] = annotation_type
    classes = config["classes"]

    choices = [
        "All my data",
        "Randomly select X% of my data",
        "Specify range of indexes",
        "From an experiment",
    ]
    selection_type_options = [
        inquirer.List(
            "selection_type",
            message="Please specify the records you’d like to label",
            choices=choices,
        ),
    ]
    selection_type = inquirer.prompt(selection_type_options)["selection_type"]
    if selection_type == choices[0]:
        chosen_selection_type = "all"
        selection_value = 0
    if selection_type == choices[1]:
        chosen_selection_type = "random"
        selection_value = int(
            typer.prompt(
                "What parcentage(0-100) of data, you want to randomly select? eg. 40"
            )
        )
    if selection_type == choices[2]:
        chosen_selection_type = "range"
        index_low = int(typer.prompt("Starting index(eg. 100): "))
        index_high = int(typer.prompt("Ending index(eg. 600): "))
        selection_value = [index_low, index_high]

    if selection_type == choices[3]:
        chosen_selection_type = "experiment"
        console.error("This is not suppported yet")
        typer.Exit()
        selection_value = 0

    # labelling methodology
    labeling_methodology = config["labeling_methodology"]["type"]
    if labeling_methodology == "market_place":
        multi_judgement_count = config["labeling_methodology"]["multi_judgement_count"]
        instruction_file = config["labeling_methodology"]["instruction_file"]
        upload_instruction_doc(project_id, Path(instruction_file))
        request_body["instruction_file"] = "s3_key"

        # prompt user with options
        console.message("How do you want to select Labeling Partner?")
        console.message("1. Alectio Recommendation")
        console.message("2. Own Choice")
        recommendation_choice = typer.prompt("select (1/2): ", default="1")
        marketplace_chosen = select_market_place_recommendation(
            annotation_type=annotation_type,
            project_id=project_id,
            task_type=task_type,
            choice=recommendation_choice,
        )
    else:
        multi_judgement_count = 1
        instruction_file = ""
        marketplace_chosen = None
        request_body["instruction_file"] = ""

    request_body["methods"] = []
    request_body["methods"].append(
        {
            "labeling_method": labeling_methodology,
            "classes": classes,
            "selection_type": chosen_selection_type,
            "value": selection_value,
            "number_of_annotators_per_record": multi_judgement_count,
            "partners": marketplace_chosen,
        }
    )
    # auto labeling
    token = get_token()

    def find_autolabel_support(task_type, class_name):
        headers = {"Authorization": str(token), "content-type": "application/json"}
        api_url = f"{AUTOLABEL_CLASS}/{task_type}/classes/{class_name}"

        post_req_result = requests.post(api_url, headers=headers)
        if post_req_result.status_code == 200:
            response = post_req_result.json()
            if "class_name" in response["data"]:
                return response["data"]["class_name"]
        return False

    with rich_console.status(
        "[bold green]Finding AutoAL support of classes..."
    ) as status:
        auto_labeling_supported_class = []
        for c in classes:
            if find_autolabel_support(task_type=task_type, class_name=c):
                auto_labeling_supported_class.append(c)

    request_body["methods"].append(
        {
            "labeling_method": "auto_labeling",
            "classes": auto_labeling_supported_class,
            "selection_type": chosen_selection_type,
            "value": selection_value,
        }
    )
    request_body["instruction_file"] = instruction_file

    # quality check parameters
    quality_checking = ask_qualitycheck_questions()
    request_body["quality_checking"] = quality_checking

    with rich_console.status(
        "[bold green]Alectio is creating a Hybrid labeling task for you ..."
    ) as status:
        done = False
        headers = {
            "Authorization": str(token),
            "content-type": "application/json",
        }
        payload = request_body
        while not done:
            BACKEND_URL = "https://devbackend.alectio.com"
            post_req_result = requests.post(
                f"{BACKEND_URL}/project/{project_id}/task/create",
                headers=headers,
                data=json.dumps(payload),
            )
            if post_req_result.status_code == 200:
                done = True
                console.success(
                    "Hybrid labeling task is created, check Alectio Portal !"
                )
