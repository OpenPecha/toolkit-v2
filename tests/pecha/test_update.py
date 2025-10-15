from openpecha.pecha import Pecha
from pathlib import Path
from openpecha.utils import read_json, convert_to_base_annotation
import subprocess
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha import get_anns



pecha = Pecha.from_path(Path(f"tests/pecha/update/data/ID8Sv2ynVKZX8wIt"))
annotation_id = "Tm3Uewnh3ySsvgIE"
annotation = [convert_to_base_annotation(ann) for ann in read_json("tests/pecha/update/data/updated_segmentation.json")]
layer_type = AnnotationType.SEGMENTATION


def test_update_annotation():
    updated_pecha = pecha.update_annotation(annotation_id=annotation_id, annotation=annotation, layer_type=layer_type)
    assert updated_pecha.id == pecha.id
    base_name = list(pecha.bases.keys())[0]
    ann_store, _ = pecha.get_layer_by_ann_type(base_name=base_name, layer_type=layer_type)

    created_annotations = get_anns(ann_store[0] if isinstance(ann_store, list) else ann_store, include_span=True)

    assert len(created_annotations) == len(annotation)
    subprocess.run("rm -rf tests/pecha/update/data/ID8Sv2ynVKZX8wIt", shell=True)
    subprocess.run("cp -r tests/pecha/serializers/json/data/ID8Sv2ynVKZX8wIt tests/pecha/update/data/ID8Sv2ynVKZX8wIt", shell=True)