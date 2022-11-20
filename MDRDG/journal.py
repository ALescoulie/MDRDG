r"""

"""
import glob
import os
from pathlib import Path
from typing import List, Dict, Any, Tuple, Optional
import json

from gromacs.utilities import in_dir

from .config import Config
import task
from .task import Task, encode_task, decode_task


class Journal:
    """

    """
    _config: Config
    _cur_step: int
    _sim_name: str
    _input_path: str
    _ligand_pairs: List[Tuple[int, int]] = []
    _ligand_keys: Dict[str, int]
    _pair_dirs: Dict[str, Path]
    _lambda_dirs: Dict[str, Path]

    def __init__(self, config: Config, sim_dir: Path):
        self._config = config

        with in_dir(sim_dir, create=True):
            if os.path.exists('_tasks_main.json'):
                with open('_tasks_main.json', 'r') as file:
                    data: Dict[str, Any] = json.load(file)
                    self._sim_name = data['name']
                    self._cur_step = data['cur_step']
                    self._ligand_pairs = data['ligand_pairs']
            else:
                self._cur_step = 0
                self._create_main_task_file()

    def _create_main_task_file(self) -> None:
        with open('_tasks_main.json', 'r') as file:
            data: Dict[str, Any] = {
                'name': self._sim_name,
                'cur_step': 0,
                'col_lambdas': self._config.simulation.col_lambdas,
                'vdw_lambdas': self._config.simulation.lj_lambdas,
                'ligand_pairs': self._ligand_pairs,
            }
            json.dump(data, file)

    def _create_task_file(self, name: str, todo: List[Task]) -> None:
        with in_dir(self._sim_name, create=False):
            with open(f'{name}.json', 'w') as file:
                data: Dict[str, Any] = {
                    "done": False,
                    "todo": [encode_task(task) for task in todo],
                    "completed": []
                }
                json.dump(data, file)

    @staticmethod
    def _parse_task_file(path: str) -> Optional[List[Task]]:
        with open(f'{path}', 'r') as file:
            data = json.load(file)
            if data['done']:
                return None
            else:
                return [decode_task(t) for t in data['todo']]

    def _get_step0_tasks(self) -> Optional[List[Task]]:
        task_file = os.path.join(f'{self._sim_name}', '_tasks_step0.json')
        if os.path.exists(task_file):
            return self._parse_task_file(task_file)
        else:
            ligands = glob.glob(str(self._config.simulation.ligand_dir))
            tasks: List[Task] = []
            for file in ligands:
                tasks.append(Task(0,
                                  task.Operations.conversion,
                                  task.ConversionSteps.convert,
                                  [Path(os.path.abspath(file))],
                                  Path(self._config.simulation.ligand_dir)))
            self._create_task_file(task_file, tasks)
            return tasks

    def _get_step1_tasks(self) -> Optional[List[Task]]:
        task_file = os.path.join(f'{self._sim_name}', '_tasks_step1.json')
        if os.path.exists(task_file):
            return self._parse_task_file(task_file)
        else:
            task1: Task = Task(1,
                               task.Operations.mapping,
                               task.MappingSteps.map_ligands,
                               [Path(os.path.join(self._sim_name, 'ligands'))],
                               Path(self._sim_name))
            self._create_task_file(task_file, [task1])
            return [task1]

    def _get_step2_tasks(self) -> None:
        pass

    def _get_step3_tasks(self) -> None:
        pass

    def _get_step4_tasks(self) -> None:
        pass

    def find_tasks(self) -> List[Task]:
        pass

    def record(self, complete_task: Task) -> None:
        pass
