from pathlib import Path
from unittest import TestCase

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.annotations import (
    SegmentationAnnotation,
    Span,
    SpellingVariantAnnotation,
)
from openpecha.pecha.parsers.edition import EditionParser


class TestEditionParser(TestCase):
    def setUp(self):
        self.DATA = Path(__file__).parent / "data"
        self.txt_file = self.DATA / "edition.txt"

        self.pecha_path = Path(
            "tests/alignment/commentary_transfer/data/root/I6556B464"
        )
        self.pecha = Pecha.from_path(self.pecha_path)

        self.pecha_backup = {
            f: f.read_bytes() for f in self.pecha_path.glob("**/*") if f.is_file()
        }

    def test_segmentation_parse(self):
        parser = EditionParser()
        segments = self.txt_file.read_text(encoding="utf-8").splitlines()
        anns = parser.parse_segmentation(segments)

        expected_anns = [
            SegmentationAnnotation(span=Span(start=0, end=87), index=1),
            SegmentationAnnotation(span=Span(start=88, end=207), index=2),
            SegmentationAnnotation(span=Span(start=208, end=283), index=3),
            SegmentationAnnotation(span=Span(start=284, end=361), index=4),
            SegmentationAnnotation(span=Span(start=362, end=508), index=5),
            SegmentationAnnotation(span=Span(start=509, end=844), index=6),
            SegmentationAnnotation(span=Span(start=845, end=1129), index=7),
            SegmentationAnnotation(span=Span(start=1130, end=1217), index=8),
            SegmentationAnnotation(span=Span(start=1218, end=1409), index=9),
            SegmentationAnnotation(span=Span(start=1410, end=1605), index=10),
        ]

        assert anns == expected_anns

    def test_spelling_variant_parse(self):
        parser = EditionParser()

        # Insertion
        old_base = "Hello"
        new_base = "Hello World"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(
                span=Span(start=5, end=5), operation="insertion", text=" World"
            )
        ]

        # Deletion
        old_base = "Hello World"
        new_base = "Hello"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(span=Span(start=5, end=11), operation="deletion")
        ]

        # Insertion in Between
        old_base = "Hello World"
        new_base = "Hello!! World"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(
                span=Span(start=5, end=5), operation="insertion", text="!!"
            )
        ]

        # Deletion in Between
        old_base = "Good morning, Everyone"
        new_base = "Good Everyone"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(span=Span(start=4, end=13), operation="deletion")
        ]

        # Insertion and Deletion
        old_base = "Good morning, Ladies and Gentlemen"
        new_base = "Good Attractive Ladies and Gentlemen"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(span=Span(start=5, end=13), operation="deletion"),
            SpellingVariantAnnotation(
                span=Span(start=13, end=13), operation="insertion", text="Attractive"
            ),
        ]

        # Test with google docs
        old_basename = list(self.pecha.bases.keys())[0]
        old_base = self.pecha.get_base(old_basename)

        segments = self.txt_file.read_text(encoding="utf-8").splitlines()
        new_base = "\n".join(segments)
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(
                span=Span(start=87, end=87, errors=None),
                metadata=None,
                operation="insertion",
                text="\n",
            ),
            SpellingVariantAnnotation(
                span=Span(start=282, end=282, errors=None),
                metadata=None,
                operation="insertion",
                text="\n",
            ),
            SpellingVariantAnnotation(
                span=Span(start=673, end=674, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=888, end=888, errors=None),
                metadata=None,
                operation="insertion",
                text=" རྟག་ཏུ་ཚུལ་ཁྲིམས་ཡང་དག་བླངས་ནས་གནས་པར་འགྱུར།",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1034, end=1080, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1080, end=1080, errors=None),
                metadata=None,
                operation="insertion",
                text="འགྲོ་བ་དགྲོལ་བར་བྱ་ཕྱིར་ཡོངས་སུ་བསྔོ་བྱེད་ཅིང༌",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1083, end=1083, errors=None),
                metadata=None,
                operation="insertion",
                text="\n",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1170, end=1213, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1279, end=1279, errors=None),
                metadata=None,
                operation="insertion",
                text="པར་",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1322, end=1323, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1323, end=1323, errors=None),
                metadata=None,
                operation="insertion",
                text="བ",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1441, end=1444, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1497, end=1500, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1573, end=1585, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
            SpellingVariantAnnotation(
                span=Span(start=1616, end=1617, errors=None),
                metadata=None,
                operation="deletion",
                text="",
            ),
        ]

    def test_parse(self):
        parser = EditionParser()

        segments = self.txt_file.read_text(encoding="utf-8").splitlines()
        seg_layer_path, spelling_variant_path = parser.parse(self.pecha, segments)

        seg_anns = get_anns(
            ann_store=AnnotationStore(file=str(self.pecha.layer_path / seg_layer_path)),
            include_span=True,
        )
        expected_seg_anns = [
            {
                "index": 1,
                "segmentation_type": "segmentation",
                "text": "བུ་མ་འཇུག་པ་ལས་སེམས་བསྐྱེད་དྲུག་པ། ཤོ་ལོ་ཀ ༡-༦༤ མངོན་དུ་ཕྱོགས་པར་མཉམ་བཞག་སེམས་གནས་ཏེ། །",
                "Span": {"start": 0, "end": 87},
            },
            {
                "index": 2,
                "segmentation_type": "segmentation",
                "text": "ྫོགས་པའི་སངས་རྒྱས་ཆོས་ལ་མངོན་ཕྱོགས་ཤིང༌། །འདི་བརྟེན་འབྱུང་བའི་དེ་ཉིད་མཐོང་བ་དེས། །ཤེས་རབ་གནས་པས་འགོག་པ་ཐོབ་པར་འགྱུར། །",
                "Span": {"start": 88, "end": 206},
            },
            {
                "index": 3,
                "segmentation_type": "segmentation",
                "text": "ཇི་ལྟར་ལོང་བའི་ཚོགས་ཀུན་བདེ་བླག་ཏུ། །མིག་ལྡན་སྐྱེས་བུ་གཅིག་གིས་འདོད་པ་ཡི། །",
                "Span": {"start": 207, "end": 282},
            },
            {
                "index": 4,
                "segmentation_type": "segmentation",
                "text": "ུལ་དུ་འཁྲིད་པ་དེ་བཞིན་འདིར་ཡང་བློས། །མིག་ཉམས་ཡོན་ཏན་བླངས་ཏེ་རྒྱལ་ཉིད་འགྲོ། །",
                "Span": {"start": 283, "end": 359},
            },
            {
                "index": 5,
                "segmentation_type": "segmentation",
                "text": "ཇི་ལྟར་དེ་ཡིས་ཆེས་ཟབ་ཆོས་རྟོགས་པ། །ལུང་དང་གཞན་ཡང་རིགས་པས་ཡིན་པས་ན། །དེ་ལྟར་འཕགས་པ་ཀླུ་སྒྲུབ་གཞུང་ལུགས་ལས། །ཇི་ལྟར་གནས་པའི་ལུགས་བཞིན་བརྗོད་པར་བྱ། ",
                "Span": {"start": 360, "end": 505},
            },
            {
                "index": 6,
                "segmentation_type": "segmentation",
                "text": "\nསོ་སོ་སྐྱེ་བོའི་དུས་ནའང་སྟོང་པ་ཉིད་ཐོས་ནས། །ནང་དུ་རབ་ཏུ་དགའ་བ་ཡང་དང་ཡང་དུ་འབྱུང༌། །རབ་ཏུ་དགའ་བ་ལས་བྱུང་མཆི་མས་མིག་བརླན་ཞིང༌། །ལུས་ཀྱི་བ་སྤུ་ལྡང་པར་འགྱུར་པ་གང་ཡིན་པ། །\nདེ་ལ་རྫོགས་པའི་སངས་རྒྱས་བློ་ཡི་ས་བོན་ཡོད། །དེ་ཉིད་ཉེ་བར་བསྟན་པའི་སྣོད་ནི་དེ་ཡིན་ཏེ། །དེ་ལ་དམ་པའི་དོན་གྱི་བདེན་པ་བསྟན་པར་བྱ། །དེ་ལ་དེ་ཡི་རྗེས་སུ་འགྲོ་བའི་ཡོན་ཏན་འབྱུང༌། །\nརྟག་ཏུ་ཚུལ་ཁྲིམས་ཡང་དག་བླངས་ནས་གནས་པར་འག",
                "Span": {"start": 506, "end": 884},
            },
            {
                "index": 7,
                "segmentation_type": "segmentation",
                "text": "ུར། །སྦྱིན་པ་གཏོང་བར་འགྱུར་ཞིང་སྙིང་རྗེ་བསྟེན་པར་བྱེད། །བཟོད་པ་སྒོམ་བྱེད་དེ་ཡི་དགེ་བའང་བྱང་ཆུབ་ཏུ། །འགྲོ་བ་དགྲོལ་བར་བྱ་ཕྱིར་ཡོངས་སུ་བསྔོ་བྱེད་ཅིང༌། །\nརྫོགས་པའི་བྱང་ཆུབ་སེམས་དཔའ་རྣམས་ལ་གུས་པར་བྱེད། །ཟབ་ཅིང་རྒྱ་ཆེའི་ཚུལ་ལ་མཁས་པའི་སྐྱེ་བོས་ནི། །རིམ་གྱིས་རབ་ཏུ་དགའ་བའི་ས་ནི་འཐོབ་འགྱུར་བས།",
                "Span": {"start": 885, "end": 1169},
            },
            {
                "index": 8,
                "segmentation_type": "segmentation",
                "text": "།དེ་ནི་དོན་དུ་གཉེར་བས་ལམ་འདི་མཉན་པར་གྱིས། །",
                "Span": {"start": 1170, "end": 1213},
            },
            {
                "index": 9,
                "segmentation_type": "segmentation",
                "text": "དེ་ཉིད་དེ་ལས་འབྱུང་མིན་གཞན་དག་ལས་ལྟ་ག་ལ་ཞིག །གཉིས་ཀ་ལས་ཀྱང་མ་ཡིན་རྒྱུ་མེད་པར་ནི་ག་ལ་ཡོད། །དེ་ནི་དེ་ལས་འབྱུང་ན་ཡོན་ཏན་འགའ་ཡང་ཡོད་མ་ཡིན། །སྐྱེས་པར་གྱུར་པ་སླར་ཡང་སྐྱེ་བར་རིགས་པའང་མ་ཡིན་ཉིད། །\nསྐྱེ",
                "Span": {"start": 1214, "end": 1407},
            },
            {
                "index": 10,
                "segmentation_type": "segmentation",
                "text": "་ཟིན་སླར་ཡང་སྐྱེ་བར་ཡོངས་སུ་རྟོག་པར་འགྱུར་ན་ནི། །མྱུ་གུ་ལ་སོགས་རྣམས་ཀྱི་སྐྱེ་བ་འདིར་རྙེད་མི་འགྱུར་ཞིང༌། །ས་བོན་སྲིད་མཐར་ཐུག་པར་རབ་ཏུ་སྐྱེ་བ་ཉིད་དུ་འགྱུར། །ཇི་ལྟར་དེ་ཉིད་ཀྱིས་དེ་",
                "Span": {"start": 1408, "end": 1585},
            },
        ]
        assert seg_anns == expected_seg_anns

        spelling_variant_anns = get_anns(
            ann_store=AnnotationStore(
                file=str(self.pecha.layer_path / spelling_variant_path)
            ),
            include_span=True,
        )
        expected_spelling_variant_anns = [
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 206, "end": 207},
            },
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 359, "end": 360},
            },
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 506, "end": 507},
            },
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 673, "end": 674},
            },
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 843, "end": 844},
            },
            {
                "operation": "insertion",
                "text": "",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 844, "end": 844},
            },
            {
                "operation": "deletion",
                "text": "\nརྫོགས་པའི་བྱང་ཆུབ་སེམས་དཔའ་རྣམས་ལ་གུས་པར་བྱེད",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1034, "end": 1080},
            },
            {
                "operation": "insertion",
                "text": "",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1080, "end": 1080},
            },
            {
                "operation": "deletion",
                "text": "།དེ་ནི་དོན་དུ་གཉེར་བས་ལམ་འདི་མཉན་པར་གྱིས། །\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1170, "end": 1214},
            },
            {
                "operation": "insertion",
                "text": "",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1279, "end": 1279},
            },
            {
                "operation": "deletion",
                "text": "ན",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1322, "end": 1323},
            },
            {
                "operation": "insertion",
                "text": "",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1323, "end": 1323},
            },
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1402, "end": 1403},
            },
            {
                "operation": "deletion",
                "text": "པར་",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1441, "end": 1444},
            },
            {
                "operation": "deletion",
                "text": "མི་",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1497, "end": 1500},
            },
            {
                "operation": "deletion",
                "text": "ཉིད་ཀྱིས་དེ་",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1573, "end": 1585},
            },
            {
                "operation": "deletion",
                "text": "\n",
                "spelling_variation": "spelling_variant",
                "Span": {"start": 1616, "end": 1617},
            },
        ]
        assert spelling_variant_anns == expected_spelling_variant_anns

    def tearDown(self):
        # Revert all original files
        for f, content in self.pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.pecha_path.glob("**/*"):
            if f.is_file() and f not in self.pecha_backup:
                f.unlink()
