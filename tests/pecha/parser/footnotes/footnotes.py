import re
from typing import List


def remove_unwanted_annotations(text: List[str]):
    """
    Minimally parse footnotes into tags that Pecha can parse and removes comment markers in the text
    see https://developers.sefaria.org/docs/text-formatting-beyond-the-segment-level#footnotes
    <sup class="footnote-marker">marker_text</sup><i class="footnote">The text inside the footnote</i>
    """
    def remove_gdoc_comments(text):
        # simply deletes comment marks everywhere.
        for i in range(len(text)):
            line = text[i]
            text[i] = re.sub(r'\[[a-zA-Z]+\]', '', line)

        return text

    def is_note_num(string):
        return not re.sub(r'[0-9]+', '', string)

    def parse_footnotes(text, marker=None):
        # if marker is None, footnote number is used, else value of marker is used

        # 1. separate text and footnotes/comments
        is_footnote = False
        lines, footnotes = [], {}
        for t in text:
            if not is_footnote:
                if not t.strip().replace('_', ''):
                    is_footnote = True
                else:
                    lines.append(t)
            else:
                # ignoring lines without footnote marker
                if '] ' not in t:
                    continue
                num, note = t.split('] ')
                num = num[1:]
                footnotes[num] = note

        # 2. format footnotes
        for i in range(len(lines)):
            line = lines[i]
            parts = re.split(r'\[([0-9]+)\]', line)
            parsed_line = []
            for p in parts:
                if p.strip() and is_note_num(p):
                    mark = marker if marker else p
                    parsed = f'<sup class="footnote-marker">{mark}</sup><i class="footnote">{footnotes[p]}</i>'
                    parsed_line.append(parsed)
                else:
                    parsed_line.append(p)
            lines[i] = ''.join(parsed_line)
        return lines

    parsed = remove_gdoc_comments(text)
    parsed = parse_footnotes(parsed)
    return parsed

