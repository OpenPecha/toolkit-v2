import tempfile
from pathlib import Path

from test_hocr_data_provider import BDRCGBTestFileProvider

from openpecha.pecha.parsers.ocr.hocr import HOCRParser
from openpecha.utils import read_json


def test_google_ocr_base_meta():
    work_id = "W1KG10193"
    pecha_id = "I123456"

    ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
    expected_meta_path = (
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_expected_data"
        / "expected_hocr_meta.json"
    )
    buda_data_path = Path(__file__).parent / "data" / "file_per_page" / "buda_data.json"
    ocr_import_info_path = (
        Path(__file__).parent / "data" / "file_per_page" / "ocr_import_info.json"
    )
    ocr_import_info = read_json(ocr_import_info_path)
    buda_data = read_json(buda_data_path)
    bdrc_image_list_path = Path(__file__).parent / "data" / "file_per_page"
    data_provider = BDRCGBTestFileProvider(
        work_id, bdrc_image_list_path, buda_data, ocr_import_info, ocr_path
    )

    expected_metadata = read_json(expected_meta_path)
    if not expected_metadata:
        raise ValueError(f"Failed to read expected metadata from {expected_meta_path}")

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRParser(output_path=tmpdirname)
        pecha = formatter.parse(
            data_provider, pecha_id, {"remove_duplicate_symbols": True}, ocr_import_info
        )
        output_metadata = pecha.load_metadata()

        assert output_metadata.source_metadata == expected_metadata.get(
            "source_metadata"
        ), "Source metadata mismatch"
        assert output_metadata.bases == expected_metadata.get(
            "bases"
        ), "Bases metadata mismatch"


if __name__ == "__main__":
    test_google_ocr_base_meta()
