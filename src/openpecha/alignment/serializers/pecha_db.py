import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from openpecha.alignment.metadata import AlignmentMetaData, LanguageEnum


class PechaDbSerializer:
    def __init__(
        self, segment_pairs: List[Dict], alignment_metadata: AlignmentMetaData
    ):
        self.segment_pairs = segment_pairs
        self.alignment_metadata = alignment_metadata

    def serialize(self, output_path: Path = Path(".")):
        pecha_db_json: Dict = defaultdict(lambda: defaultdict(dict))
        pecha_lang = {}
        for pecha_id, pecha in self.alignment_metadata.segments_metadata.items():
            if pecha.lang == LanguageEnum.tibetan:
                pecha_db_json["target"]["books"] = {
                    "title": "pecha title",  # Work need here
                    "language": "bo",
                    "version_source": f"github.com/PechaData/{pecha}/base/{pecha.base}.txt",
                    "direction": "ltr",
                    "content": [],
                }
            elif pecha.lang == LanguageEnum.english:
                pecha_db_json["source"]["books"] = {
                    "title": "pecha title",
                    "language": "en",
                    "version_source": f"github.com/PechaData/{pecha}/base/{pecha.base}.txt",
                    "direction": "ltr",
                    "content": [],
                }
            pecha_lang[pecha_id] = pecha.lang

        for segment_pair in self.segment_pairs:
            segment_pair_data = next(iter(segment_pair.values()))
            for pecha_id, segment in segment_pair_data.items():
                if pecha_lang[pecha_id] == LanguageEnum.tibetan:
                    pecha_db_json["target"]["books"]["content"].append(segment)
                elif pecha_lang[pecha_id] == LanguageEnum.english:
                    pecha_db_json["source"]["books"]["content"].append(segment)

        with open(
            output_path / f"{self.alignment_metadata.id_}.json", "w", encoding="utf-8"
        ) as f:
            json.dump(pecha_db_json, f, ensure_ascii=False, indent=2)
