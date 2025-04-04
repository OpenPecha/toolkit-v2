import json
import tempfile
from pathlib import Path

from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.ocr.data_providers import BDRCGBFileProvider
from openpecha.pecha.parsers.ocr.hocr import HOCRParser
from openpecha.utils import read_json


def test_base_text():
    work_id = "W1KG10193"
    pecha_id = "I123456"

    ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
    expected_base_text = (
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_expected_data"
        / "expected_base_text.txt"
    ).read_text(encoding="utf-8")
    buda_data_path = (
        Path(__file__).parent / "data" / "file_per_page" / work_id / "buda_data.json"
    )
    ocr_import_info_path = (
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / work_id
        / "ocr_import_info.json"
    )
    ocr_import_info = read_json(ocr_import_info_path)
    buda_data = read_json(buda_data_path)
    data_provider = BDRCGBFileProvider(work_id, buda_data, ocr_import_info, ocr_path)

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRParser(output_path=tmpdirname)
        pecha = formatter.parse(data_provider, pecha_id, {}, ocr_import_info)
        base_text = pecha.bases["I1KG10195"]
        assert expected_base_text == base_text


def is_same_ann(expected_ann, ann):
    if expected_ann.model_dump() == ann.model_dump():
        return True
    return False


def extract_annotation_values(annotation_store, annotation):
    """Extract values from annotation data by resolving references"""
    values = {}

    # Handle direct data format
    if isinstance(annotation["data"], dict):
        return annotation["data"]

    # Handle list format with direct values
    if isinstance(annotation["data"], list):
        for d in annotation["data"]:
            if isinstance(d, dict):
                if "key" in d and "value" in d:
                    values[d["key"]] = d["value"]
                elif any(k in d for k in ["imgnum", "language", "confidence"]):
                    values.update(d)

    # Handle STAM format with references
    if isinstance(annotation["data"], list) and "@type" in annotation_store:
        data_map = {}
        # Build map of data IDs to their values
        if "annotationsets" in annotation_store:
            for dataset in annotation_store["annotationsets"]:
                if "data" in dataset:
                    for d in dataset["data"]:
                        if "key" in d and "value" in d:
                            if isinstance(d["value"], dict) and "value" in d["value"]:
                                data_map[d["@id"]] = {
                                    "key": d["key"],
                                    "value": d["value"]["value"],
                                }
                            else:
                                data_map[d["@id"]] = {
                                    "key": d["key"],
                                    "value": d["value"],
                                }

        # Resolve references in annotation data
        for d in annotation["data"]:
            if "@id" in d and d["@id"] in data_map:
                data = data_map[d["@id"]]
                values[data["key"]] = data["value"]

    return values


def get_annotation_bounds(annotation):
    """Extract start and end positions from annotation"""
    offset = annotation["target"].get("offset", {})

    start = (
        offset.get("begin", {}).get("value", None)
        if isinstance(offset.get("begin"), dict)
        else offset.get("start")
    )
    end = (
        offset.get("end", {}).get("value", None)
        if isinstance(offset.get("end"), dict)
        else offset.get("end")
    )

    return start, end


def _test_pagination_layer(pecha, base_name, expected_pagination_layer_dict):
    """Test pagination layer annotations"""
    _, pagination_layer_file = pecha.get_layer_by_ann_type(
        base_name, LayerEnum.pagination
    )
    assert pagination_layer_file.exists(), "Pagination layer file should exist"
    assert pagination_layer_file.name.startswith(
        "Pagination-"
    ), "Pagination layer file name should start with 'Pagination-'"

    pagination_layer_content = json.loads(pagination_layer_file.read_text())

    for i, (actual, expected) in enumerate(
        zip(
            pagination_layer_content["annotations"],
            expected_pagination_layer_dict["annotations"],
        )
    ):
        # Compare spans
        actual_start, actual_end = get_annotation_bounds(actual)
        expected_start, expected_end = get_annotation_bounds(expected)

        assert (
            actual_start == expected_start
        ), f"Pagination start position mismatch at index {i}"
        assert (
            actual_end == expected_end
        ), f"Pagination end position mismatch at index {i}"

        # Compare data
        actual_data = extract_annotation_values(pagination_layer_content, actual)
        expected_data = extract_annotation_values(
            expected_pagination_layer_dict, expected
        )

        assert actual_data.get("imgnum") == expected_data.get(
            "imgnum"
        ), f"Image number mismatch at index {i}"
        assert actual_data.get("reference") == expected_data.get(
            "reference"
        ), f"Reference mismatch at index {i}"


