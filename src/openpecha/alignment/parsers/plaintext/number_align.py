import json
import re
from pathlib import Path
from typing import List, Tuple

from stam import AnnotationStore, Offset, Selector

from openpecha.alignment.parsers.plaintext.line_align import save_stam
from openpecha.config import _mkdir
from openpecha.ids import get_alignment_id, get_initial_pecha_id, get_uuid
from openpecha.pecha.layer import LayerCollectionEnum, LayerEnum, LayerGroupEnum


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

    @staticmethod
    def identify_root_segments(source_segments: List[str]):
        """
        1.All the source segments are meaning segments
        2.Root segments are the segments that start with a number followed by a dot.

        Input: source_segments: List of source segments
        Output: root_segment_indices: List of indices of root segments
        """

        root_segment_indices = []
        sapche_ann_indices: List[Tuple[int, int, int]] = []

        for idx, segment in enumerate(source_segments):
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

    def identify_comment_segments(self, target_segments: List[str]):
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

        comment_segment_indices = []
        sapche_ann_indices: List[Tuple[int, int, int]] = []
        for idx, segment in enumerate(target_segments):
            match = re.search(r"^([\d,-]+)\.", segment)
            if match:
                root_mapped_expression = match.group(1)
                root_mapped_numbers = self.extract_root_mapped_numbers(
                    root_mapped_expression
                )
                comment_segment_indices.append((idx, root_mapped_numbers))

            match = re.search(r"<sapche>([\s\S]*?)</sapche>", segment)
            if match:
                start = match.start(1)
                end = match.end(1)
                sapche_ann_indices.append((idx, start, end))

        """ sort the comment segment indices """
        comment_segment_indices.sort(key=lambda x: x[1][0])
        sapche_ann_indices.sort(key=lambda x: x[0])

        return comment_segment_indices, sapche_ann_indices

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

        root_segment_indices, root_sapche_indices = self.identify_root_segments(
            source_segments
        )

        (
            comment_segment_indices,
            comment_sapche_indices,
        ) = self.identify_comment_segments(target_segments)

        self.mapping_ann_indicies = {
            "root_indicies": root_segment_indices,
            "root_sapche_indicies": root_sapche_indices,
            "comment_indicies": comment_segment_indices,
            "comment_sapche_indicies": comment_sapche_indices,
        }

    def parse_to_root_pecha(self, output_path: Path):
        """create new annotation store for the given annotation layer"""
        ann_store_id = get_initial_pecha_id()
        pecha_path = _mkdir(output_path / ann_store_id)
        ann_store = AnnotationStore(id=ann_store_id)

        """ create base file for new annotation store"""
        base_dir = _mkdir(pecha_path / "base")
        base_file_name = get_uuid()[:4]
        base_file_path = base_dir / f"{base_file_name}.txt"
        base_file_path.write_text(self.source_text, encoding="utf-8")
        ann_resource = ann_store.add_resource(
            id=base_file_name, filename=base_file_path.as_posix()
        )

        ann_dataset = ann_store.add_dataset(
            id=LayerCollectionEnum.root_commentory.value
        )

        """ create annotation layer in STAM """
        char_count = 0
        ann_data_id = get_uuid()
        alignment_data_id = get_uuid()
        for segment in self.source_segments:
            target = Selector.textselector(
                ann_resource,
                Offset.simple(char_count, char_count + len(segment)),
            )
            char_count += len(segment)

            ann_store.annotate(
                id=get_uuid(),
                target=target,
                data=[
                    {
                        "id": ann_data_id,
                        "set": ann_dataset.id(),
                        "key": LayerGroupEnum.structure_type.value,
                        "value": LayerEnum.meaning_segment.value,
                    },
                    {
                        "id": alignment_data_id,
                        "set": ann_dataset.id(),
                        "key": LayerGroupEnum.associated_alignment.value,
                        "value": self.alignment_id,
                    },
                ],
            )

        """save the new annotation store"""
        ann_output_dir = _mkdir(pecha_path / "layers" / base_file_name)
        ann_store_filename = f"{LayerEnum.root_segment.value}-{get_uuid()[:3]}.json"
        ann_store_path = ann_output_dir / ann_store_filename
        ann_store_path = save_stam(ann_store, output_path, ann_store_path)

    def parse(self, output_path: Path):
        _mkdir(output_path)

        """ Check if the source and target segments are already parsed """
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
        self.parse_to_root_pecha(output_path)
