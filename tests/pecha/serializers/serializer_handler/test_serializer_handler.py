from pathlib import Path
from typing import Any, Dict, List
from unittest import TestCase

from openpecha.pecha import Pecha
from openpecha.pecha.metadata import Language
from openpecha.pecha.pecha_types import PechaType
from openpecha.pecha.serializers import (
    PECHA_SERIALIZER_REGISTRY,
    _serialize_commentary_pecha,
    _serialize_commentary_translation_pecha,
    _serialize_prealigned_commentary_pecha,
    _serialize_root_pecha,
    _serialize_root_translation_pecha,
    assign_lang_code_to_title,
)
from openpecha.utils import read_json
from tests.pecha import SharedPechaSetup

null = None


class TestFodianSerializerHandler(TestCase, SharedPechaSetup):
    def setUp(self):
        self.setup_pechas()
        self.pecha_category_vajra_cutter: List[Dict[Any, Any]] = [
            {
                "description": null,
                "short_description": null,
                "name": {
                    "en": "The Buddha's Teachings",
                    "bo": "སངས་རྒྱས་ཀྱི་བཀའ།",
                    "lzh": "佛陀教法",
                },
                "parent": null,
            },
            {
                "description": null,
                "short_description": null,
                "name": {"en": "Vajra Cutter", "bo": "རྡོ་རྗེ་གཅོད་པ།", "lzh": "金刚经"},
                "parent": "the-buddha's-teachings",
            },
        ]

        self.lzh_root_pecha = Pecha.from_path(
            Path("tests/pecha/serializers/serializer_handler/data/lzh_root/IC0482640")
        )

    def test_root_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.root_pecha)
        assert handler == _serialize_root_pecha

        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/serialized_json/serialized_root_output.json"
        )
        pecha_chain = [self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_root_pecha_serialized.json"
        )
        assert expected_serialized == updated_serialized

    def test_root_translation_pecha_with_lzh_as_source(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.root_translation_pecha)
        assert handler == _serialize_root_translation_pecha

        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/serialized_json/serialized_root_translation.json"
        )
        pecha_chain = [self.root_translation_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_root_translation_pecha_with_lzh_source_serialized.json"
        )
        assert expected_serialized == updated_serialized

    def test_root_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.root_translation_pecha)
        assert handler == _serialize_root_translation_pecha

        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/serialized_json/serialized_translation_output.json"
        )
        pecha_chain = [self.root_translation_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_root_translation_pecha_serialized.json"
        )
        assert expected_serialized == updated_serialized

    def test_commentary_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.commentary_pecha)
        assert (
            handler == _serialize_commentary_pecha
        ), f"Handler mismatch for {PechaType.commentary_pecha}"

        # bo Commentary Case
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/bo/commentary_serialized.json"
        )
        pecha_chain = [self.commentary_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_serialized/bo.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_pecha} fodian serialization failed.."

        # en Commentary Case
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/en/commentary_serialized.json"
        )
        # Emptying tgt content for Proper Testing
        serialized["target"]["books"][0]["content"] = []
        pecha_chain = [self.commentary_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_serialized/en.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_pecha} fodian serialization failed.."

        # lzh Commentary Case
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/zh/commentary_serialized.json"
        )
        # Emptying tgt content for Proper Testing
        serialized["target"]["books"][0]["content"] = []
        serialized["source"]["books"][0]["language"] = Language.literal_chinese.value
        pecha_chain = [self.commentary_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_serialized/lzh.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_pecha} fodian serialization failed.."

    def test_commentary_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.commentary_translation_pecha)

        assert (
            handler == _serialize_commentary_translation_pecha
        ), f"Handler mismatch for {PechaType.commentary_pecha}"

        # en Commentary Translation Case
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/en/commentary_serialized.json"
        )
        pecha_chain = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_translation/en.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_translation_pecha} fodian serialization failed.."

        # lzh Commentary Translation Case
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/simple/data/zh/commentary_serialized.json"
        )
        serialized["source"]["books"][0]["language"] = Language.literal_chinese.value
        pecha_chain = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_commentary_translation/lzh.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_translation_pecha} fodian serialization failed.."

    def test_prealigned_commentary_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(PechaType.prealigned_commentary_pecha)

        assert (
            handler == _serialize_prealigned_commentary_pecha
        ), f"Handler mismatch for {PechaType.commentary_pecha}"

        # bo Case
        serialized = read_json(
            "tests/pecha/serializers/pecha_db/commentary/prealigned_simple/data/expected_serialized.json"
        )
        pecha_chain = [self.commentary_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )

        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_prealigned_commentary.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.commentary_pecha} fodian serialization failed.."

    def test_prealigned_commentary_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(
            PechaType.prealigned_commentary_translation_pecha
        )

        assert (
            handler == _serialize_commentary_translation_pecha
        ), f"Handler mismatch for {PechaType.prealigned_commentary_translation_pecha}"

        # en case
        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/serialized_json/serialized_en_prealigned_commentary_translation.json"
        )
        pecha_chain = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_prealigned_commentary_translation/en.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.prealigned_commentary_translation_pecha} fodian serialization failed.."

        # lzh case
        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/serialized_json/serialized_lzh_prealigned_commentary_translation.json"
        )
        pecha_chain = [
            self.commentary_translation_pecha,
            self.commentary_pecha,
            self.root_pecha,
        ]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_prealigned_commentary_translation/lzh.json"
        )
        assert (
            expected_serialized == updated_serialized
        ), f"{PechaType.prealigned_commentary_translation_pecha} fodian serialization failed.."

    def test_prealigned_root_translation_pecha(self):
        handler = PECHA_SERIALIZER_REGISTRY.get(
            PechaType.prealigned_root_translation_pecha
        )
        assert (
            handler == _serialize_root_translation_pecha
        ), f"Handler mismatch for {PechaType.prealigned_root_translation_pecha}"

        # en Case
        serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/serialized_json/serialized_prealigned_root_translation_with_display.json"
        )
        pecha_chain = [self.root_translation_pecha, self.root_pecha]
        updated_serialized = assign_lang_code_to_title(
            handler(
                serialized,
                self.lzh_root_pecha,
                self.pecha_category_vajra_cutter,
                pecha_chain,
            )
        )
        expected_serialized = read_json(
            "tests/pecha/serializers/serializer_handler/data/expected_prealigned_root_translation_serialized.json"
        )
        assert expected_serialized == updated_serialized
