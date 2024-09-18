from pathlib import Path

from openpecha.pecha.parsers.plaintext.parser import PechaFrameWork


def test_parser():
    DATA = Path(__file__).parent / "data"
    input_file = DATA / "basefile.txt"
    input_text = input_file.read_text(encoding="utf-8")

    openpecha_framework = PechaFrameWork(input_text)
    pipeline_definition = ["chapter_parser_pipe"]
    openpecha_framework.parser_pipeline(pipeline_definition)


test_parser()
