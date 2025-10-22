from openpecha.pecha import Pecha, get_anns, get_annotation_type
from openpecha.utils import read_json, convert_to_base_annotation
from pathlib import Path
from openpecha.pecha.layer import AnnotationType
from openpecha.ids import generate_id


def test_create_pecha():
    data = read_json("tests/pecha/data/ITEST001.json")
    annotation = [convert_to_base_annotation(ann) for ann in data["annotation"]]
    annotation_id = generate_id()
    pecha = Pecha.create_pecha(pecha_id=data["pecha_id"], base_text=data["base_text"], annotation_id=annotation_id, annotation=annotation)
    # 
    assert pecha.id == data["pecha_id"]

    base_name = list(pecha.bases.keys())[0]
    assert pecha.bases[base_name] == data["base_text"]

    ann_store, _ = pecha.get_layer_by_ann_type(base_name=base_name, layer_type=AnnotationType.ALIGNMENT)

    # ann_store is a list, we need to use the first AnnotationStore
    created_annotations = get_anns(ann_store[0] if isinstance(ann_store, list) else ann_store, include_span=True)

    assert len(created_annotations) == len(data["annotation"])

    first_created = created_annotations[0]

    first_original = data["annotation"][0]
    assert first_created["span"]["start"] == first_original["span"]["start"]
    assert first_created["span"]["end"] == first_original["span"]["end"]
    assert first_created.get("index") is None
    assert first_created["alignment_index"] == first_original["alignment_index"]
    
def test_add():
    data = read_json("tests/pecha/data/ITEST001_alignment.json")
    annotation = [convert_to_base_annotation(ann) for ann in data["annotation"]]
    pecha = Pecha.from_path(Path("tests/pecha/data/ITEST001"))

    base_name = next(iter(pecha.bases))
    annotation_id = generate_id()
    annotation_id = pecha.add(annotation_id=annotation_id, annotation=annotation, annotation_type="alignment")
    
    ann_store, _ = pecha.get_layer_by_ann_type(base_name=base_name, layer_type=AnnotationType.ALIGNMENT)
    
    created_annotations = get_anns(ann_store[0] if isinstance(ann_store, list) else ann_store, include_span=True)

    assert len(created_annotations) == len(data["annotation"])

    first_created = created_annotations[0]
    first_original = data["annotation"][0]
    assert first_created["span"]["start"] == first_original["span"]["start"]
    assert first_created["span"]["end"] == first_original["span"]["end"]
    assert first_created.get("index") is None
    assert first_created["alignment_index"] == first_original["alignment_index"]

    # Clean up - remove the added annotation layer to keep test data clean
    ann_type = get_annotation_type(annotation)
    annotation_layer_file = pecha.layer_path / base_name / f"{ann_type.value}-{annotation_id}.json"
    if annotation_layer_file.exists():
        annotation_layer_file.unlink()