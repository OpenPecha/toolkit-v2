import re
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from docx2python import docx2python

from openpecha.config import PECHAS_PATH, get_logger
from openpecha.exceptions import (
    EmptyFileError,
    FileNotFoundError,
    InvalidLanguageEnumError,
    MetaDataValidationError,
)
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum
from openpecha.pecha.metadata import InitialCreationType, Language, PechaMetaData
from openpecha.pecha.parsers import BaseParser

logger = get_logger(__name__)


class DocxRootParser(BaseParser):
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

    def extract_text_from_docx(self, docx_file: Path) -> str:
        text = docx2python(docx_file).text
        if not text:
            logger.warning(
                f"The docx file {str(docx_file)} is empty or contains only whitespace."
            )
            raise EmptyFileError(
                f"[Error] The document '{str(docx_file)}' is empty or contains only whitespace."
            )

        text = self.normalize_text(text)
        return text

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

        if lang == Language.hindi.value:
            return LayerEnum.hindi_segment

        logger.error(f"The language {lang} does not included in Language Enum.")  # noqa
        raise InvalidLanguageEnumError(
            f"[Error] The language enum '{lang}' from metadata is invalid."
        )

    def calculate_segment_coordinates(
        self, segments: Dict[str, str]
    ) -> Tuple[List[Dict], str]:
        """Calculate start and end positions for each segment and build base text.

        Args:
            segments: Dictionary mapping root indices to segment text

        Returns:
            Tuple containing:
            - List of dicts with start/end positions for each segment
            - Combined base text with all segments
        """
        positions = []
        base = ""
        char_count = 0

        for root_idx_mapping, segment in segments.items():
            positions.append(
                {
                    "start": char_count,
                    "end": char_count + len(segment),
                    "root_idx_mapping": root_idx_mapping,
                }
            )
            base += f"{segment}\n"
            char_count += len(segment) + 1

        return (positions, base)

    def extract_segmentation_anns(
        self, positions: List[Dict[str, int]], lang: str
    ) -> List[Dict]:
        """Create segment annotations from position information.

        Args:
            positions: List of dicts containing start/end positions and root index mappings
            lang

        Returns:
            List of annotation dictionaries
        """
        layer_enum = self.get_layer_enum_with_lang(lang)
        return [
            {
                layer_enum.value: {"start": pos["start"], "end": pos["end"]},
                "root_idx_mapping": pos["root_idx_mapping"],
            }
            for pos in positions
        ]

    def extract_segmentation_coordinates(
        self, docx_file: Path
    ) -> Tuple[List[Dict[str, int]], str]:
        """Extract text from docx and calculate coordinates for segments.

        Args:
            docx_file: Path to the docx file

        Returns:
            Tuple containing:
            - List of dicts with segment positions and root index mappings
            - Base text containing all segments
        """
        # Extract and normalize text
        text = self.extract_text_from_docx(docx_file)
        numbered_text = self.extract_numbered_list(text)
        return self.calculate_segment_coordinates(numbered_text)

    def parse(
        self,
        input: Union[str, Path],
        metadata: Dict[str, Any],
        output_path: Path = PECHAS_PATH,
        pecha_id: Union[str, None] = None,
    ) -> Pecha:
        """Parse a docx file and create a pecha.

        The process is split into three main steps:
        1. Extract text and calculate coordinates
        2. Extract segmentation annotations
        3. Initialize pecha with annotations and metadata
        """
        input = Path(input)
        if not input.exists():
            logger.error(f"The input docx file {str(input)} does not exist.")
            raise FileNotFoundError(
                f"[Error] The input docx file '{str(input)}' does not exist."
            )

        output_path.mkdir(parents=True, exist_ok=True)

        positions, base = self.extract_segmentation_coordinates(input)

        pecha = self.create_pecha(base, output_path, metadata, pecha_id)
        pecha, _ = self.add_segmentation_annotations(
            pecha, positions, metadata["language"]
        )

        logger.info(f"Pecha {pecha.id} is created successfully.")
        return pecha

    def create_pecha(
        self, base: str, output_path: Path, metadata: Dict, pecha_id: str | None
    ) -> Pecha:
        pecha = Pecha.create(output_path, pecha_id)
        pecha.set_base(base)

        try:
            pecha_metadata = PechaMetaData(
                id=pecha.id,
                parser=self.name,
                **metadata,
                bases=[],
                initial_creation_type=InitialCreationType.google_docx,
            )
        except Exception as e:
            logger.error(f"The metadata given was not valid. {str(e)}")
            raise MetaDataValidationError(
                f"[Error] The metadata given was not valid. {str(e)}"
            )
        else:
            pecha.set_metadata(pecha_metadata.to_dict())

        return pecha

    def add_segmentation_annotations(
        self, pecha: Pecha, positions: List[Dict], lang: str
    ) -> Tuple[Pecha, Path]:

        layer_enum = self.get_layer_enum_with_lang(lang)

        # Add meaning_segment layer
        basename = list(pecha.bases.keys())[0]
        meaning_segment_layer, layer_path = pecha.add_layer(basename, layer_enum)
        anns = self.extract_segmentation_anns(positions, lang)
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
        pecha_metadata = pecha.metadata.to_dict()
        pecha_metadata["bases"].extend(bases)
        pecha.set_metadata(pecha_metadata)

        # Get layer path relative to Pecha Path
        index = layer_path.parts.index(pecha.id)
        relative_layer_path = Path(*layer_path.parts[index:])

        return (pecha, relative_layer_path)
