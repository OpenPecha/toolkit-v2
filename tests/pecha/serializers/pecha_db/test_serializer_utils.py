from unittest import TestCase

from openpecha.pecha.serializers.pecha_db.utils import (
    FormatPechaCategory,
)


class TestPechaCategoryFormatter(TestCase):
    def setUp(self):
        self.formatter = FormatPechaCategory()

    def test_assign_category_root(self):
        self.formatter.assign_category("root")
        self.assertEqual(len(self.formatter.bo_category), 1)
        self.assertEqual(len(self.formatter.en_category), 1)
        self.assertEqual(
            self.formatter.bo_category[0]["name"], "རྩ་བ།"
        )
        self.assertEqual(
            self.formatter.en_category[0]["name"], "Root text"
        )

    def test_assign_category_commentary(self):
        self.formatter.assign_category("commentary")
        self.assertEqual(len(self.formatter.bo_category), 1)
        self.assertEqual(len(self.formatter.en_category), 1)
        self.assertEqual(
            self.formatter.bo_category[0]["name"], "འགྲེལ་བ།"
        )
        self.assertEqual(
            self.formatter.en_category[0]["name"], "Commentary text"
        )