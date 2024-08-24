import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

from stam import Offset, Selector

from openpecha.config import _mkdir
from openpecha.ids import get_alignment_id, get_initial_pecha_id, get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum, LayerGroupEnum

pecha_path = Path


class PlainTextNumberAlignedParser:
    """
    Class to parse plain text lines and create aligned annotations.
    """

    def __init__(self, source_text: str, target_text: str, metadata: dict):
        self.source_text = source_text
        self.target_text = target_text
        self.metadata = metadata

    @classmethod
    def from_files(
        cls, source_path: Path, target_path: Path, metadata_path: Path
    ) -> "PlainTextNumberAlignedParser":
        """
        Create a parser instance from file paths.
        """
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        with open(metadata_path) as f:
            metadata = json.load(f)
        return cls(source_text, target_text, metadata)

    @staticmethod
    def normalize_newlines(text: str) -> str:
        text = text.strip()

        """ Replace more than two consecutive newlines  with exactly two newlines. """
        pattern = r"\n{3,}"
        text = re.sub(pattern, "\n\n", text)
        return text

    def identify_root_segments(self):
        """
        1.All the source segments are meaning segments
        2.Root segments are the segments that start with a number followed by a dot.

        Input: source_segments: List of source segments
        Output: root_segment_indices: List of indices of root segments
        """

        root_segment_indices = []
        sapche_ann_indices: List[Tuple[int, int, int]] = []

        for idx, segment in enumerate(self.source_segments):
            if re.match(r"^\d+\.", segment):
                root_segment_indices.append(idx)

            match = re.search(r"<sapche>([\s\S]*?)</sapche>", segment)
            if match:
                start = match.start(1)
                end = match.end(1)
                sapche_ann_indices.append((idx, start, end))

        """ sort the root segment indices """
        root_segment_indices.sort()
        sapche_ann_indices.sort(key=lambda x: x[0])

        return root_segment_indices, sapche_ann_indices

    @staticmethod
    def extract_root_mapped_numbers(root_mapped_expression: str):
        """
        Extract the root mapped numbers from the root mapped expression.
        """
        root_mapped_numbers: List[int] = []
        for expression in root_mapped_expression.strip().split(","):
            if "-" in expression:
                start, end = expression.split("-")
                root_mapped_numbers.extend(range(int(start), int(end) + 1))
            else:
                root_mapped_numbers.append(int(expression))

        """ sort the root mapped numbers """
        root_mapped_numbers.sort()
        return root_mapped_numbers

    def identify_comment_segments(self):
        """
        1.All target segments are meaning segments.
        2.Comment segments are the segment that starts with a number followed by a dot.
        3.One comment segment can be related/mapped/linked to more than one root segments.
        Eg notations: 2,3.   : 2nd and 3rd root segments are related to this comment segment.
                      2-5.   : 2nd to 5th root segments are related to this comment segment.
                      2-4,6. : 2nd to 4 th root segments and 6th root segment are related to this comment segment.

        4.The order of the comment segment is not particularly in the increasing order.

        For more detail explanation, refer to the following
        https://github.com/orgs/OpenPecha/projects/74/views/1?pane=issue&itemId=76094908
        """

        commentary_segment_indices = []
        sapche_ann_indices: List[Tuple[int, int, int]] = []
        for idx, segment in enumerate(self.target_segments):
            match = re.search(r"^([\d,-]+)\.", segment)
            if match:
                root_mapped_expression = match.group(1)
                root_mapped_numbers = self.extract_root_mapped_numbers(
                    root_mapped_expression
                )
                commentary_segment_indices.append((idx, root_mapped_numbers))

            match = re.search(r"<sapche>([\s\S]*?)</sapche>", segment)
            if match:
                start = match.start(1)
                end = match.end(1)
                sapche_ann_indices.append((idx, start, end))

        """ sort the comment segment indices """
        commentary_segment_indices.sort(key=lambda x: x[0])
        sapche_ann_indices.sort(key=lambda x: x[0])

        return commentary_segment_indices, sapche_ann_indices

    def parse_text_into_segments(self):
        """
        Parse the source and target texts into segment pairs.

        source segments is a list containing segments from source file.
        target segments is a list containing segments from target file.

        a.root indicies is a list of integers containing the indices of source segments
        which are root segments.

        b.sapche indicies in both root and comment segments are the indices of sapche annotations
        in the segments. List of tuple containing (segment_index, start_index, end_index)
         i)segment index is index of source of target segments
         ii)start index is the start index of sapche annotation in the particular segment
         iii)end index is the end index of sapche annotation in the particular segment

        c.comment indicies is a list of tuple containing (segment_index, root_mapped_numbers)
            i)segment index is index of target segments
            ii)root_mapped_numbers is a list of integers containing the root segments indices.It means
            which root segments are related to this comment segment.


        """

        cleaned_source_text = self.source_text.lstrip("\ufeff")
        cleaned_target_text = self.target_text.lstrip("\ufeff")

        source_segments = self.normalize_newlines(cleaned_source_text).split("\n\n")
        target_segments = self.normalize_newlines(cleaned_target_text).split("\n\n")

        self.source_segments = [
            source_segment.strip() for source_segment in source_segments
        ]
        self.target_segments = [
            target_segment.strip() for target_segment in target_segments
        ]

        root_segment_indices, root_sapche_indices = self.identify_root_segments()

        (
            commentary_segment_indices,
            commentary_sapche_indices,
        ) = self.identify_comment_segments()

        self.mapping_ann_indicies = {
            "root_indicies": root_segment_indices,
            "root_sapche_indicies": root_sapche_indices,
            "commentary_indicies": commentary_segment_indices,
            "commentary_sapche_indicies": commentary_sapche_indices,
        }

    def create_pecha(
        self, segments: List[str], ann_type: LayerEnum, output_path: Path
    ) -> pecha_path:
        """create pecha file"""
        pecha_id = get_initial_pecha_id()
        pecha_path = _mkdir(output_path / pecha_id)
        pecha = Pecha(pecha_id=pecha_id, pecha_path=pecha_path)

        """ create base file for new annotation store"""
        basefile_name = get_uuid()[:4]
        base_content = "\n\n".join(segments)
        pecha.set_base(basefile_name, base_content)

        if ann_type == LayerEnum.root_segment:
            self.source_basefile_name = basefile_name
        else:
            self.target_basefile_name = basefile_name

        """ annotate root segments / commentary segments """
        ann_store = pecha.create_ann_store(basefile_name, ann_type)

        ann_resource = next(ann_store.resources())
        ann_dataset = next(ann_store.datasets())

        if ann_type == LayerEnum.root_segment:
            ann_indicies = self.mapping_ann_indicies["root_indicies"]
        else:
            ann_indicies = [
                element[0]
                for element in self.mapping_ann_indicies["commentary_indicies"]
            ]

        char_count = 0
        meaning_ann_data_id = get_uuid()
        ann_type_data_id = get_uuid()
        alignment_data_id = get_uuid()
        for idx, segment in enumerate(segments):
            """annotate meaning segments"""
            text_selector = Selector.textselector(
                ann_resource,
                Offset.simple(char_count, char_count + len(segment)),
            )
            char_count += len(segment) + 2  # 2 being length for two newline characters
            meaning_segment_ann = pecha.annotate(
                ann_store, text_selector, LayerEnum.meaning_segment, meaning_ann_data_id
            )

            if idx in ann_indicies:
                ann_selector = Selector.annotationselector(meaning_segment_ann)
                data = [
                    {
                        "id": alignment_data_id,
                        "set": ann_dataset.id(),
                        "key": LayerGroupEnum.associated_alignment.value,
                        "value": self.alignment_id,
                    },
                ]
                pecha.annotate(
                    ann_store, ann_selector, ann_type, ann_type_data_id, data
                )
        """save root segments / commentary segments annotations"""
        pecha.save_ann_store(ann_store, ann_type, basefile_name)

        """ annotate sapche annotations """
        del ann_store  # In STAM, there is an warning on not to load multiple ann_store
        del ann_resource
        del ann_dataset

        if ann_type == LayerEnum.root_segment:
            sapche_indicies = self.mapping_ann_indicies["root_sapche_indicies"]
        else:
            sapche_indicies = self.mapping_ann_indicies["commentary_sapche_indicies"]

        ann_store = pecha.create_ann_store(basefile_name, LayerEnum.sapche)
        ann_resource = next(ann_store.resources())

        char_count = 0
        sapche_ann_data_id = get_uuid()
        for idx, segment in enumerate(segments):
            for index, start, end in sapche_indicies:
                if idx == index:
                    text_selector = Selector.textselector(
                        ann_resource,
                        Offset.simple(char_count + start, char_count + end),
                    )
                    pecha.annotate(
                        ann_store, text_selector, LayerEnum.sapche, sapche_ann_data_id
                    )
                    break
            char_count += len(segment) + 2  # 2 being length for two newline characters

        """save root segments / commentary segments annotations"""
        if ann_store.annotations_len() > 0:
            pecha.save_ann_store(ann_store, LayerEnum.sapche, basefile_name)

        return pecha_path

    def create_alignment(
        self, source_pecha_path: Path, target_pecha_path: Path, output_path: Path
    ):
        alignment_mapping: Dict[str, Dict] = {}
        source_pecha = Pecha.from_path(source_pecha_path)
        source_ann_store = source_pecha.get_annotation_store(
            self.source_basefile_name, LayerEnum.root_segment
        )
        source_dataset = next(source_ann_store.datasets())
        source_ann_key = source_dataset.key(LayerGroupEnum.structure_type.value)
        source_meaning_segments = list(
            source_dataset.data(
                source_ann_key, value=LayerEnum.meaning_segment.value
            ).annotations()
        )
        del source_ann_store

        target_pecha = Pecha.from_path(target_pecha_path)
        target_ann_store = target_pecha.get_annotation_store(
            self.target_basefile_name, LayerEnum.commentary_segment
        )
        target_dataset = next(target_ann_store.datasets())
        target_ann_key = target_dataset.key(LayerGroupEnum.structure_type.value)
        target_meaning_segments = list(
            target_dataset.data(
                target_ann_key, value=LayerEnum.meaning_segment.value
            ).annotations()
        )
        del target_ann_store

        root_ann_count = 0
        target_ann_idx = 0
        for source_meaning_segment in source_meaning_segments:
            ann_id = get_uuid()
            root_ann = next(source_meaning_segment.annotations(), None)
            if root_ann:
                root_ann_count += 1
                """ get the meaning segment with no commmentary annotation """

                """ skip the meaning segment with commentary annotation """
                while (
                    target_ann_idx < len(target_meaning_segments)
                    and next(
                        target_meaning_segments[target_ann_idx].annotations(), None
                    )
                    is not None
                ):
                    target_ann_idx += 1

                """ map the meaning segment with no commentary annotation """
                while target_ann_idx < len(target_meaning_segments):
                    target_meaning_segment = target_meaning_segments[target_ann_idx]
                    commentary_ann = next(target_meaning_segment.annotations(), None)
                    if commentary_ann:
                        break
                    alignment_mapping[get_uuid()] = {
                        target_pecha.id_: target_meaning_segment.id()
                    }
                    target_ann_idx += 1

                """get the associated commentary segment"""
                associated_root_ann_ids = []
                for (
                    meaning_ann_idx,
                    associated_commentary_segments,
                ) in self.mapping_ann_indicies["commentary_indicies"]:
                    if root_ann_count in associated_commentary_segments:
                        associated_meaning_ann = target_meaning_segments[
                            meaning_ann_idx
                        ]
                        associated_commentary_ann = next(
                            associated_meaning_ann.annotations(), None
                        )
                        if associated_commentary_ann:
                            associated_root_ann_ids.append(
                                associated_commentary_ann.id()
                            )

                alignment_mapping[ann_id] = {source_pecha.id_: root_ann.id()}
                associated_root_mapping = {
                    target_pecha.id_: associated_root_ann_id
                    for associated_root_ann_id in associated_root_ann_ids
                }
                alignment_mapping[ann_id].update(associated_root_mapping)
                continue

            alignment_mapping[ann_id] = {source_pecha.id: source_meaning_segment.id()}

        alignment_path = _mkdir(output_path / self.alignment_id)
        with open(alignment_path / "alignment.json", "w", encoding="utf-8") as f:
            json.dump(alignment_mapping, f, indent=2)

    def parse(self, output_path: Path):

        """Check if the source and target segments are already parsed"""
        neccessary_attrs = [
            "source_segments",
            "target_segments",
            "mapping_ann_indicies",
        ]
        for neccessary_attr in neccessary_attrs:
            if not hasattr(self, neccessary_attr):
                self.parse_text_into_segments()
                break

        self.alignment_id = get_alignment_id()

        source_pecha_path = self.create_pecha(
            self.source_segments, LayerEnum.root_segment, output_path
        )
        target_pecha_path = self.create_pecha(
            self.target_segments, LayerEnum.commentary_segment, output_path
        )

        self.create_alignment(source_pecha_path, target_pecha_path, output_path)
