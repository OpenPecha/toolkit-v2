from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.parsers.docx.update import DocxAnnotationUpdate
from openpecha.utils import read_json


class TestDocxAnnotationUpdate(TestCase):
    def setUp(self) -> None:
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/P2/IC7760088"
        )
        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_pecha.metadata.to_dict(),
        }

        self.root_pecha_backup = {
            f: f.read_bytes() for f in self.root_pecha_path.glob("**/*") if f.is_file()
        }

    def test_root_pecha(self):
        updater = DocxAnnotationUpdate()
        layer_path = "A389/Alignment-84EB.json"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_pecha_metadata]

        full_layer_path = self.root_pecha.layer_path / layer_path
        old_anns = get_anns(AnnotationStore(file=str(full_layer_path)))
        expected_old_anns = read_json(
            "tests/pecha/parser/docx/update/data/root/old_anns.json"
        )
        assert (
            old_anns == expected_old_anns
        ), "Old annotations do not match in Root Pecha Segmentation Layer Update"

        updater.update_annotation(self.root_pecha, layer_path, docx_file, metadatas)

        updated_anns = get_anns(AnnotationStore(file=str(full_layer_path)))
        expected_new_anns = read_json(
            "tests/pecha/parser/docx/update/data/root/new_anns.json"
        )
        assert (
            updated_anns == expected_new_anns
        ), "New annotations do not match in Root Pecha Segmentation Layer Update"

    def tearDown(self) -> None:
        # Revert all original files
        for f, content in self.root_pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.root_pecha_path.glob("**/*"):
            if f.is_file() and f not in self.root_pecha_backup:
                f.unlink()
