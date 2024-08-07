from pathlib import Path
from shutil import rmtree

from openpecha.pecha.parsers.plaintext.chapter_parser import (
    PlainTextChapterAnnotationParser,
)


def test_plain_text_chapter_ann_parser():
    DATA = Path(__file__).parent / "data"
    file_path = DATA / "chapter_annotation.txt"
    metadata_path = DATA / "metadata.json"

    chapter_ann_parser = PlainTextChapterAnnotationParser.from_file(
        file_path, metadata_path
    )
    assert isinstance(chapter_ann_parser, PlainTextChapterAnnotationParser)
    pecha_path = chapter_ann_parser.parse(DATA)

    assert pecha_path.exists()
    assert (pecha_path / "metadata.json").exists()
    assert (pecha_path / "base").exists()
    assert (pecha_path / "layers").exists()
    """ check there is only one json file in layers """
    assert len(list((pecha_path / "layers").glob("*.json"))) == 1
    """ check there is one txt file in base """
    assert len(list((pecha_path / "base").glob("*.txt"))) == 1

    """ clean up """
    rmtree(pecha_path)


test_plain_text_chapter_ann_parser()
