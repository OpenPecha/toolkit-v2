import json
from pathlib import Path

from openpecha.pecha.metadata import PechaMetaData

file_path = Path("metadata.json")

with open(file_path) as f:
    metadata = json.load(f)


pecha_metadata = PechaMetaData(**metadata)
print(pecha_metadata)
