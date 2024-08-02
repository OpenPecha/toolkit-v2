import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from openpecha.alignment import Alignment
from openpecha.alignment.metadata import LanguageEnum
from openpecha.config import LINE_BREAKERS


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
            """get annotation metadata"""
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
                pecha_db_json["target"]["books"] = [
                    {
                        "title": ann_metadata["title"]
                        if "title" in ann_metadata
                        else "",
                        "author": ann_metadata["author"]
                        if "author" in ann_metadata
                        else "",
                        "language": "bo",
                        "version_source": f"www.github.com/PechaData/{pecha_id}/base/{pecha_metadata.base}.txt",
                        "direction": "ltr",
                        "content": [],
                    }
                ]
            elif pecha_metadata.lang == LanguageEnum.english:
                pecha_db_json["source"]["books"] = [
                    {
                        "title": ann_metadata["title"]
                        if "title" in ann_metadata
                        else "",
                        "author": ann_metadata["author"]
                        if "author" in ann_metadata
                        else "",
                        "language": "en",
                        "version_source": f"www.github.com/PechaData/{pecha_id}/base/{pecha_metadata.base}.txt",
                        "direction": "ltr",
                        "content": [],
                    }
                ]
            pecha_lang[pecha_id] = pecha_metadata.lang

        pecha_segments: Dict = {}
        for pecha_id in pecha_lang.keys():
            pecha_segments[pecha_id] = []
        """ get segments of each pecha"""
        for segment_pair in self.segment_pairs:
            segment_pair_data = next(iter(segment_pair.values()))
            for pecha_id, segment in segment_pair_data.items():
                """replace newline with <br>"""
                """ place <br> after predifined line breakers"""
                segment = segment.replace("\n", "<br>")
                for line_breaker in LINE_BREAKERS:
                    segment = segment.replace(line_breaker, f"{line_breaker}<br>")

                pecha_segments[pecha_id].append(segment)

        """ add segments to json output(for pecha.org)"""
        for pecha_id, segments in pecha_segments.items():
            if pecha_lang[pecha_id] == LanguageEnum.tibetan:
                pecha_db_json["target"]["books"][0]["content"].append(segments)
            elif pecha_lang[pecha_id] == LanguageEnum.english:
                pecha_db_json["source"]["books"][0]["content"].append(segments)

        output_file = output_path / f"{self.alignment.id_}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pecha_db_json, f, ensure_ascii=False, indent=2)

        return output_file
