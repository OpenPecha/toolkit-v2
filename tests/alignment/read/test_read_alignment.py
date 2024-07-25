from pathlib import Path
from typing import Dict

from openpecha.alignment import Alignment
from openpecha.pecha import Pecha


def test_read_alignment():
    DATA = Path(__file__).parent / "data"
    alignment_path = DATA / "A0FAF24AC"
    source_id, target_id = (
        "I72772C62",
        "I01F61FAA",
    )
    pechas: Dict[str, Pecha] = {
        source_id: Pecha.from_path(DATA / source_id),
        target_id: Pecha.from_path(DATA / target_id),
    }
    alignment = Alignment.from_path(alignment_path, pechas=pechas)
    assert isinstance(alignment, Alignment)

    expected_segment_pairs = [
        {"0bba36e6b39e4e9eb2532c3db3ad4b18": {"I72772C62": "", "I01F61FAA": ""}},
        {
            "feaf3bf6b46b433394a4c2382843e6f8": {
                "I72772C62": "\ufeffརྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།\n",
                "I01F61FAA": "\ufeff{D3874}༄༅༅། །རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙཱརྱ་ཨ་བ་ཏཱ་ར་སང་ཀཱ་ར།\n",
            }
        },
        {
            "9fd3553654d4494b932a4ffe0b372c39": {
                "I72772C62": "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ།\n",
                "I01F61FAA": "བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པའི་ལེགས་པར་སྦྱར་བ།\n",
            }
        },
        {
            "93a2ad62cbd843e2bc66213cdb8def22": {
                "I72772C62": "སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །\n",
                "I01F61FAA": "བཅོམ་ལྡན་འདས་གསུང་གི་མངའ་བདག་འཇམ་དཔལ་གཞོན་ནུར་གྱུར་པ་ལ་ཕྱག་འཚལ་ལོ། །ངོ་བོ་ཉིད་ནི་བྱང་ཆུབ་སེམས་པའི། །རྒྱ་མཚོ་དེ་ལ་ཕྱག་འཚལ་ཏེ། །བདག་འདྲའི་སྤྱོད་པའི་ཡན་ལག་ལ། །འཇུག་ཕྱིར་ལེགས་སྦྱར་བཤད་ཙམ་བྱ། །དམ་པ་རྣམས་ཀྱིས་ནི་ཐོག་མ་དང་བར་དང་ཐ་མར་དགེ་བ་མངོན་པར་འཕེལ་བར་བྱ་བ་ཡིན་པས། བདེ་གཤེགས་ཞེས་བྱ་བ་ལ་སོགས་པ་སྨོས་པ་ཡིན་ཏེ། འདིར་ཕྱག་འཚལ་བ་ནི་དང་པོར་དགེ་བའོ། །ཆོས་བསྟན་པ་ནི་བར་དུ་དགེ་བའོ། །དགེ་བའི་རྩ་བ་ཡོངས་སུ་བསྔོ་བ་ནི་དགེ་བའི་རྩ་བ་མངོན་པར་འཕེལ་བ་ཡིན་པས་ཐ་མར་དགེ་བ་ཡིན་ནོ། །དེ་ལ་བདེ་བར་གཤེགས་པ་ནི་རྟོགས་པར་བྱ་བའི་ལྷག་མ་མི་མངའ་བས་ན་ཡོངས་སུ་རྫོགས་པར་ཐུགས་སུ་ཆུད་པའི་ཕྱིར་བདེ་བར་གཤེགས་པའོ། །ཆོས་ཀྱི་སྐུ་མངའ་བ་ནི་ལུང་དང་རྟོགས་པའི་བདག་ཉིད་ཅན་གྱི་དམ་པའི་ཆོས་ཀྱི་ཚོགས་ནི་ཆོས་ཀྱི་སྐུ་སྟེ་དེ་དང་བཅས་པའོ། །སྲས་བཅས་ནི་ཉིད་ལས་འཁྲུངས་པའི་སྲས་ཏེ། བྱང་ཆུབ་སེམས་དཔའ་དང་བཅས་པའོ། །ལ་ལ་ལས་ནི་བདེ་གཤེགས་དམ་པའི་ཆོས་དང་དགེ་འདུན་བཅས་ཞེས་ཟེར་རོ། །བཙུན་པ་ནི་ཉན་ཐོས་ཆེན་པོ་བརྒྱད་ལ་སོགས་པ་ལ་བྱ་སྟེ། དེ་དག་མ་ལུས་པ་ཀུན་ལ་ཕྱག་འཚལ་བའོ། །དཀོན་མཆོག་གསུམ་པོ་གཙོ་བོར་གྱུར་པས་སོ་སོར་སྨོས་པ་ཡིན་ལ། དེ་དག་ཀྱང་ཕྱག་བྱ་བར་འོས་པ་ཡིན་པས་གུས་པས་ཕྱག་འཚལ་ཏེ། ཞེས་བྱ་བ་སྨོས་ཏེ། འདིར་ཡོན་ཏན་དམ་པའི་བསྟོད་པ་རྒྱ་ཆེ་བ་དང་། མཆོད་པ་ཁྱད་པར་དུ་འཕགས་པའི་དམིགས་པ་ཡིད་ལ་བྱེད་པ་ལས་བྱུང་བའི་མོས་པའི་བསམ་པ་ཤིན་ཏུ་ཕུལ་དུ་བྱུང་བའི་དགའ་བ་རྒྱ་ཆེ་བའི་མཆོད་པ་དང་བཅས་པས་ལུས་ཞིང་ཐམས་ཅད་ཀྱི་རྡུལ་སྙེད་ཀྱིས་བཏུད་ཅིང་ཕྱག་འཚལ་ལོ། །དེ་ལྟར་ཕྱག་བཙལ་ནས་ཅི་ཞིག་བྱེད་ཅེ་ན། བདེ་གཤེགས་སྲས་ཀྱི་ཞེས་བྱ་བ་ལ་སོགས་པ་སྨོས་ཏེ། བདེ་བར་གཤེགས་པའི་བདག་ཉིད་ནི་ཆོས་ཀྱི་སྐུ་སྟེ། དེའི་དབང་དུ་བྱས་པ་ལས་སྐྱེས་པ་ས་ཆེན་པོ་ཐོབ་པ་དང་། རྒྱུ་ལ་གནས་པ་རྣམས་སོ། །དེ་རྣམས་ཀྱི་སྡོམ་པ་ནི་མི་དགེ་བ་སྤོང་བ་དང་། དགེ་བ་ལ་འཇུག་པ་དང་། སེམས་ཅན་གྱི་དོན་བྱ་བའོ། །དེ་ཡང་བཅོམ་ལྡན་འདས་ཀྱིས་ཤིན་ཏུ་ཟབ་ཅིང་རྒྱ་ཆེ་བའི་བདག་ཉིད་ཅན་དུ་གསུངས་ལ། དེར་བྱང་ཆུབ་ཏུ་སེམས་བསྐྱེད་པའི་ཕན་ཡོན་ལ་སོགས་པའི་དོན་རྣམ་པ་བཅུ་པོ་གང་ཡིན་པ་དེས་འཇུག་པའི་བདེ་བར་གཤེགས་པའི་སྲས་ཀྱི་སྡོམ་པ་ལ་འཇུག་པ་བསྟན་པར་བྱའོ། །དེ་ཡང་ལུང་བཞིན་ཞེས་བྱ་བ་སྟེ། ལུང་གི་དོན་དང་མི་འགལ་བར་རོ། །ལུང་ལས་ནི་བཅོམ་ལྡན་འདས་ཀྱིས་རྒྱ་ཆེར་གསུངས་སོ་ཞེ་ན། མདོར་བསྡུས་ནས་ནི་ཞེས་བྱ་བ་སྨོས་སོ། །དེ་ལྟ་ཡིན་དུ་ཆུག་ན། ཅི་འདིར་སྔོན་ཆད་མ་བྱུང་བ་གཞན་འགའ་ཞིག་སྨས་སམ།\n",  # noqa
            }
        },
        {
            "4f7ca86decbc447c9cf7b4e440bf7df9": {
                "I72772C62": "བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །\n",  # noqa
                "I01F61FAA": "\n",
            }
        },
        {
            "318a68c05cd0475b94162c884ddaa74b": {
                "I72772C62": "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད། །སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ། །དེ་ཕྱིར་གཞན་དོན་བསམ་པ་བདག་ལ་མེད། །རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས། །",  # noqa
                "I01F61FAA": "ལུང་ཇི་ལྟ་བ་ཡིན་ཞེ་ན། སྔོན་ཆད་ཅེས་བྱ་བ་ལ་སོགས་པ་སྨོས་སོ། །སྡེབ་སྦྱོར་མཁས་པས་སྔོན་མ་ཡིན་ནམ་ཞེ་ན། སྡེབ་སྦྱོར་ཞེས་བྱ་བ་ལ་སོགས་པ་སྨོས་སོ། །གང་གི་ཕྱིར་འདིར་སྡེབ་སྦྱོར་ལ་མཁས་པ་མེད་པ་ཉིད་ཀྱི་ཕྱིར་གཞན་གྱི་དོན་དུ་བདག་གིས་འདི་གཞུང་དུ་ཉེ་བར་སྦྱར་བ་མ་བྱས་སོ་ཞེས་བྱ་བར་དགོངས་སོ། །དེ་ལྟར་གལ་ཏེ་གཞན་གྱི་དོན་དུ་མ་བྱས་ན་ཅིའི་ཕྱིར་བྱེད་ཅེ་ན། དེའི་ཕྱིར་རང་གི་ཞེས་བྱ་བ་ལ་སོགས་པ་སྨོས་ཏེ། ཡིད་ལ་འདིར་བྱང་ཆུབ་ཀྱི་སེམས་ཏེ། དེ་བསྒོམ་པའི་ཕྱིར་ཞེས་བྱ་བ་ནི་བསླབ་པའི་ཕྱིར་རོ། །བཅོམ་ལྡན་འདས་ཀྱིས་ལུང་ལས་ཚིག་གི་དོན་རྒྱ་ཆེར་གསུངས་པ་དེ་ལས་མདོར་བསྡུས་ཏེ་རང་གི་ཡིད་ལ་བསྒོམ་པར་བྱ་བའི་ཕྱིར་བདག་གིས་འདི་བྱས་སོ་ཞེས་པའོ། །",  # noqa
            }
        },
    ]
    segment_pairs = list(alignment.get_segment_pairs())

    assert segment_pairs == expected_segment_pairs


test_read_alignment()
