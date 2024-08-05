import json
import re
from pathlib import Path


class PlainTextChapterAnnotationParser:
    def __init__(self, plain_text: str, meta_data: dict):
        self.plain_text = plain_text
        self.meta_data = meta_data

    @classmethod
    def from_file(cls, file_path: Path, meta_data_path: Path):
        plaintext = file_path.read_text(encoding="utf-8")
        with open(meta_data_path) as f:
            meta_data = json.load(f)
        return cls(plaintext, meta_data)

    def parse(self):

        pattern = re.compile(r"ch(\d+)-(\"[\u0F00-\u0FFF]+\")")
        matches = pattern.finditer(self.plain_text)

        for match in matches:
            chapter = match.group(1)
            tibetan_text = match.group(2)
            start_index = match.start()
            end_index = match.end()
            print(
                f"Chapter: {chapter}, Text: {tibetan_text}, Start Index: {start_index}, End Index: {end_index}"
            )
