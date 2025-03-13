import tempfile
from pathlib import Path

from test_hocr_data_provider import BDRCGBTestFileProvider

from openpecha.pecha.parsers.ocr.hocr import HOCRFormatter
from openpecha.utils import load_json, load_yaml


def test_google_ocr_metadata():
    work_id = "W1KG10193"
    pecha_id = "I123456"

    ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
    expected_meta_path = (
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_opf_expected_data"
        / "expected_hocr_meta.json"
    )
    buda_data_path = Path(__file__).parent / "data" / "file_per_page" / "buda_data.yml"
    ocr_import_info_path = (
        Path(__file__).parent / "data" / "file_per_page" / "ocr_import_info.yml"
    )
    ocr_import_info = load_yaml(ocr_import_info_path)
    buda_data = load_yaml(buda_data_path)
    bdrc_image_list_path = Path(__file__).parent / "data" / "file_per_page"
    data_provider = BDRCGBTestFileProvider(
        work_id, bdrc_image_list_path, buda_data, ocr_import_info, ocr_path
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRFormatter(output_path=tmpdirname)
        pecha = formatter.create_pecha(data_provider, pecha_id, {}, ocr_import_info)
        output_metadata = pecha.load_metadata()
        expected_metadata = load_json(expected_meta_path)

        # Check licence field (note the spelling)
        assert (
            output_metadata.licence.value == expected_metadata["licence"]
        ), "Licence mismatch"

        # Check copyright fields
        assert (
            output_metadata.copyright.status.value
            == expected_metadata["copyright"]["status"]
        ), "Copyright status mismatch"
        assert (
            output_metadata.copyright.notice == expected_metadata["copyright"]["notice"]
        ), "Copyright notice mismatch"
        assert (
            output_metadata.copyright.info_url
            == expected_metadata["copyright"]["info_url"]
        ), "Copyright info URL mismatch"

        # Check source metadata fields
        assert output_metadata.source_metadata.get("access") == expected_metadata[
            "source_metadata"
        ].get("access"), "Source metadata access mismatch"
        assert output_metadata.source_metadata.get(
            "geo_restriction"
        ) == expected_metadata["source_metadata"].get(
            "geo_restriction"
        ), "Source metadata geo restriction mismatch"


if __name__ == "__main__":
    test_google_ocr_metadata()
