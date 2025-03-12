import tempfile
from pathlib import Path

from test_hocr_data_provider import BDRCGBTestFileProvider

from openpecha.core.layer import Layer, LayerEnum
from openpecha.pecha.parsers.ocr.hocr import HOCRFormatter
from openpecha.utils import load_yaml


def test_base_text():
    work_id = "W1KG10193"
    pecha_id = "I123456"

    ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
    expected_base_text = (
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_opf_expected_data"
        / "expected_base_text.txt"
    ).read_text(encoding="utf-8")
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
        base_text = pecha.bases["I1KG10195"]
        assert expected_base_text == base_text


def is_same_ann(expected_ann, ann):
    if expected_ann.__dict__ == ann.__dict__:
        return True
    return False


def test_build_layers():
    work_id = "W1KG10193"
    pecha_id = "I123456"
    base_name = "I1KG10195"

    ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
    expected_pagination_layer_dict = load_yaml(
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_opf_expected_data"
        / "expected_Pagination.json"
    )
    expected_pagination_layer = Layer(
        annotation_type=LayerEnum.pagination,
        annotations=expected_pagination_layer_dict["annotations"],
    )
    expected_language_layer_dict = load_yaml(
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_opf_expected_data"
        / "expected_Language.json"
    )
    expected_language_layer = Layer(
        annotation_type=LayerEnum.language,
        annotations=expected_language_layer_dict["annotations"],
    )
    expected_confidence_layer_dict = load_yaml(
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_opf_expected_data"
        / "expected_OCRConfidence.json"
    )
    expected_confidence_layer = Layer(
        annotation_type=LayerEnum.ocr_confidence,
        annotations=expected_confidence_layer_dict["annotations"],
    )
    buda_data_path = Path(__file__).parent / "data" / "file_per_page" / "buda_data.yml"
    ocr_import_info_path = (
        Path(__file__).parent / "data" / "file_per_page" / "ocr_import_info.yml"
    )
    ocr_import_info = load_yaml(ocr_import_info_path)
    buda_data = load_yaml(buda_data_path)
    image_list_path = Path(__file__).parent / "data" / "file_per_page"
    data_provider = BDRCGBTestFileProvider(
        work_id, image_list_path, buda_data, ocr_import_info, ocr_path
    )

    opf_options = {"ocr_confidence_threshold": 0.9, "max_low_conf_per_page": 50}

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRFormatter(output_path=tmpdirname)
        pecha = formatter.create_pecha(
            data_provider, pecha_id, opf_options, ocr_import_info
        )
        pagination_layer = pecha.layers[base_name][LayerEnum.pagination]
        language_layer = pecha.layers[base_name][LayerEnum.language]
        confidence_layer = pecha.layers[base_name][LayerEnum.ocr_confidence]

        ###Pagination layer testing
        for (_, expected_ann), (_, ann) in zip(
            expected_pagination_layer.get_annotations(),
            pagination_layer.get_annotations(),
        ):
            assert is_same_ann(expected_ann, ann)

        ###Language layer testing
        for (_, expected_ann), (_, ann) in zip(
            expected_language_layer.get_annotations(), language_layer.get_annotations()
        ):
            assert is_same_ann(expected_ann, ann)

        ###Confidence layer testing
        for (_, expected_ann), (_, ann) in zip(
            expected_confidence_layer.get_annotations(),
            confidence_layer.get_annotations(),
        ):
            assert is_same_ann(expected_ann, ann)


if __name__ == "__main__":
    test_base_text()
    test_build_layers()
