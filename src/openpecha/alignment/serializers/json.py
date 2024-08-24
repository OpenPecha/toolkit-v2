from openpecha.alignment.alignment import Alignment
from openpecha.pecha import Pecha


class JSONSerializer:
    def __init__(self, alignment: Alignment):
        self.alignment = alignment

    def load_pechas(self, source_pecha: Pecha, target_pecha: Pecha):
        self.source_pecha = source_pecha
        self.target_pecha = target_pecha

    # def serialize(self, output_path: Path):
