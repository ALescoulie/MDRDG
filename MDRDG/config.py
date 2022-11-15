r"""
:mod:`mdrdg.config` -- Reads input file and saves configuration
===============================================================

.. autoclass:: Config
    :members:
    :inherited-members:

.. autoclass:: SimulationConfig
    :members:
    :inherited-members:

.. autoclass:: SysConfig
    :members:
    :inherited-members:

.. autofunction:: load_config_from_yaml

"""

from typing import List

from pathlib import Path

from pydantic import BaseModel, conint, FilePath, DirectoryPath, ValidationError

import yaml


class SimulationConfig(BaseModel):
    """Simulation configuration details

    Attributes:
        name: The name used for the top level simulation directory
        ligand_dir: Directory containing the ligands being analyzed for relative binding free energy
        protein_file: Topology file for the protein being simulated
        lj_lambdas: Lambda values for Lennard-Jones
        col_labmdas: Lambda values for Columombic interactions
    """

    name: str
    ligand_dir: DirectoryPath
    protein_file: FilePath
    lj_lambdas: List[conint(ge=0, le=1)]
    col_lambdas: List[conint(ge=0, le=1)]
    output: str


class SysConfig(BaseModel):
    """System Configuration Details

    Attributes:
        n_cpus: Cores dedicated running simulation
        memory: Memory dedicated to running simulation
        time: Time set for the simulation
    """

    n_cpus: conint(gt=0)
    memory: str
    time: str


class Config(BaseModel):
    """
    The root configuration object for MDRDG
    """
    simulation: SimulationConfig
    system: SysConfig


def load_config_from_yaml(path: str) -> Config:
    """
    Takes a yaml input file and returns a Configuration object
    Parameters
    ----------
    path of yaml input file

    Returns
    -------
    Config
    """
    with Path(path).open('r', encoding='utf8') as file:
        try:
            return Config(**yaml.safe_load(file))
        except ValidationError as err:
            raise err
