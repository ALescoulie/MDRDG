r"""

"""

import time
import os
from pathlib import Path

from typing import Dict

import json

import gromacs
import yaml
from gromacs.utilities import in_dir

from MDRDG import Config
from ._version import get_versions


def save_metadata(config_path: Path) -> None:
    metadata: Dict[str, str] = {'MDRDG version': f'{get_versions()}',
                                'GROMACS version': f'{gromacs.get_versions()}',
                                'start time': f'{time.localtime()}',
                                'config': f'{yaml.safe_load(str(config_path))}'}
    with open('_metadata.json', 'w') as file:
        json.dump(metadata, file)


def start_sim_dir(sim_name: str) -> None:
    try:
        os.mkdir(sim_name)
    except FileExistsError:
        pass

