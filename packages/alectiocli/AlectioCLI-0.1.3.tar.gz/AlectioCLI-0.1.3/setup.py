# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['alectiocli',
 'alectiocli.src',
 'alectiocli.src.experiment',
 'alectiocli.src.hybrid_labeling',
 'alectiocli.src.project']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'alectio-sdk>=0.6.21,<0.7.0',
 'inquirer>=2.9.2,<3.0.0',
 'pyfiglet>=0.8.post1,<0.9',
 'requests>=2.27.1,<3.0.0',
 'rich>=12.2.0,<13.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'termcolor>=1.1.0,<2.0.0',
 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['alectio-cli = alectiocli.main:app']}

setup_kwargs = {
    'name': 'alectiocli',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Alectio-CLI :rocket: :rocket:\n\n\n`Alectio-cli` is [Alectio\'s](https://portal.alectio.com/)\'s official command-line interface (CLI)wrapper. It allows you to create  projects, experiments and do hybrid labeling tasks. \n\n## Configuration\n\n### Setup\n\n> These setup instructions are for CLI usage only.\n\nWe recommend installing `alectiocli` in your virtualenv rather than doing a global installation so you don\'t run into unexpected behavior with mismatching versions. \n\n```sh\npip insall alectiocli\n```\n\n### Authentication\n\nFor usage of cli, you first need to authenticate with Alectio\'s server.\n\n```sh\nalectio-cli --login\n```\n![alt text](def6429b-7f66-431e-903c-caf1bae4c7df.png)\nThis will redirect you to [Alectio\'s](https://portal.alectio.com/) platform and once you login, it will generate a authentication token, which you need to copy and paste it on the command line.\n\nIf you wish to force login or refresh token after the authentication is done, use:\n```sh\nalectio-cli --login --refresh\n```\n## Usage\n\nIf you wish to get more information about any command within `alectio-cli`, you can execute `alectio-cli --help` command.\n\n### Common `alectio-cli --help` Options\n\n- `login `: Login for token authentication\n- `project `: A sub-app which handles all project related tasks\n- `experiment `: A sub-app which handles all experiment related tasks\n\n### Common `alectio-cli project --help` Options\n\n- `create `: Create an alectio project\n- `list `: List all the projects of the user\n- `delete `: Delete a project\n- `hybrid-labeling`:\n\n### Projection Creation:\n\n```sh\nalectio-cli project create [OPTIONS] YAML_FILE LABEL_FILE\n```\nA folder Alectio_cli_sample_yamls will be generated which will contain sample YAML files for doing various tasks like:\n- Yaml file for creating an experiment\n- Yaml file for manual curation experiment\n- Yaml file for Hybrid Labeling Task\n####  Sample YAML FILE for creating project\n```yml\nname: "Sample Project"\ndescription: "test "\ntype: "Image Classification"\nalectio-dataset: "false"\ntest_len: 0\ns3_bucket: \ndata_name: \nalectio_dir: \npre_loaded_model: \nproject_type: "curation"\ndata_format: "image"\ndocker_url: \npremise: "true"\ntrain_len: 10000\ndataset_source: "on-prem"\nlabels: True\n```\n#### List Projects:\n```sh\nalectio-cli project list\n```\n#### Project Deletion:\n```sh\nalectio-cli project delete <proj_id>\n```\n\n#### Hybrid Labeling Task:\n```sh\nalectio-cli project hybrid-labeling [OPTIONS] YAML_FILE\n```\n\n\n\n\n### Experiment\n\n#### Common `alectio-cli experiment --help` Options\n\n- `create `: Create an alectio experiment\n- `run `: Runs an alectio experiment\n- \n\n#### Experiment Creation\n```sh\nalectio-cli experiment create [OPTIONS] YAML_FILE\n```\n###  Sample YAML FILE for creating project\n```yml\nproject_id: \'22977034a12b11ecaf91cbe75e9b38c0\'\nname: \'Test Experiment\'\nn_records: 100\nlimits: False\nqs: [] #Empty for auto_al,ml_driven. To be filled for manual curation.\nseed: 120\nlabeling_type: pre_labeled\nis_sdk_setup: False\nis_curr_fully_labeled: False\nassoc_labeling_task_id: \'\'\n```\n\n#### Run Experiment\n```sh\nalectio-cli experiment run [OPTIONS] PYTHON_FILE EXPERIMENT_FILE\n```\n> ℹ️ Note that this cli is still in development phase, instability might occur.\n\n## Future\nWe are continually expanding and improving the offerings of this application. Some interactions may change over time, but we will do our best to retain backwards compatibility.',
    'author': 'Adwitiya',
    'author_email': 'adwitiya.trivedi@alectio.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
