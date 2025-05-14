from openpecha.pecha.serializers.utils import find_related_pecha_id
from tests.pecha import SharedPechaSetup


def test_find_related_pecha_id():
    test_setup = SharedPechaSetup()
    test_setup.setup_pechas()

    # Test Root Pecha
    annotations = {
        test_setup.root_pecha.id: test_setup.root_pecha_annotations,
    }
    ann_path = test_setup.root_pecha_annotations[0].path
    assert find_related_pecha_id(annotations, ann_path) == test_setup.root_pecha.id

    # Test Root Translation Pecha
    annotations = {
        test_setup.root_translation_pecha.id: test_setup.root_translation_pecha_annotations,
        test_setup.root_pecha.id: test_setup.root_pecha_annotations,
    }
    ann_path = test_setup.root_translation_pecha_annotations[0].path
    assert (
        find_related_pecha_id(annotations, ann_path)
        == test_setup.root_translation_pecha.id
    )

    # Test Commentary Pecha
    annotations = {
        test_setup.commentary_pecha.id: test_setup.commentary_pecha_annotations,
        test_setup.root_pecha.id: test_setup.root_pecha_annotations,
    }
    ann_path = test_setup.commentary_pecha_annotations[0].path
    assert (
        find_related_pecha_id(annotations, ann_path) == test_setup.commentary_pecha.id
    )
