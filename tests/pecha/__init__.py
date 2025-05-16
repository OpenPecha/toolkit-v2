from pathlib import Path
from typing import Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import AnnotationType


class DummyMetadataModel:
    def __init__(self, **args):
        for k, v in args.items():
            setattr(self, k, v)


null = None


class SharedPechaSetup:
    def setup_pechas(self):
        self.pecha_category: List[Dict] = [
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Madhyamaka", "bo": "དབུ་མ།", "lzh": "中观"},
                "parent": null,
            },
            {
                "description": null,
                "short_description": null,
                "name": {
                    "en": "Madhyamaka treatises",
                    "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།",
                    "lzh": "中观论著",
                },
                "parent": "madhyamaka",
            },
        ]

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

        self.root_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": None,
                "commentary_of": None,
                **self.root_pecha.metadata.to_dict(),
            }
        )
        self.root_pecha_annotations = [
            AnnotationModel(
                pecha_id="IA6E66F92",
                type=AnnotationType.SEGMENTATION,
                document_id="d2",
                path="B8B3/segmentation-74F4.json",
                title="དབུ་མ་འཇུག་པ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation",
                aligned_to=None,
            ),
            AnnotationModel(
                pecha_id="IA6E66F92",
                type=AnnotationType.ALIGNMENT,
                document_id="d2",
                path="B8B3/alignment-74F4.json",
                title="དབུ་མ་འཇུག་པ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ alignment",
                aligned_to=None,
            ),
        ]

        self.root_translation_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": "IE60BBDE8",
                "commentary_of": None,
                **self.root_translation_pecha.metadata.to_dict(),
            }
        )
        self.root_translation_pecha_annotations = [
            AnnotationModel(
                pecha_id="I62E00D78",
                type=AnnotationType.ALIGNMENT,
                document_id="d3",
                path="D93E/alignment-0216.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                aligned_to=PechaAlignment(
                    pecha_id="IE60BBDE8", alignment_id="B8B3/segmentation-74F4.json"
                ),
            )
        ]

        self.commentary_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": None,
                "commentary_of": "IE60BBDE8",
                **self.commentary_pecha.metadata.to_dict(),
            }
        )
        self.commentary_pecha_annotations = [
            AnnotationModel(
                pecha_id="I6944984E",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="BEC3/alignment-90C0.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                aligned_to=PechaAlignment(
                    pecha_id="IE60BBDE8", alignment_id="B8B3/segmentation-74F4.json"
                ),
            )
        ]

        self.commentary_translation_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": "I6944984E",
                "commentary_of": None,
                **self.commentary_translation_pecha.metadata.to_dict(),
            }
        )
        self.commentary_translation_pecha_annotations = [
            AnnotationModel(
                pecha_id="I94DBDA91",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="FD22/alignment-599A.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤  commentary",
                aligned_to=PechaAlignment(
                    pecha_id="I6944984E", alignment_id="BEC3/alignment-90C0.json"
                ),
            )
        ]

        self.prealigned_root_translation_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": "IE60BBDE8",
                "commentary_of": None,
                **self.root_translation_pecha.metadata.to_dict(),
            }
        )
        self.prealigned_root_translation_pecha_annotations = [
            AnnotationModel(
                pecha_id="I62E00D78",
                type=AnnotationType.ALIGNMENT,
                document_id="d3",
                path="D93E/alignment-0216.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                aligned_to=PechaAlignment(
                    pecha_id="IE60BBDE8", alignment_id="B8B3/alignment-F81A.json"
                ),
            )
        ]

        self.prealigned_root_translation_segmentation_pecha_metadata = (
            DummyMetadataModel(
                **{
                    "translation_of": "IE60BBDE8",
                    "commentary_of": None,
                    **self.root_translation_pecha.metadata.to_dict(),
                }
            )
        )
        self.prealigned_root_translation_segmentation_pecha_annotations = [
            AnnotationModel(
                pecha_id="I62E00D78",
                type=AnnotationType.SEGMENTATION,
                document_id="d3",
                path="D93E/segmentation-2143.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation",
                aligned_to=PechaAlignment(pecha_id="IE60BBDE8", alignment_id=None),
            ),
            AnnotationModel(
                pecha_id="I62E00D78",
                type=AnnotationType.ALIGNMENT,
                document_id="d3",
                path="D93E/alignment-0216.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ translation 1",
                aligned_to=PechaAlignment(
                    pecha_id="IE60BBDE8", alignment_id="B8B3/alignment-F81A.json"
                ),
            ),
        ]

        self.prealigned_commentary_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": None,
                "commentary_of": "IE60BBDE8",
                **self.commentary_pecha.metadata.to_dict(),
            }
        )
        self.prealigned_commentary_pecha_annotations = [
            AnnotationModel(
                pecha_id="I6944984E",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="E949/alignment-2F29.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                aligned_to=PechaAlignment(
                    pecha_id="IE60BBDE8", alignment_id="B8B3/alignment-F81A.json"
                ),
            )
        ]

        self.prealigned_commentary_segmentation_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": None,
                "commentary_of": "IE60BBDE8",
                **self.commentary_pecha.metadata.to_dict(),
            }
        )
        self.prealigned_commentary_segmentation_pecha_annotations = [
            AnnotationModel(
                pecha_id="I6944984E",
                type=AnnotationType.SEGMENTATION,
                document_id="d4",
                path="E949/segmentation-2134.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                aligned_to=PechaAlignment(pecha_id="IE60BBDE8", alignment_id=None),
            ),
            AnnotationModel(
                pecha_id="I6944984E",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="E949/alignment-2F29.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary",
                aligned_to=PechaAlignment(
                    pecha_id="IE60BBDE8", alignment_id="B8B3/alignment-F81A.json"
                ),
            ),
        ]

        self.prealigned_commentary_translation_pecha_metadata = DummyMetadataModel(
            **{
                "translation_of": "I6944984E",
                "commentary_of": None,
                **self.commentary_translation_pecha.metadata.to_dict(),
            }
        )
        self.prealigned_commentary_translation_pecha_annotations = [
            AnnotationModel(
                pecha_id="I94DBDA91",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="FD22/alignment-599A.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary translation",
                aligned_to=PechaAlignment(
                    pecha_id="I6944984E", alignment_id="E949/alignment-2F29.json"
                ),
            )
        ]
