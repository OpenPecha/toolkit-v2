class PlainText:
    def __init__(self, source_text: str, target_text: str):
        self.source_text = source_text
        self.traget_text = target_text

    @classmethod
    def from_files(cls, source_path: str, target_path: str):
        source_text = open(source_path).read()
        target_text = open(target_path).read()
        return cls(source_text, target_text)

    def parse(self, metadata: dict):
        # source_segments = self.source_text.split("\n")
        # target_segments = self.target_text.split("\n")

        # TODO:
        # 1. Create pecha with segment layers for source and target text
        # 2. create a segment pairs [((source_pecha_id,source_segment_id), (target_pecha_id, target_segment_id)), ...]
        # 3. Create AlignmentMetadata

        """
        alignment = Alignment.from_segment_pairs(segment_pairs, metadata)
        alignment.save(path)
        """
        pass
