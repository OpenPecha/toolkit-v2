from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers.docx.update import DocxAnnotationUpdate
from openpecha.utils import read_json


class TestDocxAnnotationUpdate(TestCase):
    def setUp(self) -> None:
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/IA6E66F92"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/commentary/I77BD6EA9"
        )

        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)

        self.root_pecha_metadata = {
            "translation_of": None,
            "commentary_of": None,
            "version_of": None,
            **self.root_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="IA6E66F92",
                    type=LayerEnum.segmentation,
                    document_id="d2",
                    id="B8B3/Segmentation-74F4.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation",
                    aligned_to=None,
                ),
                AnnotationModel(
                    pecha_id="IA6E66F92",
                    type=LayerEnum.segmentation,
                    document_id="d2",
                    id="B8B3/Alignment-F81A.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ alignment",
                    aligned_to=None,
                ),
            ],
        }
        self.commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": self.root_pecha.id,
            "version_of": None,
            **self.commentary_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I6944984E",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="E949/Alignment-2F29.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="IA6E66F92", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }

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
        annotation_id = "B8B3/Segmentation-74F4.json"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/root_display_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation 1.docx"
        )
        metadatas = [self.root_pecha_metadata]

        full_ann_path = self.root_pecha.layer_path / annotation_id
        old_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_old_anns = read_json(
            "tests/pecha/parser/docx/update/data/root/old_anns.json"
        )
        assert (
            old_anns == expected_old_anns
        ), "Old annotations do not match in Root Pecha Segmentation Layer Update"

        updater.update_annotation(self.root_pecha, annotation_id, docx_file, metadatas)

        updated_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_new_anns = read_json(
            "tests/pecha/parser/docx/update/data/root/new_anns.json"
        )
        assert (
            updated_anns == expected_new_anns
        ), "New annotations do not match in Root Pecha Segmentation Layer Update"

    def test_commentary_pecha(self):
        updater = DocxAnnotationUpdate()
        annotation_id = "BEC3/Alignment-90C0.json"
        docx_file = Path(
            "tests/pecha/parser/docx/annotation/data/commentary_pecha/དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ _commentary segmentation 1.docx"
        )
        metadatas = [self.commentary_pecha_metadata, self.root_pecha_metadata]

        full_ann_path = self.commentary_pecha.layer_path / annotation_id
        old_anns = get_anns(AnnotationStore(file=str(full_ann_path)))
        expected_old_anns = read_json(
            "tests/pecha/parser/docx/update/data/commentary/old_anns.json"
        )
        assert (
            old_anns == expected_old_anns
        ), "Old annotations do not match in Commentary Pecha Segmentation Layer Update"

        updater.update_annotation(
            self.commentary_pecha, annotation_id, docx_file, metadatas
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
