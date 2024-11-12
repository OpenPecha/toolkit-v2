import tempfile
from pathlib import Path

from openpecha.pecha.serializers.pecha_db import chapterize_json_content
from openpecha.utils import read_json


def test_pedurma_chapterization():
    DATA_DIR = Path(__file__).parent / "chaptering_data"
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        output_file = chapterize_json_content(DATA_DIR / "input.json", output_path, 2)

        assert read_json(output_file) == read_json(DATA_DIR / "expected_output.json")
