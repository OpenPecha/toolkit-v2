import csv
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
alignment_path = Path


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
        cls,
        source_path: Path,
        target_path: Path,
        root_metadata_path: Path,
        target_metadata_path: Path,
    ) -> "PlainTextNumberAlignedParser":
        """
        Create a parser instance from file paths.
        """
        source_text = source_path.read_text(encoding="utf-8")
        target_text = target_path.read_text(encoding="utf-8")
        metadata = {
            "source": metadata_from_csv(root_metadata_path),
            "target": metadata_from_csv(target_metadata_path),
        }
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
            match = re.search(r"^(\d+\.)([\s]*)", segment)
            if match:
                start = match.end(2)
                end = len(segment)
                root_segment_indices.append((idx, start, end))

            sapche_match = re.search(r"<sapche>([\s\S]*?)</sapche>", segment)
            if sapche_match:
                start = sapche_match.start(1)
                end = sapche_match.end(1)
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
            match = re.search(r"^([\d,-]+)\.([\s]*)", segment)
            if match:
                root_mapped_expression = match.group(1)
                start = match.end(2)
                end = len(segment)
                root_mapped_numbers = self.extract_root_mapped_numbers(
                    root_mapped_expression
                )
                commentary_segment_indices.append(
                    (idx, start, end, root_mapped_numbers)
                )

            sapche_match = re.search(r"<sapche>([\s\S]*?)</sapche>", segment)
            if sapche_match:
                start = sapche_match.start(1)
                end = sapche_match.end(1)
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

        splitter = re.compile(r"\n[\s\t]*\n")

        source_segments = splitter.split(self.normalize_newlines(cleaned_source_text))
        target_segments = splitter.split(self.normalize_newlines(cleaned_target_text))

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
        base_content = "\n\n".join(segments)
        basefile_name = pecha.set_base(base_content)

        if ann_type == LayerEnum.root_segment:
            self.source_basefile_name = basefile_name
        else:
            self.target_basefile_name = basefile_name

        """ annotate metadata"""
        ann_store = pecha.create_ann_store(basefile_name, LayerEnum.metadata)
        metadata = (
            self.metadata["source"]
            if ann_type == LayerEnum.root_segment
            else self.metadata["target"]
        )
        ann_store = pecha.annotate_metadata(ann_store, metadata)
        pecha.save_ann_store(ann_store, LayerEnum.metadata, basefile_name)

        del ann_store

        """ annotate root segments / commentary segments """
        ann_store = pecha.create_ann_store(basefile_name, ann_type)

        ann_resource = next(ann_store.resources())
        ann_dataset = next(ann_store.datasets())

        if ann_type == LayerEnum.root_segment:
            ann_indicies = self.mapping_ann_indicies["root_indicies"]
        else:
            ann_indicies = self.mapping_ann_indicies["commentary_indicies"]

        char_count = 0
        meaning_ann_data_id = get_uuid()
        ann_type_data_id = get_uuid()
        alignment_data_id = get_uuid()
        for idx, segment in enumerate(segments):
            """annotate meaning segments"""
            is_root_or_commentary = idx in [element[0] for element in ann_indicies]
            if is_root_or_commentary:
                match_ann_indicies = next(
                    element for element in ann_indicies if idx == element[0]
                )
                start = char_count + match_ann_indicies[1]
                end = char_count + match_ann_indicies[2]
            else:
                start = char_count
                end = char_count + len(segment)
            text_selector = Selector.textselector(
                ann_resource,
                Offset.simple(start, end),
            )
            char_count += len(segment) + 2  # 2 being length for two newline characters
            meaning_segment_ann = pecha.annotate(
                ann_store, text_selector, LayerEnum.meaning_segment, meaning_ann_data_id
            )

            if is_root_or_commentary:
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
    ) -> alignment_path:
        alignment_mapping: Dict[str, Dict] = {}
        source_pecha = Pecha.from_path(source_pecha_path)
        (
            source_ann_store,
            source_ann_store_file_path,
        ) = source_pecha.get_annotation_store(
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
        del source_dataset
        del source_ann_key

        target_pecha = Pecha.from_path(target_pecha_path)
        (
            target_ann_store,
            target_ann_store_file_path,
        ) = target_pecha.get_annotation_store(
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
        del target_dataset
        del target_ann_key

        root_segment_count = 0
        last_commentary_meaning_idx = 0
        for source_meaning_segment in source_meaning_segments:
            ann_id = get_uuid()
            root_segment = next(source_meaning_segment.annotations(), None)
            if root_segment:
                root_segment_count += 1
                """ write commentary meaning statements """
                target_pointer = last_commentary_meaning_idx
                while target_pointer < len(target_meaning_segments):
                    target_meaning_segment = target_meaning_segments[target_pointer]
                    commentary_ann = next(target_meaning_segment.annotations(), None)
                    if commentary_ann:
                        smallest_associated_root_segment = next(
                            element[3][0]
                            for element in self.mapping_ann_indicies[
                                "commentary_indicies"
                            ]
                            if target_pointer == element[0]
                        )
                        if root_segment_count <= smallest_associated_root_segment:
                            break
                    else:
                        alignment_mapping[get_uuid()] = {
                            target_pecha.id_: target_meaning_segment.id(),
                        }
                    target_pointer += 1
                    last_commentary_meaning_idx += 1

                """get the associated commentary segment"""
                related_root_segment_ids = []
                for (
                    target_meaning_segment_idx,
                    _,
                    _,
                    associated_root_segments,
                ) in self.mapping_ann_indicies["commentary_indicies"]:
                    if root_segment_count in associated_root_segments:
                        associated_meaning_ann = target_meaning_segments[
                            target_meaning_segment_idx
                        ]
                        associated_commentary_ann = next(
                            associated_meaning_ann.annotations(), None
                        )
                        if associated_commentary_ann:
                            related_root_segment_ids.append(
                                associated_commentary_ann.id()
                            )

                if len(related_root_segment_ids) == 0:
                    alignment_mapping[ann_id] = {
                        source_pecha.id_: root_segment.id(),
                    }
                    continue
                if len(related_root_segment_ids) == 1:
                    related_root_segment_ids = related_root_segment_ids[0]

                alignment_mapping[ann_id] = {
                    source_pecha.id_: root_segment.id(),
                    target_pecha.id_: related_root_segment_ids,
                }
                continue

            alignment_mapping[ann_id] = {source_pecha.id_: source_meaning_segment.id()}

        alignment_path = _mkdir(output_path / self.alignment_id)
        with open(alignment_path / "alignment.json", "w", encoding="utf-8") as f:
            json.dump(alignment_mapping, f, indent=2, ensure_ascii=False)

        """ write the metadata """
        self.metadata["source"]["pecha_id"] = source_pecha.id_
        self.metadata["target"]["pecha_id"] = target_pecha.id_

        self.metadata["source"]["base"] = self.source_basefile_name
        self.metadata["target"]["base"] = self.target_basefile_name

        self.metadata["source"]["layer"] = source_ann_store_file_path.name
        self.metadata["target"]["layer"] = target_ann_store_file_path.name

        with open(alignment_path / "metadata.json", "w", encoding="utf-8") as f:
            json.dump(self.metadata, f, indent=2, ensure_ascii=False)

        return alignment_path

    def parse(self, output_path: Path) -> alignment_path:

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

        alignment_path = self.create_alignment(
            source_pecha_path, target_pecha_path, output_path
        )
        return alignment_path


def metadata_from_csv(metadata_path: Path):
    metadata = {}

    with open(metadata_path, encoding="utf-8") as file:
        reader = csv.reader(file)
        """ Read the header to get the language codes """
        header = next(reader)
        languages = header[1:]  # Exclude the first empty column

        """ Iterate over each row and populate the metadata dictionary"""
        for row in reader:
            field_name = row[0]
            values = row[1:]

            if field_name == "lang":
                """For 'lang', only store a single string value"""
                metadata[field_name] = values[0] if values[0] else values[1]
            else:
                """Create a sub-dictionary for each field with language codes as keys"""
                field_data = {
                    languages[i]: values[i] for i in range(len(languages)) if values[i]
                }
                metadata[field_name] = field_data  # type: ignore

    return metadata
