from pathlib import Path
from typing import List


class PlainTextLineAlignedParser:
    def __init__(self, source_text: str, target_text: str):
        self.source_text = source_text
        self.target_text = target_text

    @classmethod
    def from_files(cls, source_path: Path, target_path: Path):
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        return cls(source_text, target_text)

    def parse(self):
        source_lines = split_text_into_lines(self.source_text)  # noqa
        target_lines = split_text_into_lines(self.target_text)  # noqa


def split_text_into_lines(text: str) -> List[str]:
    """Split text into lines and add newline to each lines"""
    lines = text.split("\n")
    lines = [
        line + "\n" if i < len(lines) - 1 else line for i, line in enumerate(lines)
    ]
    return lines
