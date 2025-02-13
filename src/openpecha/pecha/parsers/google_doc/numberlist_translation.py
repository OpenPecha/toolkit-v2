import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from docx2python import docx2python

from openpecha.alignment.alignment import AlignmentEnum
from openpecha.config import PECHAS_PATH
from openpecha.exceptions import (
    EmptyFileError,
    FileNotFoundError,
    InvalidLanguageEnumError,
    MetaDataValidationError,
)
from openpecha.pecha import Pecha, get_aligned_root_layer
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import InitialCreationType, Language, PechaMetaData
from openpecha.pecha.parsers import BaseParser


class DocxNumberListTranslationParser(BaseParser):
    def __init__(self):
        self.number_list_regex = r"^(\d+)\)\t(.*)"

    def normalize_text(self, text: str):
        text = self.normalize_whitespaces(text)
        text = self.normalize_newlines(text)
        text = text.strip()
        return text

    @staticmethod
    def normalize_whitespaces(text: str):
        """
        If there are spaces or tab between newlines, it will be removed.
        """
        return re.sub(r"\n[\s\t]+\n", "\n\n", text)

    @staticmethod
    def normalize_newlines(text: str):
        """
        If there are more than 2 newlines continuously, it will replace it with 2 newlines.
        """
        return re.sub(r"\n{3,}", "\n\n", text)

    def extract_numbered_list(self, text: str) -> Dict[str, str]:
        """
        Extract number list from the extracted text from docx.

        Example Output:>
            {
                '1': 'དབུ་མ་དགོངས་པ་རབ་གསལ་ལེའུ་དྲུག་པ་བདེན་གཉིས་སོ་སོའི་ངོ་བོ་བཤད་པ།། ',
                '2': '2 གསུམ་པ་ལ་གཉིས། ཀུན་རྫོབ་ཀྱི་བདེན་པ་བཤད་པ་དང་། ',
                '3': '2,3 དེས་གང་ལ་སྒྲིབ་ན་ཡང་དག་ཀུན་རྫོབ་འདོད་ཅེས་པས་ཡང་དག་པའི་དོན་ལ་སྒྲིབ་པས་ཀུན་རྫོབ་བམ་སྒྲིབ་བྱེད་དུ་འདོད་ཅེས་པ་སྟེ། །',
                ...
            }
        """
        res: Dict[str, str] = {}
        for para_text in text.split("\n\n"):
            match = re.match(self.number_list_regex, para_text)
            if match:
                number = match.group(1)
                text = match.group(2)
                res[number] = text

        return res

    @staticmethod
    def get_layer_enum_with_lang(lang: str):
        if lang == Language.english.value:
            return LayerEnum.english_segment

        if lang == Language.tibetan.value:
            return LayerEnum.tibetan_segment

        if lang == Language.chinese.value:
            return LayerEnum.chinese_segment

        if lang == Language.sanskrit.value:
            return LayerEnum.sanskrit_segment

        if lang == Language.italian.value:
            return LayerEnum.italian_segment

        if lang == Language.russian.value:
            return LayerEnum.russian_segment

        raise InvalidLanguageEnumError(
            f"[Error] The language enum '{lang}' from metadata is invalid."
        )

    def extract_root_segments_anns(
        self, docx_file: Path, metadata: Dict
    ) -> Tuple[List[Dict], str]:
        """
        1.Loop through numbered text
        2.If text contains root index indentifier, save it
        3.Else save the numberlist as it is
        """
        # Normalize text
        text = docx2python(docx_file).text
        if not text:
            raise EmptyFileError(
                f"[Error] The document '{str(docx_file)}' is empty or contains only whitespace."
            )

        text = self.normalize_text(text)

        # Extract text with numbered list from docx file
        numbered_text: Dict[str, str] = self.extract_numbered_list(text)

        layer_enum = self.get_layer_enum_with_lang(metadata["language"])

        anns = []
        base = ""
        char_count = 0
        for root_idx_mapping, segment in numbered_text.items():

            curr_segment_ann = {
                layer_enum.value: {
                    "start": char_count,
                    "end": char_count + len(segment) + 1,
                },
                "root_idx_mapping": root_idx_mapping,
            }
            anns.append(curr_segment_ann)
            base += f"{segment}\n"

            char_count += len(segment) + 1
        return (anns, base)

    def parse(
        self,
        input: Union[str, Path],
        metadata: Dict[str, Any],
        output_path: Path = PECHAS_PATH,
        pecha_id: Union[str, None] = None,
    ):
        input = Path(input)
        if not input.exists():
            raise FileNotFoundError(
                f"[Error] The input file '{str(input)}' does not exist."
            )

        anns, base = self.extract_root_segments_anns(input, metadata)
        pecha, _ = self.create_pecha(anns, base, metadata, output_path, pecha_id)  # type: ignore
        return pecha

    def create_pecha(
        self,
        anns: List[Dict],
        base: str,
        metadata: Dict,
        output_path: Path,
        pecha_id: str,
    ) -> Tuple[Pecha, Path]:
        pecha = Pecha.create(output_path, pecha_id)
        basename = pecha.set_base(base)

        layer_enum = self.get_layer_enum_with_lang(metadata["language"])

        # Add meaning_segment layer
        meaning_segment_layer, layer_path = pecha.add_layer(basename, layer_enum)
        for ann in anns:
            pecha.add_annotation(meaning_segment_layer, ann, layer_enum)
        meaning_segment_layer.save()

        # set base metadata
        bases = [
            {
                basename: {
                    "source_metadata": {"total_segments": len(anns)},
                    "base_file": f"{basename}.txt",
                }
            }
        ]

        # Get layer path relative to Pecha Path
        index = layer_path.parts.index(pecha.id)
        relative_layer_path = Path(*layer_path.parts[index:])

        # Inlude Root pecha and layer information if this is a translation pecha
        if "translation_of" in metadata:
            root_pecha_id = metadata["translation_of"]
            if root_pecha_id:
                root_layer_filepath = get_aligned_root_layer(root_pecha_id)
                metadata[AlignmentEnum.translation_alignment.value] = {
                    "root": root_layer_filepath,
                    "translation": str(relative_layer_path),
                }

        try:
            pecha_metadata = PechaMetaData(
                id=pecha.id,
                parser=self.name,
                **metadata,
                bases=bases,
                initial_creation_type=InitialCreationType.google_docx,
            )
        except Exception as e:
            raise MetaDataValidationError(
                f"[Error] The metadata given was not valid. {str(e)}"
            )
        else:
            pecha.set_metadata(pecha_metadata)

        return (pecha, relative_layer_path)
