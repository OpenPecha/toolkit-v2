from pathlib import Path
from unittest import TestCase, mock

from openpecha.pecha import Pecha, get_pecha_alignment_data


class TestGetPechaAlignment(TestCase):
    def setUp(self):
        data_dir = Path(__file__).parent / "data"
        self.root_pecha = Pecha.from_path(data_dir / "root_pecha/IB42962D2")
        self.commentary_pecha = Pecha.from_path(data_dir / "commentary_pecha/I07DE3474")
        self.translation_pecha = Pecha.from_path(
            data_dir / "translation_pecha/IC1743350"
        )
        self.version_pecha = Pecha.from_path(data_dir / "version_pecha/I07DE3475")

    def test_get_root_pecha_alignment_data(self):
        alignment_data = get_pecha_alignment_data(self.root_pecha)
        assert alignment_data is None

    @mock.patch("openpecha.pecha.get_pecha_with_id")
    def test_get_commentary_pecha_alignment_data(self, mock_get_pecha_with_id):
        mock_get_pecha_with_id.return_value = self.root_pecha
        alignment_data = get_pecha_alignment_data(self.commentary_pecha)
        expected_alignment_data = {
            "source": "IB42962D2/layers/F741/Tibetan_Segment-D792.json",
            "target": "I07DE3474/layers/C735/Meaning_Segment-5E94.json",
        }
        assert alignment_data == expected_alignment_data

    @mock.patch("openpecha.pecha.get_pecha_with_id")
    def test_get_translation_pecha_alignment_data(self, mock_get_pecha_with_id):
        mock_get_pecha_with_id.return_value = self.root_pecha
        alignment_data = get_pecha_alignment_data(self.translation_pecha)
        expected_alignment_data = {
            "source": "IB42962D2/layers/F741/Tibetan_Segment-D792.json",
            "target": "IC1743350/layers/ACEE/Meaning_Segment-8EEE.json",
        }
        assert alignment_data == expected_alignment_data

    @mock.patch("openpecha.pecha.get_pecha_with_id")
    def test_get_version_pecha_alignment_data(self, mock_get_pecha_with_id):
        mock_get_pecha_with_id.return_value = self.root_pecha
        alignment_data = get_pecha_alignment_data(self.version_pecha)
        expected_alignment_data = {
            "source": "IB42962D2/layers/F741/Tibetan_Segment-D792.json",
            "target": "I07DE3475/layers/C735/Meaning_Segment-5E94.json",
        }
        assert alignment_data == expected_alignment_data
