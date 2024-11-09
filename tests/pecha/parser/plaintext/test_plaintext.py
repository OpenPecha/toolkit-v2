import tempfile
from pathlib import Path
from openpecha.pecha.parsers.plaintext import plaintextparser 


def test_plain_text_bo():
    text_path = Path("tests/pecha/parser/plaintext/data/bo.txt")
    metadata = {
        "title": "test",
        "author": "test",
        "language": "bo",
        "initial_creation_type": "ebook",
        "source_metadata": {
            "source_id": "test01",
            "title": "བོད་ཡིག་གི་བཀོད་པ།",
            "author": "བོད་ཡིག་གི་བཀོད་པ།"
        },
    }
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        parser = plaintextparser()
        parser.parse(input=text_path, metadata=metadata, output_path=output_path)
        assert parser.temp_state['base_text'] == Path("tests/pecha/parser/plaintext/data/expected_base_bo.txt").read_text(encoding="utf-8")
        assert parser.temp_state['annotations']['segments']["89a.2"]["span"] == {"start": 728, "end": 957}
        assert parser.temp_state['annotations']['pages']["90b"]["span"] == {"start": 5178, "end": 6714}
    

def test_plain_text_zh():
    text_path = Path("tests/pecha/parser/plaintext/data/zh.txt")
    metadata = {
        "title": "test",
        "author": "test",
        "language": "zh",
        "initial_creation_type": "ebook",
        "source_metadata": {
            "source_id": "test01",
            "title": "བོད་ཡིག་གི་བཀོད་པ།",
            "author": "བོད་ཡིག་གི་བཀོད་པ།"
        },
    }
    output_path = Path("tests/pecha/parser/plaintext/data/")
    with tempfile.TemporaryDirectory() as tmpdirname:
        output_path = Path(tmpdirname)
        parser = plaintextparser()
        parser.parse(input=text_path, metadata=metadata, output_path=output_path)
        assert parser.temp_state['base_text'] == Path("tests/pecha/parser/plaintext/data/expected_base_zh.txt").read_text(encoding="utf-8")
        assert parser.temp_state['annotations']['segments'][20]["span"] == {"start": 808, "end": 833}
