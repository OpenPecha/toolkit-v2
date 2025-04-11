from unittest import TestCase

from openpecha.pecha.serializers.pecha_db.utils import (
    FormatPechaCategory,
)

null = None

pecha_category = [
    {
        "description": {
            "en": "",
            "bo": ""
        },
        "short_description": {
            "en": "",
            "bo": ""
        },
        "name": {
            "en": "Madhyamaka",
            "bo": "དབུ་མ།"
        },
        "parent": None
    },
    {
        "description": {
            "en": "",
            "bo": ""
        },
        "short_description": {
            "en": "",
            "bo": ""
        },
        "name": {
            "en": "Madhyamaka treatises",
            "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།"
        },
        "parent": "madhyamaka"
    }
]

expected_category = {
    'bo': [
        {
            'name': 'དབུ་མ།', 
            'heDesc': '', 
            'heShortDesc': ''
            }, 
        {
            'name': 'དབུ་མའི་གཞུང་སྣ་ཚོགས།', 
            'heDesc': '', 
            'heShortDesc': ''
            }
        ], 
    'en': [
        {
            'name': 'Madhyamaka', 
            'enDesc': '', 
            'enShortDesc': ''
            }, 
        {
            'name': 'Madhyamaka treatises', 
            'enDesc': '', 
            'enShortDesc': ''
            }
        ]
    }


class TestPechaCategoryFormatter(TestCase):
    def setUp(self):
        self.category = {}

    def test_get_category(self):
        formatter = FormatPechaCategory()
        category = formatter.get_category(pecha_category)
        self.assertEqual(category, expected_category)

    def test_assign_category_root(self):
        formatter = FormatPechaCategory()   
        category = formatter.get_category(pecha_category)
        new_category = formatter.assign_category(category, "root")
        self.assertEqual(
            new_category["bo"][-1]["name"], "རྩ་བ།"
        )
        self.assertEqual(
            new_category["en"][-1]["name"], "Root text"
        )

    def test_assign_category_commentary(self):
        formatter = FormatPechaCategory()
        category = formatter.get_category(pecha_category)
        new_category = formatter.assign_category(category, "commentary")
        self.assertEqual(
            new_category["bo"][-1]["name"], "འགྲེལ་བ།"
        )
        self.assertEqual(
            new_category["en"][-1]["name"], "Commentary text"
        )