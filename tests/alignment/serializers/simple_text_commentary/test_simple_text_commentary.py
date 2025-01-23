from pathlib import Path

from openpecha.alignment.serializers.simple_text_commentary import (
    SimpleTextCommentarySerializer,
    parse_root_idx_mapping_string,
)
from openpecha.utils import read_json


def test_simple_text_commentary_serializer():
    DATA_DIR = Path(__file__).parent / "data"
    root_opf_path = DATA_DIR / "root" / "IC537C534"
    commentary_opf_path = DATA_DIR / "commentary" / "IBDF9A009"

    serializer = SimpleTextCommentarySerializer()

    json_output = serializer.serialize(root_opf_path, commentary_opf_path)
    expected_output_file = DATA_DIR / "expected_output.json"
    assert json_output == read_json(expected_output_file)


def test_parse_root_idx_mapping():
    input = "1"
    expected_output = ["1"]
    assert parse_root_idx_mapping_string(input) == expected_output

    input = "1-3"
    expected_output = ["1", "2", "3"]
    assert parse_root_idx_mapping_string(input) == expected_output

    input = "1,3"
    expected_output = ["1", "3"]
    assert parse_root_idx_mapping_string(input) == expected_output

    input = "1-3,5"
    expected_output = ["1", "2", "3", "5"]
    assert parse_root_idx_mapping_string(input) == expected_output
