# from pathlib import Path
# from typing import Dict

# from openpecha.alignment import Alignment
# from openpecha.alignment.serializers.pecha_db import PechaDbSerializer
# from openpecha.pecha import Pecha


# def test_pecha_db_serializer():
#     DATA = Path(__file__).parent / "data"
#     alignment_path = DATA / "AFB6778F8"
#     source_id, target_id = (
#         "I8A2A44D2",
#         "IA8419656",
#     )
#     pechas: Dict[str, Pecha] = {
#         source_id: Pecha.from_path(DATA / source_id),
#         target_id: Pecha.from_path(DATA / target_id),
#     }
#     alignment = Alignment.from_path(alignment_path, pechas=pechas)
#     assert isinstance(alignment, Alignment)

#     segment_pairs = list(alignment.get_segment_pairs())
#     pecha_db = PechaDbSerializer(segment_pairs, alignment)
#     output_file = pecha_db.serialize(DATA)
#     expected_output_file = DATA / "expected_output.json"

#     assert output_file.read_text() == expected_output_file.read_text()
#     output_file.unlink()


# test_pecha_db_serializer()
