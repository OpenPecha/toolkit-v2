import json
import tempfile
from pathlib import Path

from test_hocr_data_provider import HOCRIATestFileProvider

from openpecha.core.layer import LayerEnum
from openpecha.pecha.parsers.ocr.hocr import HOCRFormatter
from openpecha.utils import load_json, load_yaml


def test_base_text():
    work_id = "W22084"
    pecha_id = "I9876543"
    mode = "IA"

    ocr_path = Path(__file__).parent / "data" / "file_per_volume" / work_id
    expected_base_text = (
        Path(__file__).parent
        / "data"
        / "file_per_volume"
        / "opf_expected_datas"
        / "expected_base_text.txt"
    ).read_text(encoding="utf-8")
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
        pecha = formatter.create_pecha(data_provider, pecha_id, {}, ocr_import_info)
        base_text = pecha.bases["I0886"]
        base_text_line = base_text.split("\n")
        expected_base_text_line = expected_base_text.split("\n")
        for i, btl in enumerate(base_text_line):
            if btl != expected_base_text_line[i]:
                print(f"'{btl}' != '{expected_base_text_line[i]}'")
                for j, c in enumerate(btl):
                    if c != expected_base_text_line[i][j]:
                        print(f"'{c}' != '{expected_base_text_line[i][j]}'")
        assert expected_base_text == base_text


def is_same_ann(expected_ann, ann):
    if expected_ann.__dict__ == ann.__dict__:
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


def test_pagination_layer(pecha, base_name, expected_pagination_layer_dict):
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


def test_confidence_layer(pecha, base_name, expected_confidence_layer_dict):
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
    work_id = "W22084"
    pecha_id = "I9876543"
    mode = "IA"
    base_name = "I0886"
    # Load test data
    ocr_path = Path(__file__).parent / "data" / "file_per_volume" / work_id
    buda_data_path = (
        Path(__file__).parent / "data" / "file_per_volume" / "buda_data.yml"
    )
    ocr_import_info_path = (
        Path(__file__).parent / "data" / "file_per_volume" / "ocr_import_info.yml"
    )

    # Load expected layer data
    expected_pagination_layer_dict = load_json(
        Path(__file__).parent
        / "data"
        / "file_per_volume"
        / "pecha_opf_expected_data"
        / "expected_Pagination.json"
    )
    expected_confidence_layer_dict = load_json(
        Path(__file__).parent
        / "data"
        / "file_per_volume"
        / "pecha_opf_expected_data"
        / "expected_OCRConfidence.json"
    )

    ocr_import_info = load_yaml(ocr_import_info_path)
    buda_data = load_yaml(buda_data_path)
    image_list_path = Path(__file__).parent / "data" / "file_per_volume"
    data_provider = HOCRIATestFileProvider(
        work_id, image_list_path, buda_data, ocr_import_info, ocr_path
    )

    opf_options = {"ocr_confidence_threshold": 0.9, "max_low_conf_per_page": 50}

    with tempfile.TemporaryDirectory() as tmpdirname:
        formatter = HOCRFormatter(mode=mode, output_path=tmpdirname)
        pecha = formatter.create_pecha(
            data_provider, pecha_id, opf_options, ocr_import_info
        )
        # Test each layer separately
        test_pagination_layer(pecha, base_name, expected_pagination_layer_dict)
        test_confidence_layer(pecha, base_name, expected_confidence_layer_dict)


if __name__ == "__main__":
    test_base_text()
    test_build_layers()
