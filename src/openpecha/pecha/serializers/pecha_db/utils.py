from typing import Dict, List, Union

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError
from openpecha.pecha import Pecha
from openpecha.utils import get_text_direction_with_lang

logger = get_logger(__name__)


def format_pecha_category_from_backend(
    category: List[Dict[str, Dict[str, str]]]
) -> Dict[str, List[Dict[str, str]]]:
    """
    Format the category recieved from backend to our required format.
    """
    formatted_category: Dict[str, List[Dict[str, str]]] = {"en": [], "bo": []}
    for item in category:
        en_category = {
            "name": item["name"]["en"],
            "enDesc": item["description"]["en"],
            "enShortDesc": item["short_description"]["en"],
        }
        bo_category = {
            "name": item["name"]["bo"],
            "heDesc": item["description"]["bo"],
            "heShortDesc": item["short_description"]["bo"],
        }

        formatted_category["en"].append(en_category)
        formatted_category["bo"].append(bo_category)
    return formatted_category


def get_metadata_for_pecha_org(pecha: Pecha, lang: Union[str, None] = None):
    """
    Extract required metadata from Pecha for `pecha.org` serialization
    """
    if not lang:
        lang = pecha.metadata.language.value
    direction = get_text_direction_with_lang(lang)

    title = (
        get_pecha_title(pecha, lang)
        if lang
        else get_pecha_title(pecha, pecha.metadata.language.value)
    )

    title = title if lang in ["bo", "en"] else f"{title}[{lang}]"
    source = pecha.metadata.source if pecha.metadata.source else ""

    return {
        "title": title,
        "language": lang,
        "versionSource": source,
        "direction": direction,
        "completestatus": "done",
    }


def get_pecha_title(pecha: Pecha, lang: str):
    pecha_title = pecha.metadata.title
    if isinstance(pecha_title, dict):
        title = pecha_title.get(lang.lower()) or pecha_title.get(lang.upper())

    if title is None or title == "":
        logger.error(
            f"[Error] {lang.upper()} title not available inside metadata for {pecha.id} for Serialization."
        )
        raise MetaDataMissingError(
            f"[Error] {lang.upper()} title not available inside metadata for {pecha.id} for Serialization."
        )

    return title
