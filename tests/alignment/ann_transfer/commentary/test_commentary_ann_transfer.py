from pathlib import Path

from openpecha.alignment.ann_transfer import CoordinateNormalisation

DATA_DIR = Path(__file__).parent / "data"

source = {"source_pecha_path": DATA_DIR / "P2/IA6ED8F68", "source_base_name": "CCF2"}
target = {"target_pecha_path": DATA_DIR / "P1/I44F30CFF", "target_base_name": "9829"}

commentary = {
    "translation_pecha_path": DATA_DIR / "P3/IBB99C5E4",
    "translation_base_name": "E3E4",
}


if __name__ == "__main__":
    coordinate_normalisation = CoordinateNormalisation(source, target, commentary)
    coordinate_normalisation.normalise_coordinate()
