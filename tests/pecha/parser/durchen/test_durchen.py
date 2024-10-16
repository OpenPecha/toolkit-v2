from pathlib import Path

from openpecha.pecha.parsers.durchen import DurchenParser


def test_durchen():
    data = Path(__file__).parent / "data"
    pedurmafile = data / "pedurma_hfml.txt"
    pedurma_text = pedurmafile.read_text(encoding="utf-8")

    parser = DurchenParser()

    output_path = Path(__file__).parent / "output"
    parser.parse(pedurma_text, metadata={}, output_path=output_path)


test_durchen()
