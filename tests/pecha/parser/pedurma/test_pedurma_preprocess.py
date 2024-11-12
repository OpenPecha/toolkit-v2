from pathlib import Path

from openpecha.pecha.parsers.pedurma import preprocess_pedurma_text


def test_pedurma_preprocess():
    DATA_DIR = Path(__file__).parent / "preprocess_input"

    input_text = (DATA_DIR / "input.txt").read_text(encoding="utf-8")
    output = preprocess_pedurma_text(input_text)

    expected_output = (DATA_DIR / "expected_output.txt").read_text(encoding="utf-8")
    assert output == expected_output
