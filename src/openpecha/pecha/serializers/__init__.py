from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel
from openpecha.pecha.metadata import Language
from openpecha.pecha.serializers.pecha_db import Serializer
from openpecha.pecha.serializers.utils import (
    find_related_pecha_id,
    get_metadatachain_from_metadatatree,
)


class BaseSerializer(ABC):
    @property
    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def serialize(
        self,
        pecha_path: Path,
        source_type: str,
    ):
        pass


class SerializerLogicHandler:
    @staticmethod
    def get_root_translation_pecha_id(
        metadatatree: List[Any], pecha_id: str, lang: str
    ) -> Optional[str]:
        """
        1. Get metadata chain from metadata tree
        2. Get Root pecha. (last element of metadata chain)
        3. Get Root Translation Pecha id by comparing with lang given.
            i.e if lang = 'lzh', get lzh root translation pecha
        """
        metadata_chain = get_metadatachain_from_metadatatree(metadatatree, pecha_id)
        root_pecha_id = metadata_chain[-1].id

        for metadata in metadatatree:
            if metadata.language == lang and metadata.translation_of == root_pecha_id:
                return metadata.id

        return None

    def serialize(
        self,
        pechatree: Dict[str, Pecha],
        metadatatree: List[Any],
        annotations: Dict[str, List[AnnotationModel]],
        pecha_category: List[Dict[str, Dict[str, str]]],
        annotation_path: str,
        base_language: str,
    ):
        pecha_id = find_related_pecha_id(annotations, annotation_path)
        if not pecha_id:
            raise ValueError(
                f"Annotation path: {annotation_path} is not present in any of Annotations: {annotations}."
            )
        metadata_chain = get_metadatachain_from_metadatatree(metadatatree, pecha_id)
        pecha_chain = [pechatree[metadata.id] for metadata in metadata_chain]  # noqa

        root_pecha_lang = metadata_chain[-1].language
        if root_pecha_lang not in [
            Language.tibetan.value,
            Language.literal_chinese.value,
        ]:
            raise ValueError(
                f"Pecha id: {pecha_id} points to Root Pecha: {metadata_chain[-1].id} where it language is {root_pecha_lang}.Language should be from 'bo' or 'lzh'."
            )

        match base_language:
            case Language.tibetan.value:
                # pecha.org website centered around bo Root text.
                if root_pecha_lang == Language.tibetan.value:
                    return Serializer().serialize(
                        pecha_chain,
                        metadata_chain,
                        annotations,
                        pecha_category,
                        annotation_path,
                    )
                if root_pecha_lang == Language.literal_chinese.value:
                    pass

            case Language.literal_chinese.value:
                # fodian.org website centered around lzh Root text.
                if root_pecha_lang == Language.tibetan.value:
                    serialized = Serializer().serialize(  # noqa
                        pecha_chain,
                        metadata_chain,
                        annotations,
                        pecha_category,
                        annotation_path,
                    )
                    lzh_root_pecha_id = self.get_root_translation_pecha_id(  # noqa
                        metadatatree, pecha_id, Language.literal_chinese.value
                    )
                    pass

                if root_pecha_lang == Language.literal_chinese.value:
                    pass

            case _:
                raise ValueError(
                    f"Invalid base language {base_language} is passed for Serialization. Should be from 'bo' or 'lzh'."
                )
        pass
