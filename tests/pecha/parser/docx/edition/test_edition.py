from unittest import TestCase
from pathlib import Path

from openpecha.pecha import Pecha
from openpecha.pecha.parsers.docx.edition import DocxEditionParser
from openpecha.pecha.parsers.docx.utils import extract_numbered_list

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
            {'Span': {'start': 0, 'end': 87}, 'index': '1'},
            {'Span': {'start': 88, 'end': 207}, 'index': '2'},
            {'Span': {'start': 208, 'end': 283}, 'index': '3'},
            {'Span': {'start': 284, 'end': 361}, 'index': '4'},
            {'Span': {'start': 362, 'end': 508}, 'index': '5'},
            {'Span': {'start': 509, 'end': 844}, 'index': '6'},
            {'Span': {'start': 845, 'end': 1129}, 'index': '7'},
            {'Span': {'start': 1130, 'end': 1217}, 'index': '8'},
            {'Span': {'start': 1218, 'end': 1409}, 'index': '9'},
            {'Span': {'start': 1410, 'end': 1605}, 'index': '10'}
        ]

        assert anns == expected_anns

    def test_spelling_variant_parse(self):
        parser = DocxEditionParser()

        # Insertion        
        old_base = "Hello"
        new_base = "Hello World"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [{'operation': 'insertion', 'start': 5, 'text': ' World'}]

        # Deletion        
        old_base = "Hello World"
        new_base = "Hello"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [{'operation': 'deletion', 'start': 5, 'end': 11}]
        
        # Insertion in Between
        old_base = "Hello World"
        new_base = "Hello!! World"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [{'operation': 'insertion', 'start': 5, 'text': '!!'}]

        # Deletion in Between
        old_base = "Good morning, Everyone"
        new_base = "Good Everyone"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [{'operation': 'deletion', 'start': 4, 'end': 13}]

        ## Insertion and Deletion
        old_base = "Good morning, Ladies and Gentlemen"
        new_base = "Good Attractive Ladies and Gentlemen"
        diffs = parser.parse_spelling_variant(old_base, new_base)
        assert diffs == [{'operation': 'deletion', 'start': 5, 'end': 13}, {'operation': 'insertion', 'start': 13, 'text': 'Attractive'}]        


    def tearDown(self):
        pass 


if __name__ == "__main__":
    test = TestDocxEditionParser()
    
    test.setUp()
    test.test_segmentation_parse()
    test.test_spelling_variant_parse()
