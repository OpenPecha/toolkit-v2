import json
import re
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

    def serialize(self, output_path: Path = Path(".")) -> Path:
        pecha_db_json: Dict = defaultdict(lambda: defaultdict(dict))
        pecha_lang = {}
        for pecha_id, pecha in self.alignment_metadata.segments_metadata.items():
            if pecha.lang == LanguageEnum.tibetan:
                pecha_db_json["target"]["books"] = {
                    "title": "pecha title",  # Work need here
                    "language": "bo",
                    "version_source": f"www.github.com/PechaData/{pecha_id}/base/{pecha.base}.txt",
                    "direction": "ltr",
                    "content": [],
                }
            elif pecha.lang == LanguageEnum.english:
                pecha_db_json["source"]["books"] = {
                    "title": "pecha title",
                    "language": "en",
                    "version_source": f"wwww.github.com/PechaData/{pecha_id}/base/{pecha.base}.txt",
                    "direction": "ltr",
                    "content": [],
                }
            pecha_lang[pecha_id] = pecha.lang

        curr_chapter: Dict = {}
        for pecha_id in pecha_lang.keys():
            curr_chapter[pecha_id] = []

        for segment_pair in self.segment_pairs:
            segment_pair_data = next(iter(segment_pair.values()))
            for pecha_id, segment in segment_pair_data.items():
                if re.match(r"^Ch \d+ ", segment):  # Start of a new chapter
                    if pecha_lang[pecha_id] == LanguageEnum.tibetan:
                        pecha_db_json["target"]["books"]["content"].append(
                            curr_chapter[pecha_id]
                        )
                    elif pecha_lang[pecha_id] == LanguageEnum.english:
                        pecha_db_json["source"]["books"]["content"].append(
                            curr_chapter[pecha_id]
                        )
                    curr_chapter[pecha_id] = []
                    continue
                curr_chapter[pecha_id].append(segment)

        """ Adding the rest of the segments """
        for pecha_id, segment in curr_chapter.items():
            if pecha_lang[pecha_id] == LanguageEnum.tibetan:
                pecha_db_json["target"]["books"]["content"].append(segment)
            elif pecha_lang[pecha_id] == LanguageEnum.english:
                pecha_db_json["source"]["books"]["content"].append(segment)

        output_file = output_path / f"{self.alignment_metadata.id_}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pecha_db_json, f, ensure_ascii=False, indent=2)

        return output_file
