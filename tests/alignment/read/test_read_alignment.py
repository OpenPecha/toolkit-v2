from pathlib import Path
from typing import Dict

from openpecha.alignment import Alignment
from openpecha.pecha import Pecha


def test_read_alignment():
    DATA = Path(__file__).parent / "data"
    alignment_path = DATA / "ABA8AD5BB"
    source_id, target_id = (
        "IA4C08511",
        "IDBEEDAAE",
    )
    pechas: Dict[str, Pecha] = {
        source_id: Pecha.from_path(DATA / source_id),
        target_id: Pecha.from_path(DATA / target_id),
    }
    alignment = Alignment.from_path(alignment_path, pechas=pechas)
    assert isinstance(alignment, Alignment)

    expected_segment_pairs = [
        {
            "9df88463d04b42cf929107f78f716bd5": {
                "IDBEEDAAE": "སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ།། བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་།། ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ།།\n",  # noqa
                "IA4C08511": "A Guide To The Bodhisattava's Way of Life Homage to all Buddha's and Bodhisattvas Respectfully I prostrate myself to the Sugatas Who are endowed with the Dharmakaya, As well as to their Noble Children And to all who are worthy of veneration.\n",  # noqa
            }
        },
        {
            "537af136ffb54580a39d8ec1070a27ad": {
                "IDBEEDAAE": "བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི།། ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ།།\n",
                "IA4C08511": "Here I shall explain how to engage in the vows of the Buddha's Children, The meaning of which I have condensed in accordance with the scriptures.\n",  # noqa
            }
        },
        {
            "8f2cc05c3d4143128cb49178c5680006": {
                "IDBEEDAAE": "སྔོན་ཆད་མ་བྱུང་བ་ཡང་འདིར་བརྗོད་མེད།། སྡེབ་སྦྱོར་མཁས་པའང་བདག་ལ་ཡོད་མིན་ཏེ།། དེ་ཕྱིར་གཞན་དོན་བསམ་པའང་བདག་ལ་མེད།། རང་གི་ཡིད་ལ་བསྒོམ་ཕྱིར་ངས་འདི་བརྩམས།།\n",  # noqa
                "IA4C08511": "Thete is nothing hete that has not been explained before And I have no skill in the art of thetotic; Therefore, lacking any intention to benefit others, I write this in order to acquaint it to my mind.\n",  # noqa
            }
        },
        {
            "cbb2cb8079854f1e8a00a5ef02b3f7ee": {
                "IDBEEDAAE": "དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས།། འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ།།\n",
                "IA4C08511": "For due to acquaintance with what is wholesome, The force of my faith may for a short while increase because of these.\n",  # noqa
            }
        },
        {
            "cd62a29f6f644e1e95b7e9ca9a8539ee": {
                "IDBEEDAAE": "བདག་དང་སྐལ་བ་མཉམ་པ་གཞན་གྱིས་ཀྱང་།། ཅི་སྟེ་འདི་དག་མཐོང་ན་དོན་ཡོད་འགྱུར།།",
                "IA4C08511": "If, however, these are seen by others Equal in fortune to myself, it may be meaningful.",
            }
        },
    ]
    segment_pairs = list(alignment.get_segment_pairs())

    assert segment_pairs == expected_segment_pairs


test_read_alignment()
