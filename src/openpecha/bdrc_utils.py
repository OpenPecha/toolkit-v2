from pathlib import Path
from typing import Any, Dict

from openpecha.utils import read_json


def extract_metadata_for_work(work_path: Path) -> Dict[str, Any]:
    metadata = {}
    ocr_import_info = read_json(work_path / "ocr_import_info.json")
    metadata["ocr_import_info"] = ocr_import_info
    buda_data = read_json(work_path / "buda_data.json")
    metadata["buda_data"] = buda_data

    return metadata


def format_metadata_for_op_api(metadata: Dict[str, Any]) -> Dict[str, Any]:
    buda_data = metadata.get("buda_data", {}).get("source_metadata", {})
    document_id = metadata.get("ocr_import_info", {}).get("bdrc_scan_id")
    author = buda_data.get("author", None)
    title = buda_data.get("title", None)
    language = (
        buda_data.get("languages", [None])[0] if buda_data.get("languages") else None
    )
    source_type = "bdrc"

    formatted_data = {
        "source_type": source_type,
        "bdrc": metadata,
        "author": {"bo": author},
        "document_id": document_id,
        "language": language,
        "source_url": buda_data.get("id", None),
        "title": {"bo": title},
    }

    return formatted_data
