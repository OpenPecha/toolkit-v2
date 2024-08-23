import json
import re
from pathlib import Path


class PlainTextNumberAlignedParser:
    """
    Class to parse plain text lines and create aligned annotations.
    """

    def __init__(self, source_text: str, target_text: str, metadata: dict):
        self.source_text = source_text
        self.target_text = target_text
        self.metadata = metadata

    @classmethod
    def from_files(
        cls, source_path: Path, target_path: Path, metadata_path: Path
    ) -> "PlainTextNumberAlignedParser":
        """
        Create a parser instance from file paths.
        """
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        with open(metadata_path) as f:
            metadata = json.load(f)
        return cls(source_text, target_text, metadata)

    @staticmethod
    def normalize_newlines(text: str) -> str:
        text = text.strip()

        """ Replace more than two consecutive newlines  with exactly two newlines. """
        pattern = r"\n{3,}"
        text = re.sub(pattern, "\n\n", text)
        return text

    def parse_text_into_segment_pairs(self):
        """
        Parse the source and target texts into segment pairs.
        """
        source_segments = self.normalize_newlines(self.source_text).split("\n\n")
        target_segments = self.normalize_newlines(self.target_text).split("\n\n")

        source_segments = [source_segment.strip() for source_segment in source_segments]
        target_segments = [target_segment.strip() for target_segment in target_segments]

        return list(zip(source_segments, target_segments))
