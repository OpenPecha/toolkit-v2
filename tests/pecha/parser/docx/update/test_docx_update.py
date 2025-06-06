from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import get_anns
from openpecha.pecha.parsers.docx.update import DocxAnnotationUpdate
from openpecha.utils import read_json
from tests.pecha import SharedPechaSetup


class TestDocxAnnotationUpdate(TestCase, SharedPechaSetup):
    def setUp(self) -> None:
        self.setup_pechas()

        self.root_pecha_backup = {
            f: f.read_bytes() for f in self.root_pecha_path.glob("**/*") if f.is_file()
        }
        self.commentary_pecha_backup = {
            f: f.read_bytes()
            for f in self.commentary_pecha_path.glob("**/*")
            if f.is_file()
        }

    def test_root_pecha(self):
        updater = DocxAnnotationUpdate()
        annotation_path = "B5FE/segmentation-4FD1.json"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_pecha_metadata]

        full_ann_path = self.root_pecha.layer_path / annotation_path
        old_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_old_anns = read_json(
            "tests/pecha/parser/docx/update/data/root/old_anns.json"
        )
        assert (
            old_anns == expected_old_anns
        ), "Old annotations do not match in Root Pecha Segmentation Layer Update"

        updater.update_annotation(
            self.root_pecha, annotation_path, docx_file, metadatas
        )

        updated_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_new_anns = read_json(
            "tests/pecha/parser/docx/update/data/root/new_anns.json"
        )
        assert (
            updated_anns == expected_new_anns
        ), "New annotations do not match in Root Pecha Segmentation Layer Update"

    def test_commentary_pecha(self):
        updater = DocxAnnotationUpdate()
        annotation_path = "B014/alignment-2127.json"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/commentary_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ _commentary segmentation 1.docx"
        )
        metadatas = [self.commentary_pecha_metadata, self.root_pecha_metadata]

        full_ann_path = self.commentary_pecha.layer_path / annotation_path
        old_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_old_anns = read_json(
            "tests/pecha/parser/docx/update/data/commentary/old_anns.json"
        )
        assert (
            old_anns == expected_old_anns
        ), "Old annotations do not match in Commentary Pecha Segmentation Layer Update"

        updater.update_annotation(
            self.commentary_pecha, annotation_path, docx_file, metadatas
        )

        updated_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_updated_anns = read_json(
            "tests/pecha/parser/docx/update/data/commentary/new_anns.json"
        )
        assert (
            updated_anns == expected_updated_anns
        ), "New annotations do not match in Commentary Pecha Segmentation Layer Update"

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
