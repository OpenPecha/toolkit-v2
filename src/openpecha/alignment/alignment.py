import json
from pathlib import Path


class Alignment:
    def __init__(self, alignment_id: str, path: Path):
        self.id_ = alignment_id
        self.path = path

    @classmethod
    def from_path(cls, alignment_path: Path):
        alignment_id = alignment_path.name

        return cls(alignment_id, alignment_path)

    @property
    def alignment_pairs(self):
        mapping_file_path = self.path / "alignment.json"
        with open(mapping_file_path) as f:
            alignment_pairs = json.load(f)
        return alignment_pairs
