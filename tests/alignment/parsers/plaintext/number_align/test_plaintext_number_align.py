from pathlib import Path

from openpecha.alignment.parsers.plaintext.number_align import (
    PlainTextNumberAlignedParser,
)


def test_plaintext_number_align():
    DATA = Path(__file__).parent / "data"

    root_file = DATA / "003-ch.txt"
    align_file = DATA / "004-ch-1-諦閑.txt"
    metadata_file = DATA / "metadata.json"

    parser = PlainTextNumberAlignedParser.from_files(
        root_file, align_file, metadata_file
    )
    parser.parse_text_into_segment_pairs()


test_plaintext_number_align()
