from unittest import TestCase

from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
from openpecha.pecha.pecha_types import PechaType


class TestDocxAnnotationParser(TestCase):
    def setUp(self):
        self.parser = DocxAnnotationParser()

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
