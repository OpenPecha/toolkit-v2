from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
from openpecha.utils import read_json


class TestDocxAnnotationParser(TestCase):
    def setUp(self):
        self.parser = DocxAnnotationParser()
        self.root_display_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P1/IA6E66F92"
        )
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P2/IC7760088"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P3/I77BD6EA9"
        )

        self.root_display_pecha = Pecha.from_path(self.root_display_pecha_path)
        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)

        self.root_display_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_display_pecha.metadata.to_dict(),
        }
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": self.root_display_pecha.id,
            **self.root_pecha.metadata.to_dict(),
        }
        self.commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": self.root_pecha.id,
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
        }

        self.root_display_pecha_backup = {
            f: f.read_bytes()
            for f in self.root_display_pecha_path.glob("**/*")
            if f.is_file()
        }
        self.commentary_pecha_backup = {
            f: f.read_bytes()
            for f in self.commentary_pecha_path.glob("**/*")
            if f.is_file()
        }

    def test_root_pecha(self):
        type = LayerEnum.alignment
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_display_pecha_metadata]

        pecha, annotation_path = self.parser.add_annotation(
            self.root_display_pecha, type, docx_file, metadatas
        )
        layer_path = pecha.layer_path / annotation_path
        new_anns = get_anns(AnnotationStore(file=str(layer_path)))
        expected_new_anns = read_json(
            Path(
                "tests/pecha/parser/docx/annotation/data/root_display_pecha/expected_new_anns.json"
            )
        )

        assert new_anns == expected_new_anns

    def test_commentary_pecha(self):
        type = LayerEnum.alignment
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/commentary_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ _commentary segmentation 1.docx"
        )
        metadatas = [
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
            self.root_display_pecha_metadata,
        ]

        parent_layer_path = next(self.root_pecha.layer_path.rglob("*.json"))
        parent_layer_path = str(
            parent_layer_path.relative_to(self.root_pecha.pecha_path.parent)
        )
        pecha, annotation_path = self.parser.add_annotation(
            self.commentary_pecha,
            type,
            docx_file,
            metadatas,
        )
        layer_path = pecha.layer_path / annotation_path

        new_anns = get_anns(AnnotationStore(file=str(layer_path)))
        expected_new_anns = read_json(
            Path(
                "tests/pecha/parser/docx/annotation/data/commentary_pecha/expected_new_anns.json"
            )
        )

        assert new_anns == expected_new_anns

    def tearDown(self) -> None:
        # Revert all original files
        for f, content in self.root_display_pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.root_display_pecha_path.glob("**/*"):
            if f.is_file() and f not in self.root_display_pecha_backup:
                f.unlink()

        # Revert all original files
        for f, content in self.commentary_pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.commentary_pecha_path.glob("**/*"):
            if f.is_file() and f not in self.commentary_pecha_backup:
                f.unlink()
