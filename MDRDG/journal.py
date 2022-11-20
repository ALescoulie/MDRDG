r"""

"""
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass
import json


from .config import Config

class Journal:
    """

    """

    cur_step: int

    def __init__(self, config: Config, sim_dir: Path):
        os.chdir(str(Path))

        if os.path.exists('_tasks_main.json'):
            with open('_tasks_main.json', 'r') as file:
                data: Dict[str, Any] = json.load(file)
                self.cur_step = data["cur_step"]
        else:

