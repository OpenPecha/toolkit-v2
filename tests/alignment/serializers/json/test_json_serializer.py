from pathlib import Path

from stam import AnnotationStore

from openpecha.alignment.alignment import Alignment
from openpecha.alignment.serializers.json import JSONSerializer
from openpecha.pecha import Pecha


def test_json_serializer():
    DATA = Path(__file__).parent / "data"

    alignment_path = DATA / "A7D77FF6C"

    alignment = Alignment.from_path(alignment_path)
    serializer = JSONSerializer(alignment)

    source_pecha = Pecha.from_path(DATA / "IFAAACD6C")
    target_pecha = Pecha.from_path(DATA / "IA88DADBA")

    source_ann_store, target_ann_store = serializer.load_pechas(
        source_pecha, target_pecha
    )
    assert isinstance(source_ann_store, AnnotationStore)
    assert isinstance(target_ann_store, AnnotationStore)

    expected_path = DATA / "expected_output"
    output_path = DATA / "output"
    serializer.serialize(output_path)

    assert (output_path / "root.json").exists()
    assert (output_path / "commentary.json").is_file()

    assert (output_path / "root.json").read_text(encoding="utf-8") == (
        expected_path / "root.json"
    ).read_text(encoding="utf-8")
    assert (output_path / "commentary.json").read_text(encoding="utf-8") == (
        expected_path / "commentary.json"
    ).read_text(encoding="utf-8")


test_json_serializer()
