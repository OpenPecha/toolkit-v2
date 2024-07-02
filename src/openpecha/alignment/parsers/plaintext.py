from pathlib import Path

from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha import Pecha


class PlainText:
    def __init__(self, source_text: str, target_text: str, metadata: dict):
        self.source_text = source_text
        self.target_text = target_text
        self.metadata = metadata

    @classmethod
    def from_files(cls, source_path: Path, target_path: Path, metadata: dict):
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        return cls(source_text, target_text, metadata)

    def parse(self):
        source_text_lines = self.source_text.split("\n")
        target_text_lines = self.target_text.split("\n")

        """ prepare the data for pecha creation"""
        source_pecha_id, target_pecha_id = (
            get_initial_pecha_id(),
            get_initial_pecha_id(),
        )
        source_segments = {get_uuid(): segment for segment in source_text_lines}
        target_segments = {get_uuid(): segment for segment in target_text_lines}

        source_pecha = Pecha(  # noqa
            source_pecha_id, source_segments, self.metadata["source"]
        )
        target_pecha = Pecha(  # noqa
            target_pecha_id, target_segments, self.metadata["target"]
        )

        # TODO:

        # 2. create a segment pairs [((source_pecha_id,source_segment_id), (target_pecha_id, target_segment_id)), ...]
        # 3. Create AlignmentMetadata

        """
        alignment = Alignment.from_segment_pairs(segment_pairs, metadata)
        alignment.save(path)
        """
        pass
