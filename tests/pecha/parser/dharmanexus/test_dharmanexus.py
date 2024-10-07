from pathlib import Path
from openpecha.pecha.parsers.dharamanexus import DharamanexusParser


def test_dharmanexus():
    file_dict = {
        "BO_K01_D0001_H0001": [
            "./tests/pecha/parser/dharmanexus/data/BO_K01_D0001_H0001$0.json", 
            "./tests/pecha/parser/dharmanexus/data/BO_K01_D0001_H0001$1.json"
            ],
        "BO_K01_D0001-2_H0001-2": [
            "./tests/pecha/parser/dharmanexus/data/BO_K01_D0001-2_H0001-2$0.json",
            "./tests/pecha/parser/dharmanexus/data/BO_K01_D0001-2_H0001-2$1.json"
            ]
    }
    dharmanexus = DharamanexusParser()
    dharmanexus.parse(file_dict)
    assert dharmanexus.state['BO_K01_D0001_H0001']['base_text'] == Path("./tests/pecha/parser/dharmanexus/data/expected_base_text.txt").read_text(encoding="utf-8")
    assert dharmanexus.state['BO_K01_D0001_H0001']['annotations']['segments']['BO_K01_D0001_H0001:80a-16']['span'] == {'start': 175695, 'end': 175795}
    assert dharmanexus.state['BO_K01_D0001-2_H0001-2']['annotations']['pages']['58a']['span'] == {'start': 123317, 'end': 124350}