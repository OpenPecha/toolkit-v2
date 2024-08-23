import json
import re
from pathlib import Path
from typing import List, Tuple


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
