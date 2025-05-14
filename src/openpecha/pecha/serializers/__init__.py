from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List

from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel
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
        if root_pecha_lang not in ["bo", "lzh"]:
            raise ValueError(
                f"Pecha id: {pecha_id} points to Root Pecha: {metadata_chain[-1].id} where it language is {root_pecha_lang}.Language should be from 'bo' or 'lzh'."
            )

        match base_language:
            case "bo":
                # pecha.org website centered around bo Root text.
                pass

            case "lzh":
                # fodian.org website centered around lzh Root text.
                pass

            case _:
                raise ValueError(
                    f"Invalid base language {base_language} is passed for Serialization. Should be from 'bo' or 'lzh'."
                )
        pass
