from pathlib import Path
from unittest import TestCase

from openpecha.pecha.parsers.docx.footnote import DocxFootnoteParser
from openpecha.pecha.parsers.docx.utils import read_docx


class TestFootnoteParser(TestCase):
    def setUp(self):
        self.FOOTNOTE_DIR = Path("tests/pecha/parser/docx/utils/data/footnote")
        self.ONE_PAGE_DIR = self.FOOTNOTE_DIR / "one_page"
        self.TWO_PAGE_DIR = self.FOOTNOTE_DIR / "two_page"
        self.one_page_footnote = self.ONE_PAGE_DIR / "one_page_footnote.docx"
        self.two_page_footnote = self.TWO_PAGE_DIR / "two_page_footnote.docx"

    def test_parse_one_page_footnote(self):
        parser = DocxFootnoteParser()
        text = read_docx(self.one_page_footnote, ignore_footnotes=False)

        # Test GET FOOTNOTE CONTENTS
        _, footnote_contents = parser.get_footnote_contents(text)
        expected_footnote_contents = {
            0: "功德光論師，世親菩薩弟子，極善巧毗奈耶，出生於秣搜羅國婆羅門家，幼時 熟習外道宗義及明處，後於家鄉出家並受具足戒，依止世親菩薩，修習大小乘 藏，及聲聞十八部派一切宗義，弟子約五千比丘。住世說約四百年，是否屬實， 猶存疑惑，然而確是住世很久。後圓寂於自己的故鄉。著作頗豐，譯為藏文廣 知者，有《菩薩地所分佈施次第第九之上注釋》、《菩薩地戒品釋》，此二者 由那措譯師及香智軍二位譯為藏文，存於論典經品「ཡི」函中。《毗奈耶根本經》 及其自釋、《毗奈耶行持一百零一竭摩法》，在八世紀末，赤松德贊時，由覺 柔譯師及噶榮戒源二位譯為藏文，存於論典經品「ཟུ」、「འུ」、「ཡུ」。",
            1: "《瑜伽師地論》中《本地分》菩薩地之菩薩戒品。",
            2: "《菩薩地戒品》說:「云何菩薩自性戒?謂若略說具四功德，當知是名菩薩自性戒。何等為四?一、從他正受。二、善淨意樂。三、犯已還淨。四、深敬專念無有違犯。」",
        }

        self.assertEqual(footnote_contents, expected_footnote_contents)
