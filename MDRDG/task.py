r"""

"""
from collections import defaultdict
from pathlib import Path
from enum import Enum
from typing import List, Union, Type, NamedTuple, Dict, Tuple, Optional


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
    step: Step
    files: List[Path]
    directory: Path


def run_task(task: Task) -> None:
    pass


class TaskQueue:
    _tasks: List[Task]
    _batch_list = List[List[Task]]
    _n_cur: int

    def __init__(self, tasks: List[Task]) -> None:
        self._tasks = tasks

    def _build_batches(self) -> None:
        batch_dict: Dict[Tuple[int, int], List[Task]] = defaultdict(list)

        for task in self._tasks:
            batch_dict[(task.operation.value, task.step.value)].append(task)

        batch_keys: List[Tuple[int, int]] = list(batch_dict.keys())
        self._batch_list = [batch_dict[k] for k in sorted(batch_keys, key=lambda x: (x[0], x[1]))]

    def pop_batch(self) -> Optional[List[Task]]:
        if self._n_cur == len(self._batch_list):
            return None
        else:
            batch: List[Task] = self._batch_list[self._n_cur]
            self._n_cur += 1
            return batch
