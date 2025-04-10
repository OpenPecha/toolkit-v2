from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
from openpecha.pecha.pecha_types import PechaType
from openpecha.utils import read_json


class TestDocxAnnotationParser(TestCase):
    def setUp(self):
        self.parser = DocxAnnotationParser()
        self.root_display_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P1/IA6E66F92"
        )
        self.root_display_pecha = Pecha.from_path(self.root_display_pecha_path)
        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
        }
        self.root_display_pecha_backup = {
            f: f.read_bytes()
            for f in self.root_display_pecha_path.glob("**/*")
            if f.is_file()
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

        layer_path = self.parser.add_annotation(
            self.root_display_pecha, ann_type, ann_title, docx_file, metadatas
        )

        new_anns = get_anns(AnnotationStore(file=str(layer_path)))
        layer_path.unlink()
        expected_new_anns = read_json(
            Path(
                "tests/pecha/parser/docx/annotation/data/root_display_pecha/expected_new_anns.json"
            )
        )

        metadata = self.root_display_pecha.metadata
        basename = list(metadata.bases.keys())[0]
        new_annotation_metadata = metadata.bases[basename]["source_metadata"][
            "annotations"
        ][layer_path.stem]

        expected_new_annotation_metadata = {
            "annotation_title": "དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1",
            "annotation_type": "Root_Segment",
        }

        assert new_anns == expected_new_anns
        assert new_annotation_metadata == expected_new_annotation_metadata

    def tearDown(self) -> None:
        # Revert all original files
        for f, content in self.root_display_pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.root_display_pecha_path.glob("**/*"):
            if f.is_file() and f not in self.root_display_pecha_backup:
                f.unlink()
