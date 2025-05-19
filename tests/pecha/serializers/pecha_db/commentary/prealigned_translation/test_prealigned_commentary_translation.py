from unittest import TestCase

from openpecha.pecha.serializers.pecha_db.commentary.prealigned_commentary_translation import (
    PreAlignedCommentaryTranslationSerializer,
)
from tests.pecha import SharedPechaSetup


class TestPreAlignedCommentaryTranslationSerializer(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

    def test_prealigned_commentary_translation_pecha(self):
        serializer = PreAlignedCommentaryTranslationSerializer()  # noqa
        pass
