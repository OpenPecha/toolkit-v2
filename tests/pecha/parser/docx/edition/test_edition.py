from unittest import TestCase
from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.docx.edition import DocxEditionParser
from openpecha.pecha.parsers.docx.utils import extract_numbered_list
from openpecha.pecha.annotations import SegmentationAnnotation, Span, SpellingVariantAnnotation

class TestDocxEditionParser(TestCase):
    def setUp(self):
        self.DATA = Path(__file__).parent / "data"
        self.docx_file = self.DATA / "edition.docx"

        pecha_path = Path("tests/alignment/commentary_transfer/data/root/I6556B464")
        self.pecha = Pecha.from_path(pecha_path)

    def test_segmentation_parse(self):
        parser = DocxEditionParser()
        anns = parser.parse_segmentation(self.docx_file)
        
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
            SegmentationAnnotation(span=Span(start=1410, end=1605), index=10)
        ]

        assert anns == expected_anns

    def test_spelling_variant_parse(self):
        parser = DocxEditionParser()

        # Insertion        
        old_base = "Hello"
        new_base = "Hello World"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            SpellingVariantAnnotation(span=Span(start=5, end=5), operation="insertion", text=" World")
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
            SpellingVariantAnnotation(span=Span(start=5, end=5), operation="insertion", text="!!")
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
            SpellingVariantAnnotation(span=Span(start=13, end=13), operation="insertion", text="Attractive")
        ]   

        # Test with google docs
        old_basename = list(self.pecha.bases.keys())[0]
        old_base = self.pecha.get_base(old_basename)

        numbered_list = extract_numbered_list(self.docx_file)
        new_base = "\n".join(list(numbered_list.values()))
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [
            {'operation': 'insertion', 'start': 87, 'text': '\n'}, 
            {'operation': 'insertion', 'start': 283, 'text': '\n'}, 
            {'operation': 'deletion', 'start': 675, 'end': 676}, 
            {'operation': 'insertion', 'start': 890, 'text': ' རྟག་ཏུ་ཚུལ་ཁྲིམས་ཡང་དག་བླངས་ནས་གནས་པར་འགྱུར།'}, 
            {'operation': 'deletion', 'start': 1081, 'end': 1127}, 
            {'operation': 'insertion', 'start': 1127, 'text': 'འགྲོ་བ་དགྲོལ་བར་བྱ་ཕྱིར་ཡོངས་སུ་བསྔོ་བྱེད་ཅིང༌'}, 
            {'operation': 'insertion', 'start': 1176, 'text': '\n'}, 
            {'operation': 'deletion', 'start': 1264, 'end': 1307}, 
            {'operation': 'insertion', 'start': 1373, 'text': 'པར་'}, 
            {'operation': 'deletion', 'start': 1419, 'end': 1420}, 
            {'operation': 'insertion', 'start': 1420, 'text': 'བ'}, 
            {'operation': 'deletion', 'start': 1539, 'end': 1542}, 
            {'operation': 'deletion', 'start': 1595, 'end': 1598}, 
            {'operation': 'deletion', 'start': 1671, 'end': 1683}, 
            {'operation': 'deletion', 'start': 1714, 'end': 1715}
        ]


    def tearDown(self):
        pass 

