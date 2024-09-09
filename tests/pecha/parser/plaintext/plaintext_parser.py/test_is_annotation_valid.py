from openpecha.pecha.parsers.plaintext.plaintext_parser import PlainTextParser


def test_is_annotation_name_valid():
    assert (
        PlainTextParser.is_annotation_name_valid("Meaning_Segment") is True
    ), "Meaning_Segment should have been a valid annotation name"
    assert (
        PlainTextParser.is_annotation_name_valid("Chapter") is True
    ), "Chapter should have been a valid annotation name"
    assert (
        PlainTextParser.is_annotation_name_valid("Title") is False
    ), "Title should have been an invalid annotation name"
