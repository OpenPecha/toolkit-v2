import csv
import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List

from openpecha.exceptions import FileNotFoundError


@contextmanager
def cwd(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def read_csv(file_path) -> List[List[str]]:
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows


def write_csv(file_path, data) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def read_json(fn: str | Path) -> Dict:
    fn = Path(fn)
    if not fn.is_file():
        raise FileNotFoundError(f"{str(fn)} JSON file is not found to read.")
    with fn.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(
    output_fn: str | Path,
    data: Dict,
) -> Path:
    """Dump data to a JSON file."""
    output_fn = Path(output_fn)
    output_fn.parent.mkdir(exist_ok=True, parents=True)
    with output_fn.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_fn
