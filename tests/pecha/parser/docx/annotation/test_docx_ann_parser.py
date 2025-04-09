from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
from openpecha.pecha.pecha_types import PechaType


class TestDocxAnnotationParser(TestCase):
    def setUp(self):
        self.parser = DocxAnnotationParser()
        self.root_display_pecha = Pecha.from_path(
            Path("tests/alignment/commentary_transfer/data/P1/IA6E66F92")
        )
        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
        }

    def test_is_root_related_pecha(self):
        # Test root pecha types
        assert self.parser.is_root_related_pecha(PechaType.root_pecha)
        assert self.parser.is_root_related_pecha(
            PechaType.prealigned_root_translation_pecha
        )

        # Test non-root pecha types
        assert not self.parser.is_root_related_pecha(PechaType.commentary_pecha)
        assert not self.parser.is_root_related_pecha(
            PechaType.prealigned_commentary_pecha
        )

    def test_is_commentary_related_pecha(self):
        # Test commentary pecha types
        assert self.parser.is_commentary_related_pecha(PechaType.commentary_pecha)
        assert self.parser.is_commentary_related_pecha(
            PechaType.prealigned_commentary_pecha
        )

        # Test non-commentary pecha types
        assert not self.parser.is_commentary_related_pecha(PechaType.root_pecha)
        assert not self.parser.is_commentary_related_pecha(
            PechaType.prealigned_root_translation_pecha
        )

    def test_root_pecha(self):
        ann_type = LayerEnum.root_segment
        ann_title = "དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_display_pecha_metadata]

        self.parser.add_annotation(
            self.root_display_pecha, ann_type, ann_title, docx_file, metadatas
        )


work = TestDocxAnnotationParser()
work.setUp()
work.test_root_pecha()
