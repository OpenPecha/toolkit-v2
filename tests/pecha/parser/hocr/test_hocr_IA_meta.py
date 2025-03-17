import tempfile
from pathlib import Path

from test_hocr_data_provider import HOCRIATestFileProvider

from openpecha.pecha.parsers.ocr.hocr import HOCRFormatter
from openpecha.utils import load_json   


def test_google_ocr_metadata():
    work_id = "W22084"
    pecha_id = "I9876543"
    mode = "IA"

    ocr_path = Path(__file__).parent / "data" / "file_per_volume" / work_id
    expected_meta_path = (
        Path(__file__).parent
        / "data"
        / "file_per_volume"
        / "pecha_expected_data"
        / "expected_hocr_meta.json"
    )
    buda_data_path = (
        Path(__file__).parent / "data" / "file_per_volume" / "buda_data.json"
    )
    ocr_import_info_path = (
        Path(__file__).parent / "data" / "file_per_volume" / "ocr_import_info.json"
    )
    ocr_import_info = load_json(ocr_import_info_path)
    buda_data = load_json(buda_data_path)
    bdrc_image_list_path = Path(__file__).parent / "data" / "file_per_volume"
    data_provider = HOCRIATestFileProvider(
        work_id, bdrc_image_list_path, buda_data, ocr_import_info, ocr_path
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRFormatter(mode=mode, output_path=tmpdirname)
        pecha = formatter.create_pecha(data_provider, pecha_id, {}, ocr_import_info)
        output_metadata = pecha.load_metadata()
        expected_metadata = load_json(expected_meta_path)

        # Check licence field (note the spelling)
        assert output_metadata.licence.value == expected_metadata["licence"]

        # Check copyright fields
        assert (
            output_metadata.copyright.status.value
            == expected_metadata["copyright"]["status"]
        )
        assert (
            output_metadata.copyright.notice == expected_metadata["copyright"]["notice"]
        )
        assert (
            output_metadata.copyright.info_url
            == expected_metadata["copyright"]["info_url"]
        )

        # Check source metadata fields
        assert output_metadata.source_metadata.get("access") == expected_metadata[
            "source_metadata"
        ].get("access")
        assert output_metadata.source_metadata.get(
            "geo_restriction"
        ) == expected_metadata["source_metadata"].get("geo_restriction")


if __name__ == "__main__":
    test_google_ocr_metadata()
