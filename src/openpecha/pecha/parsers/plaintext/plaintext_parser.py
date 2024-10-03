import re
from pathlib import Path
from typing import Callable, Dict, List, Union

from stam import AnnotationStore, Offset, Selector

from openpecha.ids import get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum, get_layer_group


def count_whitespace_details(text) -> Dict:
    """Count whitespace characters at the start of the string"""
    start_whitespace_match = re.match(r"\A([\s\n]*)", text)
    start_whitespace_count = (
        len(start_whitespace_match.group(1)) if start_whitespace_match else 0
    )

    """ Count whitespace characters at the end of the string"""
    end_whitespace_match = re.search(r"([\s\n]*)\Z", text)
    end_whitespace_count = (
        len(end_whitespace_match.group(1)) if end_whitespace_match else 0
    )

    return {
        "start_whitespace": start_whitespace_count,
        "end_whitespace": end_whitespace_count,
    }


class PlainTextParser:
    def __init__(
        self,
        input: Union[str, Path],
        segmenter: Callable[[str], List[str]],
        annotation_name: str,
    ):
        self.input = input
        self.segmenter = segmenter
        self.annotation_name = annotation_name

    @staticmethod
    def segment_text(
        text: str,
        delimiter: str,
        strip_segments: bool = True,
        delimiter_length: int = 1,
    ) -> List[Dict]:
        res = []
        char_count = 0
        for segment in text.split(delimiter):
            start_whitespace_count = 0
            end_whitespace_count = 0

            if strip_segments:
                whitespace_count = count_whitespace_details(segment)
                start_whitespace_count = whitespace_count["start_whitespace"]
                end_whitespace_count = whitespace_count["end_whitespace"]
                segment = segment.strip()

            if segment:
                res.append(
                    {
                        "annotation_text": segment,
                        "start": char_count + start_whitespace_count,
                        "end": char_count
                        + len(segment)
                        + start_whitespace_count
                        - end_whitespace_count,
                    }
                )

            char_count += len(segment) + delimiter_length
        return res

    @staticmethod
    def space_segmenter(text: str, strip_segments: bool = True) -> List[Dict]:
        return PlainTextParser.segment_text(text, " ", strip_segments)

    @staticmethod
    def new_line_segmenter(text: str, strip_segments: bool = True) -> List[Dict]:
        return PlainTextParser.segment_text(text, "\n", strip_segments)

    @staticmethod
    def two_new_line_segmenter(text: str, strip_segments: bool = True) -> List[Dict]:
        return PlainTextParser.segment_text(
            text, "\n\n", strip_segments, delimiter_length=2
        )

    @staticmethod
    def regex_segmenter(
        text: str, pattern: str, group_mapping: List[str]
    ) -> List[Dict]:
        if "annotation_text" not in group_mapping:
            raise ValueError("group_mapping must contain 'annotation_text'")

        matches = re.finditer(pattern, text)
        result = []

        for match in matches:
            groups = match.groups()
            if len(groups) == len(group_mapping):
                segment_data = {group_mapping[i]: groups[i] for i in range(len(groups))}

                # Add start and end indices for the "annotation_text" group
                annotation_index = group_mapping.index("annotation_text")
                start, end = match.span(
                    annotation_index + 1
                )  # +1 because group 0 is the entire match
                segment_data["start"] = start
                segment_data["end"] = end

                result.append(segment_data)
            else:
                raise ValueError(
                    "Number of groups in pattern does not match the number of provided group meanings"
                )

        return result

    @staticmethod
    def is_annotation_name_valid(annotation_name: str) -> bool:
        return annotation_name in [layer.value for layer in LayerEnum]

    def parse(self, output_path: Path) -> Path:
        assert isinstance(self.input, str)
        segments = self.segmenter(self.input)
        """ check if annotation name is in LayerEnum """
        if not self.is_annotation_name_valid(self.annotation_name):
            raise ValueError("Invalid annotation name")

        """create pecha file"""
        pecha = Pecha.create_pecha(output_path)

        """ create base file for new annotation store"""
        basefile_name = pecha.set_base(self.input)

        """ create annotation layer """
        ann_store = pecha.create_ann_store(
            basefile_name, LayerEnum(self.annotation_name)
        )
        ann_resource = next(ann_store.resources())
        ann_dataset = next(ann_store.datasets())
        ann_type_id = get_uuid()
        for segment in segments:
            assert isinstance(segment, dict)
            text_selector = Selector.textselector(
                ann_resource, Offset.simple(segment["start"], segment["end"])
            )
            ann_data = [
                {"id": get_uuid(), "set": ann_dataset.id(), "key": k, "value": v}
                for k, v in segment.items()
                if k not in ["start", "end", "annotation_text"]
            ]
            pecha.annotate(
                ann_store,
                text_selector,
                LayerEnum(self.annotation_name),
                ann_type_id,
                ann_data,
            )
        ann_store_path = pecha.save_ann_store(
            ann_store, LayerEnum(self.annotation_name), basefile_name
        )
        return ann_store_path

    def parse_ann_on_ann(self) -> Path:
        assert isinstance(self.input, Path)
        """ check if annotation name is in LayerEnum """
        if not self.is_annotation_name_valid(self.annotation_name):
            raise ValueError("Invalid annotation name")

        pecha = Pecha.from_path(pecha_path=self.input.parents[2])

        basefile_name = self.input.parent.name
        ann_store = pecha.create_ann_store(
            basefile_name, LayerEnum(self.annotation_name)
        )
        parent_ann_store = ann_store.add_substore(filename=str(self.input))
        ann_dataset = next(ann_store.datasets())
        ann_value = Path(parent_ann_store.filename()).stem.split("-")[0]
        ann_key_value = get_layer_group(LayerEnum(ann_value)).value
        ann_key = ann_dataset.key(ann_key_value)
        ann_type_id = get_uuid()
        for ann in ann_key.data(value=ann_value).annotations():
            ann_str = str(ann)
            segments = self.segmenter(ann_str)
            for segment in segments:
                assert isinstance(segment, dict)

                if not segment["annotation_text"]:
                    continue

                selector = Selector.annotationselector(
                    annotation=ann,
                    offset=Offset.simple(segment["start"], segment["end"]),
                )
                ann_data = [
                    {"id": get_uuid(), "set": ann_dataset.id(), "key": k, "value": v}
                    for k, v in segment.items()
                    if k not in ["start", "end", "annotation_text"]
                ]
                pecha.annotate(
                    ann_store,
                    selector,
                    LayerEnum(self.annotation_name),
                    ann_type_id,
                    ann_data,
                )
        ann_store_path = pecha.save_ann_store(
            ann_store, LayerEnum(self.annotation_name), basefile_name
        )
        del ann_store

        """ To be removed later, after stam is fixed"""
        """ saving basefile path as relative  in AnnotationSubStore """
        ann_type = self.input.stem.split("-")[0]
        pecha.save_ann_store(
            AnnotationStore(file=str(self.input)),
            LayerEnum(ann_type),
            basefile_name,
            self.input.name,
        )
        return ann_store_path
