r"""

"""

from pathlib import Path

from typing import List, NamedTuple

from pydantic import DirectoryPath

import glob


class Ligand(NamedTuple):
    name: str
    file: Path


class LigandMol2(NamedTuple):
    name: str
    file: Path


def collect_ligands(directory: DirectoryPath) -> List[Ligand]:
    ligands: List[Ligand] = []
    for i, f in enumerate(glob.glob(str(directory)))
        f_path: Path = Path(str(f))
        ligands.append(Ligand(f_path.stem, f_path))
    return ligands


def convert_ligands(ligands: List[Ligand]) -> List[LigandMol2]:
    pass
