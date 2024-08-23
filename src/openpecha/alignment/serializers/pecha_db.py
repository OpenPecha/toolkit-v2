import json
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Dict, List

from openpecha.alignment import Alignment
from openpecha.config import LINE_BREAKERS
from openpecha.pecha.layer import LayerEnum


class PechaDbSerializer:
    def __init__(self, segment_pairs: List[Dict], alignment: Alignment):
        self.segment_pairs = segment_pairs
        self.alignment = alignment

    def serialize(self, output_path: Path = Path(".")) -> Path:
        if self.alignment.pechas is None:
            raise ValueError("Alignment pechas data is missing.")

        pecha_db_json: Dict = defaultdict(lambda: defaultdict(dict))
        pecha_type = {}
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
                            if isinstance(ann_metadata[key], list):
                                ann_metadata[key].append(value)
                            if isinstance(ann_metadata[key], str):
                                ann_metadata[key] = [ann_metadata[key], value]
                        else:
                            ann_metadata[key] = value

            if pecha_metadata.type == LayerEnum.root_segment:
                pecha_db_json["source"]["books"] = [
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
            elif pecha_metadata.type == LayerEnum.commentary_segment:
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
            pecha_type[pecha_id] = pecha_metadata.type

        curr_chapter_number = 1
        pecha_segments: DefaultDict[str, DefaultDict[int, List[str]]] = defaultdict(
            lambda: defaultdict(list)
        )

        for pecha_id in pecha_type.keys():
            pecha_segments[pecha_id] = defaultdict(list)

        """ get segments of each pecha"""
        for segment_pair in self.segment_pairs:

            segment_pair_data = next(iter(segment_pair.values()))
            for pecha_id, segment_data in segment_pair_data.items():
                segment_data = defaultdict(lambda: "", segment_data)
                """replace newline with <br>"""
                """ place <br> after predifined line breakers"""
                segment = segment_data["string"]
                segment = segment.replace("\n", "<br>")
                for line_breaker in LINE_BREAKERS:
                    segment = segment.replace(line_breaker, f"{line_breaker}<br>")

                """ check chapter number"""
                chapter_number = (
                    int(segment_data["metadata"]["Chapter Number"])
                    if "metadata" in segment_data
                    else None
                )
                if chapter_number and chapter_number != curr_chapter_number:
                    curr_chapter_number = chapter_number

                pecha_segments[pecha_id][curr_chapter_number].append(segment)

        """ add segments to json output(for pecha.org)"""
        for pecha_id, segments in pecha_segments.items():

            for chapter_segments in segments.values():
                if pecha_type[pecha_id] == LayerEnum.root_segment:
                    pecha_db_json["source"]["books"][0]["content"].append(
                        ["".join(chapter_segments)]
                    )
                elif pecha_type[pecha_id] == LayerEnum.commentary_segment:
                    pecha_db_json["target"]["books"][0]["content"].append(
                        ["".join(chapter_segments)]
                    )

        output_file = output_path / f"{self.alignment.id_}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(pecha_db_json, f, ensure_ascii=False, indent=2)

        return output_file
