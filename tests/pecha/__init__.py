from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import LayerEnum


class SharedPechaSetup:
    def setup_pechas(self):
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/IA6E66F92"
        )
        self.root_translation_pecha_path = Path(
            "tests/pecha/serializers/pecha_db/root/data/en/I62E00D78"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/commentary/I77BD6EA9"
        )
        self.commentary_translation_pecha_path = Path(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/en/I94DBDA91"
        )

        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.root_translation_pecha = Pecha.from_path(self.root_translation_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)
        self.commentary_translation_pecha = Pecha.from_path(
            self.commentary_translation_pecha_path
        )

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
                    title="\u0f51\u0f44\u0f0b\u0f42\u0fb1\u0f72\u0f44\u0f0b\u0f54\u0f0b\u0f62\u0f66\u0f0b\u0f63\u0f0b\u0f66\u0f7c\u0f44\u0f0b\u0f62\u0f92\u0fb1\u0f72\u0f0b\u0f0d\u0f66\u0f7c\u0f44\u0f0b\u0f62\u0f92\u0fb1\u0f72\u0f0b\u0f0d segmentation",
                    aligned_to=None,
                ),
                AnnotationModel(
                    pecha_id="IA6E66F92",
                    type=LayerEnum.segmentation,
                    document_id="d2",
                    id="B8B3/Alignment-74F4.json",
                    title="\u0f51\u0f44\u0f0b\u0f42\u0fb1\u0f72\u0f44\u0f0b\u0f54\u0f0b\u0f62\u0f66\u0f0b\u0f63\u0f0b\u0f66\u0f7c\u0f44\u0f0b\u0f62\u0f92\u0fb1\u0f72\u0f0b\u0f0d\u0f66\u0f7c\u0f44\u0f0b\u0f62\u0f92\u0fb1\u0f72\u0f0b\u0f0d alignment",
                    aligned_to=None,
                ),
            ],
        }

        self.root_translation_pecha_metadata = {
            "translation_of": "IE60BBDE8",
            "commentary_of": None,
            "version_of": None,
            **self.root_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I62E00D78",
                    type=LayerEnum.alignment,
                    document_id="d3",
                    id="D93E/Alignment-0216.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }

        self.commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
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
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Segmentation-74F4.json"
                    ),
                )
            ],
        }

        self.commentary_translation_pecha_metadata = {
            "translation_of": "I6944984E",
            "commentary_of": None,
            "version_of": None,
            **self.commentary_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I94DBDA91",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="FD22/Alignment-599A.json",
                    title="\u0f51\u0f44\u0f0b\u0f42\u0fb1\u0f72\u0f44\u0f0b\u0f54\u0f0b\u0f62\u0f66\u0f0b\u0f63\u0f0b\u0f66\u0f7c\u0f44\u0f0b\u0f62\u0f92\u0fb1\u0f72\u0f0b\u0f0d\u0f66\u0f7c\u0f44\u0f0b\u0f62\u0f92\u0fb1\u0f72\u0f0b\u0f0d commentary",
                    aligned_to=PechaAlignment(
                        pecha_id="I6944984E", alignment_id="E949/Alignment-2F29.json"
                    ),
                )
            ],
        }

        self.prealigned_root_translation_pecha_metadata = {
            "translation_of": "IE60BBDE8",
            "commentary_of": None,
            "version_of": None,
            **self.root_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I62E00D78",
                    type=LayerEnum.alignment,
                    document_id="d3",
                    id="D93E/Alignment-0216.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                    aligned_to=PechaAlignment(
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Alignment-F81A.json"
                    ),
                )
            ],
        }

        self.prealigned_commentary_pecha_metadata = {
            "translation_of": None,
            "commentary_of": "IE60BBDE8",
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
                        pecha_id="IE60BBDE8", alignment_id="B8B3/Alignment-F81A.json"
                    ),
                )
            ],
        }

        self.prealigned_commentary_translation_pecha_metadata = {
            "translation_of": "I6944984E",
            "commentary_of": None,
            "version_of": None,
            **self.commentary_translation_pecha.metadata.to_dict(),
            "annotations": [
                AnnotationModel(
                    pecha_id="I94DBDA91",
                    type=LayerEnum.alignment,
                    document_id="d4",
                    id="FD22/Alignment-599A.json",
                    title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary translation",
                    aligned_to=PechaAlignment(
                        pecha_id="I6944984E", alignment_id="E949/Alignment-2F29.json"
                    ),
                )
            ],
        }
