import re
from pathlib import Path
from typing import Dict, List

from stam import Offset, Selector

from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum


def filter_pipeline(text: str, pipelist: List):
    """
    input: text, list of filtering pipes
    output: True if any of the pipe returns True, False otherwise
    """
    for pipe in pipelist:
        if pipe(text):
            return True
    return False


def english_filter_pipe(text: str):
    """
    input: text
    output: True if text contains english characters, False otherwise
    """
    return bool(re.search(r"[a-zA-Z]", text))


def symbol_filter_pipe(text: str):
    """
    input: text
    output: True if text contains symbols, False otherwise
    """
    return bool(re.search(r"[-\"\'$\*\+\?\|\[\]\{\}\;\(\)]", text))


class PechaFrameWork:
    def __init__(self, input: str, metadata: Dict = None):
        self.input = input
        self.meta_data = {} if not metadata else metadata
        self.data = self.preprocess()
        self.output = None

    def parser_pipeline(self, pipelist: List):
        """
        reads the list of pipes and runs them in sequence
        if a pipe is a string, call built-in pipe,
        if it is a function, call the function
        """
        for pipe in pipelist:
            if isinstance(pipe, str):
                getattr(self, pipe)()
            else:
                pipe(self.data)

    def preprocess(self) -> Dict:
        """
        Preprocess the input text by splitting it into atomic units.
        """
        splited_strings = [x for x in re.split(r"([\s\n])", self.input) if x != ""]
        return {"raw_string": splited_strings}

    def calculate_char_positions(self, index_start, index_end):
        """
        Calculates char_start and char_end based on the start and end indexes.
        """
        char_start = sum(len(self.data["raw_string"][i]) for i in range(index_start))
        char_end = char_start + sum(
            len(self.data["raw_string"][i]) for i in range(index_start, index_end + 1)
        )
        return char_start, char_end

    def chapter_parser_pipe(self):
        """
        Input is self.data.
        Process is to group all the lines within the same chapter together.
        Output is to update self.data by including the chapter information.
        """
        chapter_number_regex = r"\Ach(\d+)-"
        chapter_name_regex = r"-\"([\u0F00-\u0FFF]+)\""

        previous_chapter_data = None  # Keep track of the previous chapter
        found_chapter = False
        self.data["Chapter"] = []
        for i, input_line in enumerate(self.data["raw_string"]):
            if input_line in [" ", "\n"]:
                continue

            chapter_data = {}

            # Check for chapter number
            chapter_number_match = re.match(chapter_number_regex, input_line)
            if chapter_number_match:
                chapter_number = chapter_number_match.group(1)
                chapter_data["number"] = chapter_number
                found_chapter = True

            # Check for chapter name
            chapter_name_match = re.search(chapter_name_regex, input_line)
            if chapter_name_match:
                chapter_name = chapter_name_match.group(1)
                chapter_data["name"] = chapter_name
                found_chapter = True

            # Update input if chapter data is found
            if chapter_data:
                chapter_data["index_start"] = (
                    i + 2
                )  # Add two to skip chapter number and name

                # If there's a previous chapter, update its index_end
                if previous_chapter_data:
                    previous_chapter_data["index_end"] = (
                        i - 1
                    )  # End at the line before the current chapter starts

                # Append the new chapter data
                self.data["Chapter"].append(chapter_data)

                # Set current chapter as the previous for the next iteration
                previous_chapter_data = chapter_data

        # After the loop, update the last chapter's index_end to the end of the data
        if previous_chapter_data and found_chapter:
            previous_chapter_data["index_end"] = len(self.data["raw_string"]) - 1

        if self.data["Chapter"] == []:
            del self.data["Chapter"]

        return self.data

    def tsawa_parser_pipe(self):
        """
        Input is self.data.
        Process is to look inside and check for tsawa(String separated by new line).
        Output is to update self.data by including the tsawa information.
        """
        index_start = 0

        """ filter out the atomic unit strings that are not tsawa """
        filter_pipeline_definition = [english_filter_pipe, symbol_filter_pipe]
        found_tsawa = False
        self.data["Tsawa"] = []
        for i, input_line in enumerate(self.data["raw_string"]):
            if input_line in [" ", "\n"]:
                continue

            if filter_pipeline(input_line, filter_pipeline_definition):
                index_end = i
                if index_start == index_end:
                    index_start = i + 1
                    continue
                tsawa_data = {
                    "index_start": index_start,
                    "index_end": index_end,
                }

                self.data["Tsawa"].append(tsawa_data)

                index_start = i + 1
                continue

            if i + 1 >= len(self.data["raw_string"]):
                continue

            if (
                self.data["raw_string"][i + 1] == "\n"
                and self.data["raw_string"][i + 2] == "\n"
            ):

                index_end = i
                tsawa_data = {
                    "index_start": index_start,
                    "index_end": index_end,
                }
                self.data["Tsawa"].append(tsawa_data)
                found_tsawa = True
                index_start = i + 3

        tsawa_data = {
            "index_start": index_start,
            "index_end": len(self.data["raw_string"]) - 1,
        }
        if found_tsawa:
            self.data["Tsawa"].append(tsawa_data)

        if self.data["Tsawa"] == []:
            del self.data["Tsawa"]

        return self.data

    @staticmethod
    def is_annotation_name_valid(annotation_name: str) -> bool:
        return annotation_name in [layer.value for layer in LayerEnum]

    def pecha_convertor_pipeline(self, anns_list: List[str], output_path: Path):
        """
        reads the list of annotations and convert them to stam in sequence
        the annotation string should contain in the self.data
        """
        for ann_name in anns_list:
            assert ann_name in self.data, f"{ann_name} not found in self.data"
            assert self.is_annotation_name_valid(
                ann_name
            ), f"{ann_name} is not a valid annotation name"

        if not output_path.exists():
            output_path.mkdir(parents=True, exist_ok=True)

        """create pecha file"""
        pecha_id = get_initial_pecha_id()
        pecha_path = _mkdir(output_path / pecha_id)
        pecha = Pecha(pecha_id=pecha_id, pecha_path=pecha_path)

        """ create base file for new annotation store"""
        basefile_name, base_content = get_uuid()[:4], self.input
        pecha.set_base(basefile_name, base_content)

        pecha_ann_file_paths = []

        for ann_name in anns_list:
            """create annotation layer"""
            ann_store = pecha.create_ann_store(basefile_name, LayerEnum(ann_name))
            ann_resource = next(ann_store.resources())
            ann_dataset = next(ann_store.datasets())
            ann_type_id = get_uuid()
            for ann_info in self.data[ann_name]:
                assert isinstance(ann_info, dict)

                char_start, char_end = self.calculate_char_positions(
                    ann_info["index_start"], ann_info["index_end"]
                )
                text_selector = Selector.textselector(
                    ann_resource, Offset.simple(char_start, char_end)
                )
                ann_data = [
                    {"id": get_uuid(), "set": ann_dataset.id(), "key": k, "value": v}
                    for k, v in ann_info.items()
                    if k not in ["index_start", "index_end"]
                ]
                pecha.annotate(
                    ann_store,
                    text_selector,
                    LayerEnum(ann_name),
                    ann_type_id,
                    ann_data,
                )
            ann_store_path = pecha.save_ann_store(  # noqa
                ann_store, LayerEnum(ann_name), basefile_name
            )
            pecha_ann_file_paths.append(ann_store_path)

        return pecha_ann_file_paths
