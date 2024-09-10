from pathlib import Path

from openpecha.pecha.parsers.plaintext.plaintext_parser import PlainTextParser


def test_ann_on_ann_parse():
    data_folder = Path(__file__).parent / "data"
    pecha_id = "ID534D0B0"
    basefile_name = "1bfe"
    ann_store_file_name = "Chapter-13c.json"
    ann_store_path = (
        data_folder / pecha_id / "layers" / basefile_name / ann_store_file_name
    )

    parser = PlainTextParser(
        ann_store_path, PlainTextParser.two_new_line_segmenter, "Tsawa"
    )

    ann_store_path = parser.parse_ann_on_ann()


test_ann_on_ann_parse()
