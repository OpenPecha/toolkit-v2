from typing import Dict, List


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
