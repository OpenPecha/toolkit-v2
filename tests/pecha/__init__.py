from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel, PechaAlignment
from openpecha.pecha.layer import AnnotationType


class DummyMetadataModel:
    def __init__(self, **args):
        for k, v in args.items():
            setattr(self, k, v)


class SharedPechaSetup:
    def setup_pechas(self):
        self.root_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/I6556B464"
        )
        self.root_translation_pecha_path = Path(
            "tests/pecha/serializers/pecha_db/root/data/en/I5003D420"
        )
        self.commentary_pecha_path = Path(
            "tests/alignment/commentary_transfer/data/commentary/I015AFFA7"
        )
        self.commentary_translation_pecha_path = Path(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/en/ICFCF1CDC"
        )
        self.prealigned_commentary_translation_pecha_path = Path(
            "tests/pecha/serializers/pecha_db/commentary/prealigned_translation/data/en/IF5944957"
        )

        self.root_pecha = Pecha.from_path(self.root_pecha_path)
        self.root_translation_pecha = Pecha.from_path(self.root_translation_pecha_path)
        self.commentary_pecha = Pecha.from_path(self.commentary_pecha_path)
        self.commentary_translation_pecha = Pecha.from_path(
            self.commentary_translation_pecha_path
        )
        self.prealigned_commentary_translation_pecha = Pecha.from_path(
            self.prealigned_commentary_translation_pecha_path
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
                pecha_id="I6556B464",
                type=AnnotationType.SEGMENTATION,
                document_id="d2",
                path="B5FE/segmentation-4FD1.json",
                title="དབུ་མ་འཇུག་པ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ segmentation",
                aligned_to=None,
            ),
            AnnotationModel(
                pecha_id="I6556B464",
                type=AnnotationType.ALIGNMENT,
                document_id="d2",
                path="B5FE/alignment-6707.json",
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
                pecha_id="I5003D420",
                type=AnnotationType.ALIGNMENT,
                document_id="d3",
                path="9813/alignment-AE0B.json",
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
                pecha_id="I015AFFA7",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="B014/alignment-2127.json",
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
                pecha_id="ICFCF1CDC",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="EB60/alignment-6786.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤  commentary",
                aligned_to=PechaAlignment(
                    pecha_id="I015AFFA7", alignment_id="B014/alignment-2127.json"
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
                **self.prealigned_commentary_translation_pecha.metadata.to_dict(),
            }
        )
        self.prealigned_commentary_translation_pecha_annotations = [
            AnnotationModel(
                pecha_id="IF5944957",
                type=AnnotationType.ALIGNMENT,
                document_id="d4",
                path="0DCE/alignment-8B56.json",
                title="དགོངས་པ་རབ་གསལ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ commentary translation",
                aligned_to=PechaAlignment(
                    pecha_id="I6944984E", alignment_id="E949/alignment-2F29.json"
                ),
            )
        ]
