from pathlib import Path

from openpecha.pecha.parsers.ocr.google_vision import GoogleVisionParser
from openpecha.utils import read_json

ocr_path = Path(__file__).parent / "data" / "I1PD958780125.json"
expected_output = (
    Path(__file__).parent / "data" / "expected_output_of_I1PD958780125.txt"
).read_text(encoding="utf-8")


def test_remove_overlap_and_duplicates():

    state = {
        "base_layer_len": 0,
        "base_layer": "",
        "low_confidence_annotations": {},
        "language_annotations": [],
        "pagination_annotations": {},
        "word_confidences": [],
        "latest_language_annotation": None,
        "latest_low_confidence_annotation": None,
        "page_low_confidence_annotations": [],
    }

    ocr_object = read_json(ocr_path)

    google_parser = GoogleVisionParser()

    bboxes, avg_char_width = google_parser.get_char_base_bboxes_and_avg_width(
        response=ocr_object
    )

    google_parser.remove_duplicate_symbols = True
    google_parser.same_line_ratio_threshold = 0.2
    google_parser.check_postprocessing = False

    google_parser.build_page(bboxes, 1, "I1PD958780125", state, avg_char_width)
    base = state["base_layer"]

    assert base == expected_output