def _test_language_layer(pecha, base_name, expected_language_layer_dict):
    """Test language layer annotations"""
    _, language_layer_file = pecha.get_layer_by_ann_type(base_name, LayerEnum.language)
    assert language_layer_file.exists(), "Language layer file should exist"
    assert language_layer_file.name.startswith(
        "Language-"
    ), "Language layer file name should start with 'Language-'"

    language_layer_content = json.loads(language_layer_file.read_text())

    for i, (actual, expected) in enumerate(
        zip(
            language_layer_content["annotations"],
            expected_language_layer_dict["annotations"],
        )
    ):
        # Compare spans
        actual_start, actual_end = get_annotation_bounds(actual)
        expected_start, expected_end = get_annotation_bounds(expected)

        assert (
            actual_start == expected_start
        ), f"Language start position mismatch at index {i}"
        assert (
            actual_end == expected_end
        ), f"Language end position mismatch at index {i}"

        # Compare data
        actual_data = extract_annotation_values(language_layer_content, actual)
        expected_data = extract_annotation_values(
            expected_language_layer_dict, expected
        )

        assert actual_data.get("language") == expected_data.get(
            "language"
        ), f"Language value mismatch at index {i}"


def _test_confidence_layer(pecha, base_name, expected_confidence_layer_dict):
    """Test OCR confidence layer annotations"""
    _, confidence_layer_file = pecha.get_layer_by_ann_type(
        base_name, LayerEnum.ocr_confidence
    )
    assert confidence_layer_file.exists(), "OCR confidence layer file should exist"
    assert confidence_layer_file.name.startswith(
        "OCRConfidence-"
    ), "OCR confidence layer file name should start with 'OCRConfidence-'"

    confidence_layer_content = json.loads(confidence_layer_file.read_text())

    for i, (actual, expected) in enumerate(
        zip(
            confidence_layer_content["annotations"],
            expected_confidence_layer_dict["annotations"],
        )
    ):
        # Compare spans
        actual_start, actual_end = get_annotation_bounds(actual)
        expected_start, expected_end = get_annotation_bounds(expected)

        assert (
            actual_start == expected_start
        ), f"Confidence start position mismatch at index {i}"
        assert (
            actual_end == expected_end
        ), f"Confidence end position mismatch at index {i}"

        # Compare data
        actual_data = extract_annotation_values(confidence_layer_content, actual)
        expected_data = extract_annotation_values(
            expected_confidence_layer_dict, expected
        )

        assert actual_data.get("confidence") == expected_data.get(
            "confidence"
        ), f"Confidence value mismatch at index {i}"


def test_build_layers():
    # Test setup
    work_id = "W1KG10193"
    pecha_id = "I123456"
    base_name = "I1KG10195"

    # Load test data
    ocr_path = Path(__file__).parent / "data" / "file_per_page" / work_id
    buda_data_path = (
        Path(__file__).parent / "data" / "file_per_page" / work_id / "buda_data.json"
    )
    ocr_import_info_path = (
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / work_id
        / "ocr_import_info.json"
    )

    # Load expected layer data
    expected_pagination_layer_dict = read_json(
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_expected_data"
        / "expected_Pagination.json"
    )
    expected_language_layer_dict = read_json(
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_expected_data"
        / "expected_Language.json"
    )
    expected_confidence_layer_dict = read_json(
        Path(__file__).parent
        / "data"
        / "file_per_page"
        / "pecha_expected_data"
        / "expected_OCRConfidence.json"
    )

    # Load configuration data
    ocr_import_info = read_json(ocr_import_info_path)
    buda_data = read_json(buda_data_path)

    # Initialize data provider and formatter
    data_provider = BDRCGBFileProvider(work_id, buda_data, ocr_import_info, ocr_path)
    opf_options = {"ocr_confidence_threshold": 0.9, "max_low_conf_per_page": 50}

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRParser(output_path=tmpdirname)
        pecha = formatter.parse(data_provider, pecha_id, opf_options, ocr_import_info)

        # Test each layer
        _test_pagination_layer(pecha, base_name, expected_pagination_layer_dict)
        _test_language_layer(pecha, base_name, expected_language_layer_dict)
        _test_confidence_layer(pecha, base_name, expected_confidence_layer_dict)


if __name__ == "__main__":
    test_base_text()
    test_build_layers()
