from pathlib import Path
from shutil import rmtree


def _mkdir(path):
    if path.exists():
        rmtree(path)
    path.mkdir(exist_ok=True, parents=True)
    return path


def _mkdir_if_not(path: Path):
    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
    return path


BASE_PATH = _mkdir_if_not(Path.home() / ".openpecha")
PECHAS_PATH = _mkdir_if_not(BASE_PATH / "pechas")
ALIGNMENT_PATH = _mkdir_if_not(BASE_PATH / "alignment")

PECHA_DATA_ORG = "PechaData"

LINE_BREAKERS = [
    "། །",
    "ག །",
    "ག།",
    "།།",
    "ཤ །",
    "ཤ།",
    "ཀ།",
    "ཀ །",
    "།། །།",
    "། །།",
    "།།།",
]
