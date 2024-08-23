import json
from pathlib import Path
from shutil import rmtree

from stam import AnnotationStore

from openpecha.alignment import Alignment
from openpecha.alignment.parsers.plaintext.plaintext import (
    PlainTextLineAlignedParser,
    split_text_into_lines,
)
from openpecha.pecha.layer import LayerCollectionEnum, LayerEnum, LayerGroupEnum


def test_plaintext_line_aligned_parser():
    DATA = Path(__file__).parent / "data"
    source_path = DATA / "root_segment.txt"
    target_path = DATA / "commentary.txt"
    metadata_path = DATA / "metadata.json"

    parser = PlainTextLineAlignedParser.from_files(
        source_path, target_path, metadata_path
    )

    with open(metadata_path, encoding="utf-8") as f:
        metadata = json.load(f)
    alignment_type = LayerCollectionEnum(metadata["metadata"]["type"])
    (source_ann_store, source_ann_store_name), (
        target_ann_store,
        target_ann_store_name,
    ) = parser.parse_pechas(dataset_id=alignment_type.value, output_path=DATA)

    assert isinstance(source_ann_store, AnnotationStore)
    assert isinstance(target_ann_store, AnnotationStore)

    source_lines = split_text_into_lines(source_path.read_text(encoding="utf-8"))
    target_lines = split_text_into_lines(target_path.read_text(encoding="utf-8"))

    """ comparing source lines"""
    dataset = list(source_ann_store.datasets())[0]

    source_key = dataset.key(LayerGroupEnum.structure_type.value)
    source_anns = list(
        dataset.data(source_key, value=LayerEnum.root_segment.value).annotations()
    )
    for annotation, source_line in zip(source_anns, source_lines):
        assert str(annotation) == source_line

    """ comparing target text lines"""
    dataset = list(target_ann_store.datasets())[0]

    target_key = dataset.key(LayerGroupEnum.structure_type.value)
    target_anns = list(
        dataset.data(target_key, value=LayerEnum.commentary.value).annotations()
    )
    for annotation, target_line in zip(target_anns, target_lines):
        assert str(annotation) == target_line

    """ alignment """
    parser.source_ann_store = source_ann_store
    parser.target_ann_store = target_ann_store

    alignment = parser.create_alignment(source_ann_store_name, target_ann_store_name)
    if alignment:
        alignment.write(output_path=DATA)
    assert isinstance(alignment, Alignment)

    """ clean up """
    rmtree(Path(DATA / source_ann_store.id()))
    rmtree(Path(DATA / target_ann_store.id()))
    rmtree(Path(DATA / alignment.id_))


test_plaintext_line_aligned_parser()
