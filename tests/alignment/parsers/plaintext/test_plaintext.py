from pathlib import Path
from shutil import rmtree

from stam import AnnotationStore

from openpecha.alignment.parsers.plaintext import (
    PlainTextLineAlignedParser,
    split_text_into_lines,
)


def test_plaintext_line_aligned_parser():
    DATA = Path(__file__).parent / "data"
    source_path = DATA / "root_segment.txt"
    target_path = DATA / "commentary.txt"
    metadata_path = DATA / "metadata.json"

    parser = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata_path
    )
    source_ann_store, target_ann_store = parser.parse(output_path=DATA)

    assert isinstance(source_ann_store, AnnotationStore)
    assert isinstance(target_ann_store, AnnotationStore)

    source_lines = split_text_into_lines(source_path.read_text(encoding="utf-8"))
    target_lines = split_text_into_lines(target_path.read_text(encoding="utf-8"))

    for annotation, source_line in zip(source_ann_store.annotations(), source_lines):
        assert str(annotation) == source_line

    for annotation, target_line in zip(target_ann_store.annotations(), target_lines):
        assert str(annotation) == target_line

    """ clean up """
    rmtree(Path(DATA / source_ann_store.id()))
    rmtree(Path(DATA / target_ann_store.id()))


test_plaintext_line_aligned_parser()
