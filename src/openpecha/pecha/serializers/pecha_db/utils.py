from typing import Dict, List, Union

from openpecha.config import get_logger
from openpecha.exceptions import MetaDataMissingError
from openpecha.pecha import Pecha
from openpecha.utils import get_text_direction_with_lang

logger = get_logger(__name__)

class FormatPechaCategory:

    def __init__(self):
        self.bo_category = []
        self.en_category = []
        self.category = {}
        self.pecha = None
        self.bo_root_category = {
            "name": "རྩ་བ།",
            "heDesc": "",
            "heShortDesc": "",
        }
        self.en_root_category = {
            "name": "Root text",
            "enDesc": "",
            "enShortDesc": "",
        }
        self.bo_commentary_category = {
            "name": "འགྲེལ་བ།",
            "heDesc": "",
            "heShortDesc": "",
        }
        self.en_commentary_category = {
            "name": "Commentary text",
            "enDesc": "",
            "enShortDesc": "",
        }

    def get_category(self, pecha_category: Dict[str, List[Dict[str, str]]]):
        """
        Get the category of the Pecha
        """
        for cat_info in pecha_category:
            bo_name = cat_info["name"].get("bo")
            en_name = cat_info["name"].get("en")

            bo_desc = cat_info["description"].get("bo")
            en_desc = cat_info["description"].get("en")

            bo_short_desc = cat_info["short_description"].get("bo")
            en_short_desc = cat_info["short_description"].get("en")
            if self.category == {}:
                self.category = {
                    "bo": [],
                    "en": [],
                }
            self.category["bo"].append({
                "name": bo_name,
                "heDesc": bo_desc,
                "heShortDesc": bo_short_desc,
            })
            self.category["en"].append({
                "name": en_name,
                "enDesc": en_desc,
                "enShortDesc": en_short_desc,
            })
        return self.category


    def assign_category(self, type: str):
        if type == "root":
            self.bo_category.append(self.bo_root_category)
            self.en_category.append(self.en_root_category)
        else:
            self.bo_category.append(self.bo_commentary_category)
            self.en_category.append(self.en_commentary_category)


    def format_root_category(self, pecha: Pecha, pecha_category: Dict[str, List[Dict[str, str]]]):
        """
        1.Add Root section ie "རྩ་བ།" or "Root text" to category
        2.Add pecha title to category
        """
        self.get_category(pecha_category)
        self.bo_category = self.category["bo"]
        self.en_category = self.category["en"]
        self.pecha = pecha

        bo_title = get_pecha_title(self.pecha, "bo")
        en_title = get_pecha_title(self.pecha, "en")
        
        self.assign_category("root")

        self.bo_category.append({"name": bo_title, "heDesc": "", "heShortDesc": ""})
        self.en_category.append({"name": en_title, "enDesc": "", "enShortDesc": ""})

        return {"bo": self.bo_category, "en": self.en_category}


    def format_commentary_category(self, pecha: Pecha, pecha_category: Dict[str, List[Dict[str, str]]], root_title: str):
        """
        1.Add Commentary section ie "འགྲེལ་བ།" or "Commentary text" to category
        2.Add pecha title to category
        """
        self.get_category(pecha_category)
        self.bo_category = self.category["bo"]
        self.en_category = self.category["en"]
        self.pecha = pecha
        
        bo_title = get_pecha_title(self.pecha, "bo")
        en_title = get_pecha_title(self.pecha, "en")
        
        self.assign_category("commentary")

        self.bo_category.append({"name": bo_title, "heDesc": "", "heShortDesc": ""})
        self.en_category.append({"name": en_title, "enDesc": "", "enShortDesc": ""})

        mapping = {
            "base_text_titles": [root_title],
            "base_text_mapping": "many_to_one",
            "link": "Commentary",
        }

        self.category["bo"][-1].update(mapping)
        self.category["en"][-1].update(mapping)

        return self.category

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


# if __name__ == "__main__":
#     pecha_category = [
#             {
#                 "description": {
#                     "en": "",
#                     "bo": ""
#                 },
#                 "short_description": {
#                     "en": "",
#                     "bo": ""
#                 },
#                 "name": {
#                     "en": "Madhyamaka",
#                     "bo": "དབུ་མ།"
#                 },
#                 "parent": None
#             },
#             {
#                 "description": {
#                     "en": "",
#                     "bo": ""
#                 },
#                 "short_description": {
#                     "en": "",
#                     "bo": ""
#                 },
#                 "name": {
#                     "en": "Madhyamaka treatises",
#                     "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།"
#                 },
#                 "parent": "madhyamaka"
#             }
#         ]
#     FormatPechaCategory().get_category(pecha_category)
#     print(FormatPechaCategory().category)