class TestFootnotes:
    def test_parse_txt_footnotes(self):
        test_data = [
                        "1.",
                        "2. 敬禮一切[a]佛菩薩",
                        "3. 如是我聞：[abcde]一時，",
                        "4. 世尊[10]在毘舍離大林重樓閣[2]，",
                        "5. 與大比丘眾[302]萬二千人及諸菩薩摩訶薩俱。",
                        "6. 世尊於中夜[4]，結跏趺坐，正念而住，",
                        "7. 有尋有伺[5]，定生喜樂，入於初禪。[6]",
                        "8. 從彼定起，無尋無伺，定生喜樂，入第二禪[7]。",
                        "________________",
                        "[10] 世尊:原文寫做 བཅོམ་ལྡན་འདས，亦音譯為薄伽梵(bhagavat)，為佛陀十號之一，有多種意義。漢譯經典多取其中一義，譯為世尊。",
                        "[2] 大林重樓閣:原文寫做 ཚལ་ཆེན་པོའི་ཁང་པ་བརྩེགས་པའི་གནས。位於中印度毘舍離城北附近。此譯名見《高僧法顯傳》。",
                        "[302] 大比丘眾萬二千人:原文寫做 དགེ་སློང་ཁྲི་ཉིས་སྟོང་གི་དགེ་འདུན་ཆེན་པོ，「大比丘眾」(དགེ་སློང་གི་དགེ་འདུན་ཆེན་པོ)一詞常見於佛典，人數由五百至無量不等。關於此詞彙， 常見的解釋約有二種:一種解為「比丘萬二千人大眾(mahāsaṃghika / དགེ་ འདུན་ཆེན་པོ)」或「比丘大眾萬二千人」，另一則解為「聞法眾皆為大比丘」。 此處譯法順古。",
                        "[4] 中夜:原文寫做 མི་ཉལ་ཙམ，梵文做 praśāntarātriḥ，直譯為「約莫未寢之時」。《翻 譯名義大集》中將之譯為「未映之時」(未映義為天未破曉)，並記為「極為 寧靜之夜」(མཚན་མོ་རབ་ཏུ་ཞི་བ)的同義詞(Mvyt: 8228)。此詞在藏文大藏經中 的出現頻率並不高，若依據藏語文直觀的解讀方式，常有人將之解為「約莫將 寢未寢之時」，但在《大正藏》中，並未出現過「未映之時」一詞，或雖有「未 寢」「未眠」等詞，然其詞義及語境亦與此處有別。基於前述原因，按照字面 將之譯出的做法顯然有待商榷。經比照錄有此詞的藏本大藏經與《大正藏》可 知:《佛說首楞嚴三昧經.卷一》中，將之翻為「中夜半」(CBETA, T15, no. 642)，《方廣大莊嚴經.卷一.序品第一》中翻為「中夜」(CBETA, T03, no. 187)，《佛說月上女經》中則僅翻為「夜」一字(CBETA, T14, no. 480);至 於其餘藏文藏經，僅於《華嚴經》尚有此詞，如《大方廣佛華嚴經.佛不思議 法品.第三十三》，但在漢譯《佛不思議法品》中，則未將該詞譯出。在此， 根據前述分析，參考《首楞嚴三昧經》與《方廣大莊嚴經》，將此詞彙譯為「中 夜」。",
                        "[5] 有尋有伺:尋伺為尋、伺二詞之合稱。尋係指粗大的分別，伺則指細微的分別。 相關解釋，可參考《中華佛教百科全書》「尋伺」條:「尋與伺二心所的併稱。 『尋』者，舊譯『覺』，為粗略推求諸法名義的思惟作用，通於定、散及無漏。 『伺』者，舊譯『觀』，乃細心伺察諸法名義的思惟作用，不遍於一切心，不 起於一切時，其性雖遲鈍，但深入推度名身等，與『尋』同有等起語言之作用。 二者皆攝於俱舍七十五法的不定地法、唯識百法的四不定。」",
                        "[6] 有尋有伺，定生喜樂，入於初禪:原文寫做 རྟོག་པ་དང་བཅས་པ། དཔྱོད་པ་དང་བཅས་པའི་ཏིང་ངེ་འཛིན་ལས་སྐྱེས་པའི་དགའ་བ་དང་བདེ་བ་ཅན་བསམ་གཏན་དང་པོ་ལ་སྙོམས་པར་ཞུགས，直譯為「平 等安住於帶有尋伺的三昧所生喜樂之初禪」。其中「定生喜樂」一詞，義為「由 三昧所生之喜樂」，漢文古譯多做此種譯法，今從古而譯，下同。特此說明。 又，漢譯佛經中，「定生喜樂」往往專指二禪境界，而初禪則多譯為「離生喜 樂」，義為「由『捨離五欲及諸罪』所生之喜樂」。由於原文已經敘明是由三 昧所生之喜樂，故雖與漢譯慣用譯法略有出入，此處仍將之譯為「定生喜樂」。 又，「禪」字原文寫做 བསམ་གཏན，梵文則做 dhyāna，音譯為禪那，簡稱禪;意 譯則為靜慮，義指心專注於某一事物的狀態。鳩摩羅什翻譯此字時，多做靜慮， 但有時也會譯為禪。玄奘翻譯時則一律譯為靜慮。為俾讀誦，此處採用鳩摩羅 什的譯法，將之譯為禪。此外，漢譯佛典中，多將「入於初禪」寫做「入初禪」 或「入初靜慮」。為俾讀誦並兼顧前後用語的一致性，此處採用權宜的譯法， 譯為「入於初禪」。",
                        "[7] 此句省略了主詞「世尊」。由於此段關於入出四禪境界的主詞皆為世尊，為俾 閱讀，特將入於第二、三四禪的主詞世尊一概略去不譯，不另行再加註解。特 此說明。",
                        "[a]@drupchen@pecha.org Note11 is also not presented properly. ",
                        "[abcde]test google comment. "
                    ]
        expected = [
                        '1.',
                        '2. 敬禮一切佛菩薩',
                        '3. 如是我聞：一時，',
                        '4. 世尊<sup class="footnote-marker">10</sup><i class="footnote">世尊:原文寫做 བཅོམ་ལྡན་འདས，亦音譯為薄伽梵(bhagavat)，為佛陀十號之一，有多種意義。漢譯經典多取其中一義，譯為世尊。</i>在毘舍離大林重樓閣<sup class="footnote-marker">2</sup><i class="footnote">大林重樓閣:原文寫做 ཚལ་ཆེན་པོའི་ཁང་པ་བརྩེགས་པའི་གནས。位於中印度毘舍離城北附近。此譯名見《高僧法顯傳》。</i>，',
                        '5. 與大比丘眾<sup class="footnote-marker">302</sup><i class="footnote">大比丘眾萬二千人:原文寫做 དགེ་སློང་ཁྲི་ཉིས་སྟོང་གི་དགེ་འདུན་ཆེན་པོ，「大比丘眾」(དགེ་སློང་གི་དགེ་འདུན་ཆེན་པོ)一詞常見於佛典，人數由五百至無量不等。關於此詞彙， 常見的解釋約有二種:一種解為「比丘萬二千人大眾(mahāsaṃghika / དགེ་ འདུན་ཆེན་པོ)」或「比丘大眾萬二千人」，另一則解為「聞法眾皆為大比丘」。 此處譯法順古。</i>萬二千人及諸菩薩摩訶薩俱。',
                        '6. 世尊於中夜<sup class="footnote-marker">4</sup><i class="footnote">中夜:原文寫做 མི་ཉལ་ཙམ，梵文做 praśāntarātriḥ，直譯為「約莫未寢之時」。《翻 譯名義大集》中將之譯為「未映之時」(未映義為天未破曉)，並記為「極為 寧靜之夜」(མཚན་མོ་རབ་ཏུ་ཞི་བ)的同義詞(Mvyt: 8228)。此詞在藏文大藏經中 的出現頻率並不高，若依據藏語文直觀的解讀方式，常有人將之解為「約莫將 寢未寢之時」，但在《大正藏》中，並未出現過「未映之時」一詞，或雖有「未 寢」「未眠」等詞，然其詞義及語境亦與此處有別。基於前述原因，按照字面 將之譯出的做法顯然有待商榷。經比照錄有此詞的藏本大藏經與《大正藏》可 知:《佛說首楞嚴三昧經.卷一》中，將之翻為「中夜半」(CBETA, T15, no. 642)，《方廣大莊嚴經.卷一.序品第一》中翻為「中夜」(CBETA, T03, no. 187)，《佛說月上女經》中則僅翻為「夜」一字(CBETA, T14, no. 480);至 於其餘藏文藏經，僅於《華嚴經》尚有此詞，如《大方廣佛華嚴經.佛不思議 法品.第三十三》，但在漢譯《佛不思議法品》中，則未將該詞譯出。在此， 根據前述分析，參考《首楞嚴三昧經》與《方廣大莊嚴經》，將此詞彙譯為「中 夜」。</i>，結跏趺坐，正念而住，',
                        '7. 有尋有伺<sup class="footnote-marker">5</sup><i class="footnote">有尋有伺:尋伺為尋、伺二詞之合稱。尋係指粗大的分別，伺則指細微的分別。 相關解釋，可參考《中華佛教百科全書》「尋伺」條:「尋與伺二心所的併稱。 『尋』者，舊譯『覺』，為粗略推求諸法名義的思惟作用，通於定、散及無漏。 『伺』者，舊譯『觀』，乃細心伺察諸法名義的思惟作用，不遍於一切心，不 起於一切時，其性雖遲鈍，但深入推度名身等，與『尋』同有等起語言之作用。 二者皆攝於俱舍七十五法的不定地法、唯識百法的四不定。」</i>，定生喜樂，入於初禪。<sup class="footnote-marker">6</sup><i class="footnote">有尋有伺，定生喜樂，入於初禪:原文寫做 རྟོག་པ་དང་བཅས་པ། དཔྱོད་པ་དང་བཅས་པའི་ཏིང་ངེ་འཛིན་ལས་སྐྱེས་པའི་དགའ་བ་དང་བདེ་བ་ཅན་བསམ་གཏན་དང་པོ་ལ་སྙོམས་པར་ཞུགས，直譯為「平 等安住於帶有尋伺的三昧所生喜樂之初禪」。其中「定生喜樂」一詞，義為「由 三昧所生之喜樂」，漢文古譯多做此種譯法，今從古而譯，下同。特此說明。 又，漢譯佛經中，「定生喜樂」往往專指二禪境界，而初禪則多譯為「離生喜 樂」，義為「由『捨離五欲及諸罪』所生之喜樂」。由於原文已經敘明是由三 昧所生之喜樂，故雖與漢譯慣用譯法略有出入，此處仍將之譯為「定生喜樂」。 又，「禪」字原文寫做 བསམ་གཏན，梵文則做 dhyāna，音譯為禪那，簡稱禪;意 譯則為靜慮，義指心專注於某一事物的狀態。鳩摩羅什翻譯此字時，多做靜慮， 但有時也會譯為禪。玄奘翻譯時則一律譯為靜慮。為俾讀誦，此處採用鳩摩羅 什的譯法，將之譯為禪。此外，漢譯佛典中，多將「入於初禪」寫做「入初禪」 或「入初靜慮」。為俾讀誦並兼顧前後用語的一致性，此處採用權宜的譯法， 譯為「入於初禪」。</i>',
                        '8. 從彼定起，無尋無伺，定生喜樂，入第二禪<sup class="footnote-marker">7</sup><i class="footnote">此句省略了主詞「世尊」。由於此段關於入出四禪境界的主詞皆為世尊，為俾 閱讀，特將入於第二、三四禪的主詞世尊一概略去不譯，不另行再加註解。特 此說明。</i>。'
                    ]
        res = remove_unwanted_annotations(test_data)

        assert res == expected

TestFootnotes().test_parse_txt_footnotes()