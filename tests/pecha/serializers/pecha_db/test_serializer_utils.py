from unittest import TestCase

from openpecha.pecha.serializers.pecha_db.utils import (
    format_pecha_category_from_backend,
)


class TestPechaCategoryFormatter(TestCase):
    def test_single_category(self):
        single_category = [
            {
                "description": {
                    "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།",
                    "en": "Madhyamaka treatises",
                },
                "name": {"bo": "དབུ་མ།", "en": "Madhyamaka"},
                "short_description": {"bo": "", "en": ""},
            }
        ]
        formatted_category = format_pecha_category_from_backend(single_category)
        expected_category = {
            "en": [
                {
                    "name": "Madhyamaka",
                    "enDesc": "Madhyamaka treatises",
                    "enShortDesc": "",
                }
            ],
            "bo": [
                {"name": "དབུ་མ།", "heDesc": "དབུ་མའི་གཞུང་སྣ་ཚོགས།", "heShortDesc": ""}
            ],
        }
        self.assertEqual(formatted_category, expected_category)

    def test_multiple_categories(self):
        multiple_category = [
            {
                "description": {
                    "bo": "དབུ་མའི་གཞུང་སྣ་ཚོགས།",
                    "en": "Madhyamaka treatises",
                },
                "name": {"bo": "དབུ་མ།", "en": "Madhyamaka"},
                "short_description": {"bo": "", "en": ""},
            },
            {
                "description": {"bo": "", "en": ""},
                "name": {"bo": "རྡོ་རྗེ་གཅོད་པ།", "en": "Vajra Cutter"},
                "short_description": {"bo": "", "en": ""},
            },
        ]
        formatted_category = format_pecha_category_from_backend(multiple_category)
        expected_category = {
            "en": [
                {
                    "name": "Madhyamaka",
                    "enDesc": "Madhyamaka treatises",
                    "enShortDesc": "",
                },
                {"name": "Vajra Cutter", "enDesc": "", "enShortDesc": ""},
            ],
            "bo": [
                {
                    "name": "དབུ་མ།",
                    "heDesc": "དབུ་མའི་གཞུང་སྣ་ཚོགས།",
                    "heShortDesc": "",
                },
                {"name": "རྡོ་རྗེ་གཅོད་པ།", "heDesc": "", "heShortDesc": ""},
            ],
        }
        self.assertEqual(formatted_category, expected_category)
