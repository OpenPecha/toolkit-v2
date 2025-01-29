from pathlib import Path
from shutil import rmtree


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
ALIGNMENT_PATH = _mkdir_if_not(BASE_PATH / "alignments")

INPUT_DATA_PATH = _mkdir_if_not(BASE_PATH / "input_data")
JSON_OUTPUT_PATH = _mkdir_if_not(BASE_PATH / "pechadb_json_output")

SERIALIZED_ALIGNMENT_JSON_PATH = _mkdir_if_not(BASE_PATH / "serialized_alignment_jsons")

GOOGLE_API_TOKEN_PATH = (
    BASE_PATH / "token.pickle"
)  # This token is recieved after authentication with Google Drive using credential.json

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
