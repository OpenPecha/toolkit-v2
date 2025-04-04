from pathlib import Path
from typing import Dict

from openpecha.utils import read_json


def extract_metadata_for_work(work_path: Path) -> Dict:
    metadata = {}
    ocr_import_info = read_json(work_path / "ocr_import_info.json")
    metadata["ocr_import_info"] = ocr_import_info
    buda_data = read_json(work_path / "buda_data.json")
    metadata["buda_data"] = buda_data

    return metadata


def format_metadata_for_op_api(metadata: Dict) -> Dict:
    NA = "NA"
    buda_data = metadata["buda_data"]["source_metadata"]

    if buda_data.get("author"):
        author = buda_data["author"]
    else:
        author = NA

    if buda_data.get("title"):
        title = buda_data["title"]
    else:
        title = NA

    if buda_data.get("long_title"):
        long_title = buda_data["long_title"]
    else:
        long_title = NA

    if buda_data.get("languages"):
        language = buda_data["languages"][0]
    else:
        language = NA

    formatted_data = {
        "bdrc": metadata,
        "author": {"bo": author},
        "document_id": NA,
        "language": language,
        "long_title": {"bo": long_title},
        "source_url": buda_data["id"],
        "title": {"bo": title, "en": NA},
    }

    return formatted_data
