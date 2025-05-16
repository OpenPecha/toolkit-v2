from pathlib import Path
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.pecha_types import PechaType
from openpecha.pecha.serializers import (
    PECHA_SERIALIZER_REGISTRY,
    _serialize_commentary_pecha,
    _serialize_commentary_translation_pecha,
)
from openpecha.utils import read_json
from tests.pecha import SharedPechaSetup


class TestFodianSerializerHandler(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()

        self.lzh_root_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/serializer_handler/data/lzh_root/ID0CDF467")
        )
        pass

    def test_commentary_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.commentary_pecha)
        assert (
            handler == _serialize_commentary_pecha
        ), f"Handler mismatch for {PechaType.commentary_pecha}"

        # BO Commentary
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/bo/commentary_serialized.json"
        )
        updated_serialized = handler(serialized, self.lzh_root_pecha)

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_serialized/bo.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_pecha} fodian serialization failed.."

        # EN Commentary
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/en/commentary_serialized.json"
        )
        # Emptying tgt content for Proper Testing
        serialized["target"]["books"][0]["content"] = []
        updated_serialized = handler(serialized, self.lzh_root_pecha)

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_serialized/en.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_pecha} fodian serialization failed.."

    def test_commentary_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.commentary_translation_pecha)

        assert (
            handler == _serialize_commentary_translation_pecha
        ), f"Handler mismatch for {PechaType.commentary_pecha}"

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
        ), f"{PechaType.commentary_translation_pecha} fodian serialization failed.."
