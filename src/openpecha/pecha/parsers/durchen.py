import re
from pathlib import Path
from typing import Dict, List, Union

from botok.tokenizers.chunktokenizer import ChunkTokenizer

from openpecha.config import PECHAS_PATH
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.parsers import BaseParser


class DurchenParser(BaseParser):
    def __init__(self):
        self.ann_regex = r"(\(\d+\) <.+?>)"
        self.pagination_regex = r"\d+-\d+"

    def get_base_text(self, text: str):
        text = re.sub(self.pagination_regex, "", text)
        text = re.sub(self.ann_regex, "", text)
        text = text.replace(":", "")
        return text

    def parse(
        self,
        input: str,
        metadata: Union[Dict, Path],
        output_path: Path = PECHAS_PATH,
    ) -> Pecha:
        pecha = Pecha.create(output_path)

        base_text = self.get_base_text(input)
        basename = pecha.set_base(base_text)

        layer, _ = pecha.add_layer(basename, LayerEnum.durchen)

        char_walker = 0
        # Remove pagination
        input = re.sub(self.pagination_regex, "", input)
        # Normalize newlines with #
        input = input.replace("\n", "#")
        # Split the text into chunks (with anns)
        chunks = re.split(self.ann_regex, input)
        prev_chunk = chunks[0]
        for chunk in chunks:
            if re.search(self.ann_regex, chunk):
                ann = get_durchen_annotation(prev_chunk, chunk, char_walker)
                pecha.add_annotation(layer, ann, LayerEnum.durchen)
            else:
                clean_chunk = chunk.replace(":", "")
                char_walker += len(clean_chunk)
            prev_chunk = chunk

        layer.save()
        return pecha


def get_durchen_annotation(prev_chunk: str, note_chunk: str, char_walker: int):
    default_option = get_default_option(prev_chunk, note_chunk)
    start = char_walker - len(default_option)
    end = char_walker
    {
        "chapter_number": "1",
        "chapter_title": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
        "Chapter": {"start": 145, "end": 446},
    }

    ann = {"Durchen": {"start": start, "end": end}, "note": note_chunk}
    return ann


def get_default_option(prev_chunk: str, note_chunk: str):
    default_option = ""
    if "+" in note_chunk:
        return default_option
    if ":" in prev_chunk:
        match = re.search(":.*", prev_chunk)
        if match:
            default_option = match.group(
                0
            )  # Use group(0) to safely access the matched string
    else:
        syls = get_syls(prev_chunk)
        if syls:
            default_option = syls[-1]
            if default_option == "#":
                default_option = syls[-2]
    default_option = default_option.replace("#", "\n")
    default_option = default_option.replace(":", "")
    return default_option


def get_syls(text: str):
    tokenizer = ChunkTokenizer(text)

    tokens = tokenizer.tokenize()
    syls: List = []
    syl_walker = 0
    for token in tokens:
        token_string = token[1]
        if is_shad(token_string):
            try:
                syls[syl_walker - 1] += token_string
            except:  # noqa
                syls.append(token_string)
                syl_walker += 1
        else:
            syls.append(token_string)
            syl_walker += 1
    return syls


def is_shad(text):
    shads = ["། །", "།", "།།", "། "]
    if text in shads:
        return True
    return False
