from typing import Dict


class Pecha:
    def __init__(self, pecha_id: str, segments: Dict[str, str]) -> None:
        self.pecha_id = pecha_id
        self.segments = segments
        self.base_text = "".join(segments.values())

    @classmethod
    def from_path(cls, path: str):
        pass

    @classmethod
    def from_id(cls, pecha_id: str):
        pass
