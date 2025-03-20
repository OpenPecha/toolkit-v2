import csv
import json
import math
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, List, Optional, Union

from openpecha.config import NO_OF_CHAPTER_SEGMENT


@contextmanager
def cwd(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def get_text_direction_with_lang(lang):
    # Left-to-Right (LTR) languages
    ltr_languages = [
        "bo",  # Tibetan
        "dz",  # Dzongkha
        "en",  # English
        "es",  # Spanish
        "fr",  # French
        "hi",  # Hindi
        "ja",  # Japanese
        "ko",  # Korean
        "mn",  # Mongolian
        "mr",  # Marathi
        "ms",  # Malay
        "ne",  # Nepali
        "pt",  # Portuguese
        "ru",  # Russian
        "sw",  # Swahili
        "th",  # Thai
        "vi",  # Vietnamese
        "zh",  # Chinese (both Simplified and Traditional)
    ]

    # Right-to-Left (RTL) languages
    rtl_languages = ["ar", "he"]  # Arabic  # Hebrew

    if lang in ltr_languages:
        return "ltr"
    elif lang in rtl_languages:
        return "rtl"
    else:
        # Default to LTR if language is unknown
        return "ltr"


def parse_root_mapping(root_mapping) -> List[int]:
    """
    Parse the root_mapping into List of Integers.
    Examples:>
    Input: 1  Output: [1]
    Input: 1,2,3,4,5 Output: [1,2,3,4,5]
    Input: 1-3  Output: [1,2,3]
    Input: 1-3,5-7 Output: [1,2,3,5,6,7]
    """
    root_mapping = root_mapping.replace(" ", "").strip()
    root_mapping_list = []
    for mapping in root_mapping.split(","):
        if "-" in mapping:
            start, end = mapping.split("-")
            root_mapping_list.extend(list(range(int(start), int(end) + 1)))
        else:
            root_mapping_list.append(int(mapping))
    return root_mapping_list


def chunk_strings(strings: List[str], chunk_size=NO_OF_CHAPTER_SEGMENT):
    """
    Splits a list of strings into smaller lists of at most chunk_size elements each.

    Args:
    strings (list of str): The list of strings to be chunked.
    chunk_size (int): The maximum size of each chunk.

    Returns:
    list of list of str: A list of lists, where each inner list contains up to chunk_size elements.
    """
    return [strings[i : i + chunk_size] for i in range(0, len(strings), chunk_size)]


def get_chapter_num_from_segment_num(
    segment_num: int, no_of_chapter_segment: int = NO_OF_CHAPTER_SEGMENT
) -> int:
    """
    For commentary pecha, get the chapter number from the segment number(root mapping).
    """
    return math.ceil(segment_num / no_of_chapter_segment)


def process_segment_num_for_chapter(
    segment_num: int, no_of_chapter_segment: int = NO_OF_CHAPTER_SEGMENT
) -> int:
    return (
        segment_num % no_of_chapter_segment
        if segment_num % no_of_chapter_segment != 0
        else no_of_chapter_segment
    )


def read_csv(file_path) -> List[List[str]]:
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows


def write_csv(file_path, data) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


def load_json(fn: Union[str, Path]) -> Optional[Dict]:
    fn = Path(fn)
    if not fn.is_file():
        return None
    with fn.open(encoding="utf-8") as f:
        return json.load(f)


def dump_json(data: Dict, output_fn: Union[str, Path]) -> Path:
    """Dump data to a JSON file."""
    output_fn = Path(output_fn)
    output_fn.parent.mkdir(exist_ok=True, parents=True)
    with output_fn.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return output_fn


def load_json_str(s: str) -> Optional[Dict]:
    """Load JSON data from a string."""
    if not s:
        return None
    return json.loads(s)


# Keep existing read_json and write_json for backward compatibility
def read_json(file_path):
    """Deprecated: Use load_json instead"""
    return load_json(file_path)


def write_json(file_path, data):
    """Deprecated: Use dump_json instead"""
    return dump_json(data, file_path)
