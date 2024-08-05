from pathlib import Path

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


test_plain_text_chapter_ann_parser()
