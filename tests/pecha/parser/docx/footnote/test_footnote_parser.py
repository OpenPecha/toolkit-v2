from pathlib import Path
from unittest import TestCase, mock

from stam import AnnotationStore

from openpecha.pecha import Pecha, get_anns
from openpecha.pecha.annotations import FootnoteAnnotation, Span
from openpecha.pecha.layer import AnnotationType
from openpecha.pecha.parsers import update_coords
from openpecha.pecha.parsers.docx.footnote import DocxFootnoteParser
from openpecha.pecha.parsers.docx.utils import read_docx


class TestFootnoteParser(TestCase):
    def setUp(self):
        self.FOOTNOTE_DIR = Path("tests/pecha/parser/docx/utils/data/footnote")
        self.ONE_PAGE_DIR = self.FOOTNOTE_DIR / "one_page"
        self.one_page_footnote = self.ONE_PAGE_DIR / "one_page_footnote.docx"

        self.parser = DocxFootnoteParser()

        self.expected_footnote_contents = {
            1: "功德光論師，世親菩薩弟子，極善巧毗奈耶，出生於秣搜羅國婆羅門家，幼時 熟習外道宗義及明處，後於家鄉出家並受具足戒，依止世親菩薩，修習大小乘 藏，及聲聞十八部派一切宗義，弟子約五千比丘。住世說約四百年，是否屬實， 猶存疑惑，然而確是住世很久。後圓寂於自己的故鄉。著作頗豐，譯為藏文廣 知者，有《菩薩地所分佈施次第第九之上注釋》、《菩薩地戒品釋》，此二者 由那措譯師及香智軍二位譯為藏文，存於論典經品「ཡི」函中。《毗奈耶根本經》 及其自釋、《毗奈耶行持一百零一竭摩法》，在八世紀末，赤松德贊時，由覺 柔譯師及噶榮戒源二位譯為藏文，存於論典經品「ཟུ」、「འུ」、「ཡུ」。",
            2: "《瑜伽師地論》中《本地分》菩薩地之菩薩戒品。",
            3: "《菩薩地戒品》說:「云何菩薩自性戒?謂若略說具四功德，當知是名菩薩自性戒。何等為四?一、從他正受。二、善淨意樂。三、犯已還淨。四、深敬專念無有違犯。」",
        }
        self.expected_text_without_footnote_content = "1)\t \n\n2)\t 菩薩戒品釋\n\n3)\t 功德光----footnote0----論師造\n\n4)\t 解說菩薩戒品----footnote1----。\n\n5)\t 頂禮一切佛菩薩！\n\n6)\t 問：「云何所說『具四功德自性尸羅----footnote2----，應知即是妙善（淨戒）』？」\n\n7)\t 依彼而言，說「能利自（他）」等文。\n\n8)\t 其中「利益」謂善行。\n\n9)\t 「安樂」謂無惱害。\n\n10)\t 「哀憫」，謂如以諸善及無惱害行哀憫對方。\n\n11)\t 「義利」謂希求義利及具有義利，凡所有欲求及無罪。\n\n12)\t 「利益安樂故」謂住於善及無惱害行。\n\n13)\t 「人」謂刹帝利等，彼等中多數，由於佛陀出世、善說正法、善建立僧伽，當成極多利益、安樂。\n\n14)\t 彼等亦由利益、安樂自己後，而哀憫世間，\n\n15)\t 彼等於他人作如是念：「（他們）具足利益安樂，復何妙哉！」\n\n16)\t 他人亦作是念：「我等亦得如是，亦何其妙哉！」\n\n17)\t 是故，說「令得義利、利益、安樂故。」\n\n18)\t 「諸人天等」謂不能通達及成辦彼等之義利故。\n\n\n\n\n\n"

        self.expected_footnote_spans = {1: (24, 24), 2: (39, 39), 3: (76, 76)}
        self.expected_text_without_footnote_spans = "1)\t \n\n2)\t 菩薩戒品釋\n\n3)\t 功德光論師造\n\n4)\t 解說菩薩戒品。\n\n5)\t 頂禮一切佛菩薩！\n\n6)\t 問：「云何所說『具四功德自性尸羅，應知即是妙善（淨戒）』？」\n\n7)\t 依彼而言，說「能利自（他）」等文。\n\n8)\t 其中「利益」謂善行。\n\n9)\t 「安樂」謂無惱害。\n\n10)\t 「哀憫」，謂如以諸善及無惱害行哀憫對方。\n\n11)\t 「義利」謂希求義利及具有義利，凡所有欲求及無罪。\n\n12)\t 「利益安樂故」謂住於善及無惱害行。\n\n13)\t 「人」謂刹帝利等，彼等中多數，由於佛陀出世、善說正法、善建立僧伽，當成極多利益、安樂。\n\n14)\t 彼等亦由利益、安樂自己後，而哀憫世間，\n\n15)\t 彼等於他人作如是念：「（他們）具足利益安樂，復何妙哉！」\n\n16)\t 他人亦作是念：「我等亦得如是，亦何其妙哉！」\n\n17)\t 是故，說「令得義利、利益、安樂故。」\n\n18)\t 「諸人天等」謂不能通達及成辦彼等之義利故。\n\n\n\n\n\n"

        self.expected_annotations = [
            FootnoteAnnotation(
                index=1,
                span=Span(start=24, end=24),
                note=self.expected_footnote_contents[1],
            ),
            FootnoteAnnotation(
                index=2,
                span=Span(start=39, end=39),
                note=self.expected_footnote_contents[2],
            ),
            FootnoteAnnotation(
                index=3,
                span=Span(start=76, end=76),
                note=self.expected_footnote_contents[3],
            ),
        ]

        self.expected_updated_anns = [
            FootnoteAnnotation(
                index=1,
                span=Span(start=13, end=13, errors=None),
                metadata=None,
                note="功德光論師，世親菩薩弟子，極善巧毗奈耶，出生於秣搜羅國婆羅門家，幼時 熟習外道宗義及明處，後於家鄉出家並受具足戒，依止世親菩薩，修習大小乘 藏，及聲聞十八部派一切宗義，弟子約五千比丘。住世說約四百年，是否屬實， 猶存疑惑，然而確是住世很久。後圓寂於自己的故鄉。著作頗豐，譯為藏文廣 知者，有《菩薩地所分佈施次第第九之上注釋》、《菩薩地戒品釋》，此二者 由那措譯師及香智軍二位譯為藏文，存於論典經品「ཡི」函中。《毗奈耶根本經》 及其自釋、《毗奈耶行持一百零一竭摩法》，在八世紀末，赤松德贊時，由覺 柔譯師及噶榮戒源二位譯為藏文，存於論典經品「ཟུ」、「འུ」、「ཡུ」。",
            ),
            FootnoteAnnotation(
                index=2,
                span=Span(start=24, end=24, errors=None),
                metadata=None,
                note="《瑜伽師地論》中《本地分》菩薩地之菩薩戒品。",
            ),
            FootnoteAnnotation(
                index=3,
                span=Span(start=53, end=53, errors=None),
                metadata=None,
                note="《菩薩地戒品》說:「云何菩薩自性戒?謂若略說具四功德，當知是名菩薩自性戒。何等為四?一、從他正受。二、善淨意樂。三、犯已還淨。四、深敬專念無有違犯。」",
            ),
        ]

        self.pecha = Pecha.from_path(
            Path("tests/pecha/parser/docx/footnote/data/I926CCA43")
        )
        self.pecha_backup = {
            f: f.read_bytes() for f in self.pecha.pecha_path.glob("**/*") if f.is_file()
        }

    def test_get_footnote_contents(self):
        text = read_docx(self.one_page_footnote, ignore_footnotes=False)
        (
            text_without_footnote_content,
            footnote_contents,
        ) = self.parser.get_footnote_contents(text)
        self.assertEqual(footnote_contents, self.expected_footnote_contents)
        self.assertEqual(
            text_without_footnote_content, self.expected_text_without_footnote_content
        )

    def test_get_footnote_spans(self):
        text_without_footnote_spans, footnote_spans = self.parser.get_footnote_spans(
            self.expected_text_without_footnote_content, self.expected_footnote_contents
        )

        self.assertEqual(footnote_spans, self.expected_footnote_spans)
        self.assertEqual(
            text_without_footnote_spans, self.expected_text_without_footnote_spans
        )

    def test_create_footnote_annotations(self):
        annotations = self.parser.create_footnote_annotations(
            self.expected_footnote_spans, self.expected_footnote_contents
        )
        self.assertEqual(annotations, self.expected_annotations)

    def test_update_coords(self):
        new_base = self.pecha.get_base(list(self.pecha.bases.keys())[0])
        updated_anns = update_coords(
            self.expected_annotations,
            self.expected_text_without_footnote_spans,
            new_base,
        )
        self.assertEqual(updated_anns, self.expected_updated_anns)

    @mock.patch("openpecha.pecha.get_layer_id")
    def test_create_footnote_layer(self, mock_get_layer_id):
        mock_get_layer_id.return_value = "D93E"
        annotation_path = self.parser.add_footnote_layer(
            self.pecha, self.expected_updated_anns, AnnotationType.FOOTNOTE
        )
        self.assertEqual(annotation_path, "B4A6/footnote-D93E.json")

        anns = get_anns(
            ann_store=AnnotationStore(
                file=str(self.pecha.layer_path / annotation_path)
            ),
            include_span=True,
        )
        expected_anns = [
            {
                "index": 1,
                "note": "功德光論師，世親菩薩弟子，極善巧毗奈耶，出生於秣搜羅國婆羅門家，幼時 熟習外道宗義及明處，後於家鄉出家並受具足戒，依止世親菩薩，修習大小乘 藏，及聲聞十八部派一切宗義，弟子約五千比丘。住世說約四百年，是否屬實， 猶存疑惑，然而確是住世很久。後圓寂於自己的故鄉。著作頗豐，譯為藏文廣 知者，有《菩薩地所分佈施次第第九之上注釋》、《菩薩地戒品釋》，此二者 由那措譯師及香智軍二位譯為藏文，存於論典經品「ཡི」函中。《毗奈耶根本經》 及其自釋、《毗奈耶行持一百零一竭摩法》，在八世紀末，赤松德贊時，由覺 柔譯師及噶榮戒源二位譯為藏文，存於論典經品「ཟུ」、「འུ」、「ཡུ」。",
                "structure_type": "footnote",
                "text": "",
                "Span": {"start": 13, "end": 13},
            },
            {
                "index": 2,
                "note": "《瑜伽師地論》中《本地分》菩薩地之菩薩戒品。",
                "structure_type": "footnote",
                "text": "",
                "Span": {"start": 24, "end": 24},
            },
            {
                "index": 3,
                "note": "《菩薩地戒品》說:「云何菩薩自性戒?謂若略說具四功德，當知是名菩薩自性戒。何等為四?一、從他正受。二、善淨意樂。三、犯已還淨。四、深敬專念無有違犯。」",
                "structure_type": "footnote",
                "text": "",
                "Span": {"start": 53, "end": 53},
            },
        ]
        self.assertEqual(anns, expected_anns)

    def tearDown(self):
        # Revert all original files
        for f, content in self.pecha_backup.items():
            f.write_bytes(content)

        # Remove any new files that weren't in the original backup
        for f in self.pecha.pecha_path.glob("**/*"):
            if f.is_file() and f not in self.pecha_backup:
                f.unlink()
