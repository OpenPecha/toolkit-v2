from pathlib import Path
from shutil import rmtree


def _mkdir(path):
    if path.exists():
        rmtree(path)
    path.mkdir(exist_ok=True, parents=True)
    return path


BASE_PATH = _mkdir(Path.home() / ".openpecha")
PECHAS_PATH = _mkdir(BASE_PATH / "pechas")

PECHA_ANNOTATION_STORE_ID = "PechaAnnotationStore"
PECHA_DATASET_ID = "PechaDataSet"
