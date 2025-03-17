import logging
import os
from pathlib import Path
from shutil import rmtree

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


def get_logger(name):
    return logging.getLogger(name)


def _mkdir(path):
    if path.exists():
        rmtree(path)
    path.mkdir(exist_ok=True, parents=True)
    return path


def _mkdir_if_not(path: Path):
    """Create a directory if it does not exist"""
    if not path.exists():
        path.mkdir(exist_ok=True, parents=True)
    return path


GOOGLE_API_CRENDENTIALS_PATH = (
    Path("~/.gcloud/google_docs_and_sheets.json").expanduser().as_posix()
)

BASE_PATH = _mkdir_if_not(Path.home() / ".openpecha")
PECHAS_PATH = _mkdir_if_not(BASE_PATH / "pechas")
TEMP_CACHE_PATH = _mkdir_if_not(BASE_PATH / "temp_cache")
ALIGNMENT_PATH = _mkdir_if_not(BASE_PATH / "alignments")

INPUT_DATA_PATH = _mkdir_if_not(BASE_PATH / "input_data")
JSON_OUTPUT_PATH = _mkdir_if_not(BASE_PATH / "pechadb_json_output")

GITHUB_ORG_NAME: str = os.environ.get("GITHUB_ORG_NAME", "PechaData")

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

NO_OF_CHAPTER_SEGMENT = 100
