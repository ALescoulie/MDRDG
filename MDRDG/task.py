r"""

"""
from collections import defaultdict
from pathlib import Path
from enum import Enum
from typing import List, Union, Type, NamedTuple, Dict, Tuple, Optional, Any, Set

from .config import Config


class Operations(Enum):
    conversion = 0
    mapping = 1
    top_gen = 2
    run_lambdas = 3
    calc_fep = 4


class ConversionSteps(Enum):
    convert = 0


class MappingSteps(Enum):
    map_ligands = 0


class TopGenSteps(Enum):
    dir_gen = 0
    ligand_gen = 1
    complex_gen = 2
    solvation = 3


class LambdaSteps(Enum):
    dir_gen = 0
    run_em = 1
    run_eq1 = 2
    run_eq2 = 3
    run_prod = 4


class FepSteps(Enum):
    run_fep = 0


Step: Type = Union[ConversionSteps, MappingSteps, TopGenSteps, LambdaSteps, FepSteps]


class Task(NamedTuple):
    step: int
    operation: Operations
    op_step: Step
    files: List[Path]
    directory: Path


def encode_task(task: Task) -> Dict[str, Any]:
    task_dict = {
        'step': task.op_step,
        'op': task.operation.value,
        'op_step': task.op_step.value,
        'files': [str(p) for p in task.files],
        'dir': str(task.directory)
    }
    return task_dict


def decode_task(task_dict: Dict[str, Any]) -> Task:
    # TODO fix encoding to use enum operations
    task: Task = Task(task_dict['step'],
                      Operations[task_dict['op']],
                      task_dict['op_step'],
                      task_dict['files'],
                      task_dict['dir'])
    return task


def run_task(task: Task) -> None:
    pass


class TaskQueue:
    _tasks: Set[Task]
    _batch_list = List[List[Task]]

    def __init__(self, tasks: List[Task]) -> None:
        self._tasks = set(tasks)
        self._batch_sort()

    def _batch_sort(self) -> None:
        batch_dict: Dict[Tuple[int, int], List[Task]] = defaultdict(list)

        for task in self._tasks:
            batch_dict[(task.operation.value, task.op_step.value)].append(task)

        batch_keys: List[Tuple[int, int]] = list(batch_dict.keys())
        self._batch_list = [batch_dict[k] for k in sorted(batch_keys, key=lambda x: (x[0], x[1]))]

    def pop(self) -> Optional[List[Task]]:
        if len(self._batch_list) == 0:
            return None
        else:
            batch: List[Task] = self._batch_list.pop(0)
            return batch

    def enqueue(self, batch: List[Task]) -> None:
        self._tasks += batch
        self._batch_sort()
