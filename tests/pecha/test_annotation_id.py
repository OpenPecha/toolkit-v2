from openpecha.ids import get_annotation_id


def test_get_annotation_id():
    ann_id = get_annotation_id()
    assert len(ann_id) == 8
