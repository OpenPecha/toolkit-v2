import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from openpecha.alignment import Alignment
from openpecha.alignment.metadata import LanguageEnum


class PechaDbSerializer:
    def __init__(self, segment_pairs: List[Dict], alignment: Alignment):
        self.segment_pairs = segment_pairs
        self.alignment = alignment

    def serialize(self, output_path: Path = Path(".")) -> Path:
        if self.alignment.pechas is None:
            raise ValueError("Alignment pechas data is missing.")

        pecha_db_json: Dict = defaultdict(lambda: defaultdict(dict))
        pecha_lang = {}
        for (
            pecha_id,
            pecha_metadata,
        ) in self.alignment.metadata.segments_metadata.items():
            metadata_ann_store = self.alignment.pechas[pecha_id].metadata
            ann_metadata: Dict = {}
            for ann in metadata_ann_store.annotations():
                ann_base = (
                    ann.target().resource(metadata_ann_store).filename().split("/")[-1]
                )
                if ann_base == f"{pecha_metadata.base}.txt":
                    for ann_data in ann:
                        key, value = ann_data.key().id(), str(ann_data.value())
                        if key in ann_metadata:
                            ann_metadata[key] = ann_metadata[key] + " " + value
                        else:
                            ann_metadata[key] = value

            if pecha_metadata.lang == LanguageEnum.tibetan:
                pecha_db_json["target"]["books"] = {
                    "title": ann_metadata["title"] if "title" in ann_metadata else "",
                    "language": "bo",
                    "version_source": f"www.github.com/PechaData/{pecha_id}/base/{pecha_metadata.base}.txt",
                    "direction": "ltr",
                    "content": [],
                }
            elif pecha_metadata.lang == LanguageEnum.english:
                pecha_db_json["source"]["books"] = {
                    "title": ann_metadata["title"] if "title" in ann_metadata else "",
                    "language": "en",
                    "version_source": f"wwww.github.com/PechaData/{pecha_id}/base/{pecha_metadata.base}.txt",
                    "direction": "ltr",
                    "content": [],
                }
            pecha_lang[pecha_id] = pecha_metadata.lang

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

        output_file = output_path / f"{self.alignment.id_}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pecha_db_json, f, ensure_ascii=False, indent=2)

        return output_file
