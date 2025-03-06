import tempfile
from pathlib import Path

from test_hocr_data_provider import HOCRIATestFileProvider

from openpecha.pecha.parsers.ocr.hocr import HOCRFormatter
from openpecha.utils import load_yaml


def test_google_ocr_metadata():
    work_id = "W22084"
    pecha_id = "I9876543"
    mode = "IA"

    ocr_path = Path(__file__).parent / "data" / "file_per_volume" / work_id
    expected_meta_path = (
        Path(__file__).parent
        / "data"
        / "file_per_volume"
        / "opf_expected_datas"
        / "expected_hocr_meta.yml"
    )
    buda_data_path = (
        Path(__file__).parent / "data" / "file_per_volume" / "buda_data.yml"
    )
    ocr_import_info_path = (
        Path(__file__).parent / "data" / "file_per_volume" / "ocr_import_info.yml"
    )
    ocr_import_info = load_yaml(ocr_import_info_path)
    buda_data = load_yaml(buda_data_path)
    bdrc_image_list_path = Path(__file__).parent / "data" / "file_per_volume"
    data_provider = HOCRIATestFileProvider(
        work_id, bdrc_image_list_path, buda_data, ocr_import_info, ocr_path
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRFormatter(mode=mode, output_path=tmpdirname)
        pecha = formatter.create_opf(data_provider, pecha_id, {}, ocr_import_info)
        output_metadata = pecha.read_meta_file()
        expected_metadata = load_yaml(expected_meta_path)
        assert output_metadata["license"] == expected_metadata["license"]
        assert output_metadata["copyright"] == expected_metadata["copyright"]
        assert (
            output_metadata["source_metadata"]["access"]
            == expected_metadata["source_metadata"]["access"]
        )
        assert output_metadata["source_metadata"].get(
            "geo_restriction"
        ) == expected_metadata["source_metadata"].get("geo_restriction")


if __name__ == "__main__":
    test_google_ocr_metadata()
