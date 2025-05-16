from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.pecha_types import PechaType
from openpecha.pecha.serializers import (
    PECHA_SERIALIZER_REGISTRY,
    _serialize_root_pecha,
    _serialize_root_translation_pecha,
    _serialize_commentary_pecha,
    _serialize_commentary_translation_pecha,
)
from openpecha.utils import read_json, write_json
from tests.pecha import SharedPechaSetup


class TestFodianSerializerHandler(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

        self.lzh_root_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/serializer_handler/data/lzh_root/ID0CDF467")
        )

    def test_root_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.root_pecha)
        assert handler == _serialize_root_pecha

        serialized = read_json(
            "tests/pecha/serializers/pecha_db/root/data/expected_root_output.json"
        )
        updated_serialized = handler(serialized, self.lzh_root_pecha)

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_root_pecha_serialized.json"
        )
        assert expected_serialized == updated_serialized


    def test_root_translation_pecha_with_lzh_as_source(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.root_translation_pecha)
        assert handler == _serialize_root_translation_pecha

        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/root_translation.json"
        )
        updated_serialized = handler(serialized, self.lzh_root_pecha)
        write_json("tests/pecha/serializers/serializer_handler/data/expected_root_translation_pecha_with_lzh_source_serialized.json", updated_serialized)
        # expected_serialized = read_json(
        #     "tests/pecha/serializers/serializer_handler/data/expected_root_translation_pecha_serialized.json"
        # )
        # assert expected_serialized == updated_serialized

    def test_root_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.root_translation_pecha)
        assert handler == _serialize_root_translation_pecha

        serialized = read_json(
            "tests/pecha/serializers/pecha_db/root/data/expected_translation_output.json"
        )
        updated_serialized = handler(serialized, self.lzh_root_pecha)
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_root_translation_pecha_serialized.json"
        )
        assert expected_serialized == updated_serialized


    def test_commentary_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.commentary_pecha)
        assert (
            handler == _serialize_commentary_pecha
        ), "Serializer Logic Handler not properly retrieved in case of Commentary Pecha Type."

        # Tibetan Commentary
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/bo/commentary_serialized.json"
        )
        updated_serialized = handler(serialized, self.lzh_root_pecha)

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_pecha_serialized.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), "Serializer Logic handler isnt working in Tibetan Commentary Pecha case for Fodian website."

    def test_commentary_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.commentary_translation_pecha)

        assert (
            handler == _serialize_commentary_translation_pecha
        ), "Serializer Logic Handler not properly retrieved in case of Commentary Translation Pecha Type."

        # Commentary Pecha other than Tibetan Language
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/en/commentary_serialized.json"
        )
        updated_serialized = handler(serialized, self.lzh_root_pecha)
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_translation_pecha_serialized.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), "Serializer Logic handler isnt working in Tibetan Commentary Translation Pecha case for Fodian website."
