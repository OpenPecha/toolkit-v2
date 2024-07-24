from pathlib import Path
from shutil import rmtree

from stam import AnnotationStore, TextResource

from openpecha.alignment import Alignment
from openpecha.alignment.parsers.plaintext import (
    PlainTextLineAlignedParser,
    split_text_into_lines,
)
from openpecha.ids import get_uuid
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum
from openpecha.pecha.metadata import PechaMetaData


def test_plaintext_line_aligned_parser():
    DATA = Path(__file__).parent / "data"
    source_path = DATA / "root_segment.txt"
    target_path = DATA / "commentary.txt"
    metadata_path = DATA / "metadata.json"

    parser = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata_path
    )
    dataset_id = f"root_commentary_{get_uuid()[:3]}"
    source_ann_store, target_ann_store = parser.parse_pechas(
        dataset_id=dataset_id, output_path=DATA
    )

    assert isinstance(source_ann_store, AnnotationStore)
    assert isinstance(target_ann_store, AnnotationStore)

    source_lines = split_text_into_lines(source_path.read_text(encoding="utf-8"))
    target_lines = split_text_into_lines(target_path.read_text(encoding="utf-8"))

    """ get source metadata"""
    dataset = list(source_ann_store.datasets())[0]

    metadata_key = dataset.key(LayerGroupEnum.resource_type.value)
    metadata_ann = list(
        dataset.data(metadata_key, value=LayerEnum.metadata.value).annotations()
    )[0]

    text_resource = metadata_ann.target().resource(source_ann_store)
    assert isinstance(text_resource, TextResource)
    metadata_obj = PechaMetaData.from_text(text_resource.text())
    assert isinstance(metadata_obj, PechaMetaData)

    """ comparing source lines"""
    source_key = dataset.key(LayerGroupEnum.structure_type.value)
    source_anns = list(
        dataset.data(source_key, value=LayerEnum.root_segment.value).annotations()
    )
    for annotation, source_line in zip(source_anns, source_lines):
        assert str(annotation) == source_line

    """ get source metadata"""
    dataset = list(target_ann_store.datasets())[0]
    metadata_key = dataset.key(LayerGroupEnum.resource_type.value)
    metadata_ann = list(
        dataset.data(metadata_key, value=LayerEnum.metadata.value).annotations()
    )[0]

    text_resource = metadata_ann.target().resource(target_ann_store)
    assert isinstance(text_resource, TextResource)
    metadata_obj = PechaMetaData.from_text(text_resource.text())
    assert isinstance(metadata_obj, PechaMetaData)

    """ comparing target text lines"""

    target_key = dataset.key(LayerGroupEnum.structure_type.value)
    target_anns = list(
        dataset.data(target_key, value=LayerEnum.comment.value).annotations()
    )
    for annotation, target_line in zip(target_anns, target_lines):
        assert str(annotation) == target_line

    """ alignmet """
    parser.source_ann_store = source_ann_store
    parser.target_ann_store = target_ann_store

    alignment = parser.create_alignment()
    if alignment:
        alignment.save(output_path=DATA)
    assert isinstance(alignment, Alignment)

    """ clean up """
    rmtree(Path(DATA / source_ann_store.id()))
    rmtree(Path(DATA / target_ann_store.id()))
    rmtree(Path(DATA / alignment.id_))


test_plaintext_line_aligned_parser()
