import collections
import yaml
import os
import ruamel.yaml


def create_sample_yaml_for_experiment(folder_path, project_id):
    """Create sample yaml for experiment

    Args:
        project_id (string): project id
    values:
    name,n_records,seeds,labeling_type,is_sdk_setup,
    is_curr_fully_labeled,assoc_labeling_task_id
    """

    yaml_str = """# sample code 
# QS list is empty for auto_al,ml_driven curation
        project_id: 
        name: 'test_experiment'
        n_records: 100
        limits: False
        qs: [] 
        seed: 120
        labeling_type: pre_labeled
        is_sdk_setup: False
        is_curr_fully_labeled: False
        assoc_labeling_task_id:
"""

    yaml_file = ruamel.yaml.YAML()
    code = yaml_file.load(yaml_str)
    code["project_id"] = str(project_id)
    # current_working_directory=os.getcwd()

    # print(current_working_directory)
    with open(os.path.join(folder_path, "experiment.yaml"), "w+") as outfile:
        ruamel.yaml.dump(code, outfile, Dumper=ruamel.yaml.RoundTripDumper)
    return "experiment file created"


def manual_curation_experiment(folder_path, project_id):
    """Create sample yaml for experiment of manual curation

    Args:
        project_id (string): project id
    """

    yaml_str = """# sample code
    project_id: 
    name: 'New Experiment Manual curation test'
    n_records: 100
    limits: False

    qs:
        confidence:
            enable: True
            range:
                start: 0.5
                stop: 1
        entropy:
            enable: True
            range:
                start: 0.5
                stop: 1
        margin:
            enable: True
            range:
                start: 0.5
                stop: 1

    seed: 120
    labeling_type: pre_labeled
    is_sdk_setup: False
    is_curr_fully_labeled: False
    assoc_labeling_task_id:
"""

    yaml_file = ruamel.yaml.YAML()
    code = yaml_file.load(yaml_str)
    code["project_id"] = str(project_id)
    # current_working_directory=os.getcwd()

    # print(current_working_directory)
    with open(
        os.path.join(folder_path, "sample_experiment_manual_curation.yaml"), "w+"
    ) as outfile:
        ruamel.yaml.dump(code, outfile, Dumper=ruamel.yaml.RoundTripDumper)
    return " manual curation experiment file created"


def create_hybrid_labeling_yaml_file(folder_path, project_id):

    """Create sample yaml for hybrid labeling

    Args:
        project_id (string): project id
    """
    yaml_str = """# sample code
    task_name: "Hybrid Labeling for Object Detection"
    project_id: 
    task_description: "This is a YOLO V5 model for brand logo detection"
    task_type: "2d_object_detection"
    annotation_type: "bounding_boxes"
    classes: ["dog", "cat", "horse", "rat", "bird", "dog"]

    labeling_methodology:
        type: market_place
        multi_judgement_count: 5
        instruction_file: "converted_compressed.pdf"

    quality_check:
        type: auto_quality_checking
        anomaly_criteria:
            width: [14, 40]
            height: [14, 40]
            area: [14, 40]
            aspect_ratio: [14, 40]
        action:
            when: 20
            what: relabel_automatic
            number_of_relabel_times: 4
"""

    yaml_file = ruamel.yaml.YAML()
    code = yaml_file.load(yaml_str)
    code["project_id"] = str(project_id)
    with open(
        os.path.join(folder_path, "sample_hybrid_labeling.yaml"), "w+"
    ) as outfile:
        ruamel.yaml.dump(code, outfile, Dumper=ruamel.yaml.RoundTripDumper)
    return "hybrid labeling experiment file created"
