from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import get_anns
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
from openpecha.utils import read_json
from tests.pecha import SharedPechaSetup


class TestDocxAnnotationParser(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.parser = DocxAnnotationParser()
        self.root_pecha_backup = {
            f: f.read_bytes() for f in self.root_pecha_path.glob("**/*") if f.is_file()
        }
        self.commentary_pecha_backup = {
            f: f.read_bytes()
            for f in self.commentary_pecha_path.glob("**/*")
            if f.is_file()
        }

    def test_root_pecha(self):
        type = LayerEnum.ALIGNMENT
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_pecha_metadata]

        pecha, layer_name = self.parser.add_annotation(
            self.root_pecha, type, docx_file, metadatas
        )
        layer_path = pecha.layer_path / layer_name
        new_anns = get_anns(AnnotationStore(file=str(layer_path)))
        expected_new_anns = read_json(
            Path(
                "tests/pecha/parser/docx/annotation/data/root_display_pecha/expected_new_anns.json"
            )
        )

        assert new_anns == expected_new_anns

    def test_commentary_pecha(self):
        type = LayerEnum.ALIGNMENT
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/commentary_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ _commentary segmentation 1.docx"
        )
        metadatas = [
            self.commentary_pecha_metadata,
            self.root_pecha_metadata,
        ]

        pecha, layer_name = self.parser.add_annotation(
            self.commentary_pecha,
            type,
            docx_file,
            metadatas,
        )
        layer_path = pecha.layer_path / layer_name

        new_anns = get_anns(AnnotationStore(file=str(layer_path)))
        expected_new_anns = read_json(
            Path(
                "tests/pecha/parser/docx/annotation/data/commentary_pecha/expected_new_anns.json"
            )
        )

        assert new_anns == expected_new_anns

    def tearDown(self) -> None:
        # Revert all original files
        for f, content in self.root_pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.root_pecha_path.glob("**/*"):
            if f.is_file() and f not in self.root_pecha_backup:
                f.unlink()

        # Revert all original files
        for f, content in self.commentary_pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.commentary_pecha_path.glob("**/*"):
            if f.is_file() and f not in self.commentary_pecha_backup:
                f.unlink()
