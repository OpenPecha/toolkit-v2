from pathlib import Path
from shutil import rmtree

from stam import AnnotationStore

from openpecha.alignment import Alignment
from openpecha.alignment.parsers.plaintext.line_align import (
    PlainTextLineAlignedParser,
    split_text_into_lines,
)
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum


def test_plaintext_line_aligned_parser():
    DATA = Path(__file__).parent / "data"
    source_path = DATA / "root_segment.txt"
    target_path = DATA / "commentary.txt"
    metadata_path = DATA / "metadata.json"

    parser = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata_path
    )

    (source_layer, source_layer_name), (
        target_layer,
        target_layer_name,
    ) = parser.parse_pechas(output_path=DATA)

    assert isinstance(source_layer, AnnotationStore)
    assert isinstance(target_layer, AnnotationStore)

    source_lines = split_text_into_lines(source_path.read_text(encoding="utf-8"))
    target_lines = split_text_into_lines(target_path.read_text(encoding="utf-8"))

    """ comparing source lines"""
    dataset = list(source_layer.datasets())[0]

    source_key = dataset.key(LayerGroupEnum.associated_alignment.value)
    source_anns = list(
        dataset.data(source_key, value=LayerEnum.root_segment.value).annotations()
    )
    for annotation, source_line in zip(source_anns, source_lines):
        assert str(annotation) == source_line

    """ comparing target text lines"""
    dataset = list(target_layer.datasets())[0]

    target_key = dataset.key(LayerGroupEnum.associated_alignment.value)
    target_anns = list(
        dataset.data(target_key, value=LayerEnum.commentary_segment.value).annotations()
    )
    for annotation, target_line in zip(target_anns, target_lines):
        assert str(annotation) == target_line

    """ alignment """
    parser.source_layer = source_layer
    parser.target_layer = target_layer

    alignment = parser.create_alignment(source_layer_name, target_layer_name)
    if alignment:
        alignment.write(output_path=DATA)
    assert isinstance(alignment, Alignment)

    """ clean up """
    rmtree(Path(DATA / source_layer.id()))
    rmtree(Path(DATA / target_layer.id()))
    rmtree(Path(DATA / alignment.id))


test_plaintext_line_aligned_parser()
