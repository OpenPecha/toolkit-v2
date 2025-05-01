from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    STRUCTURE_ANNOTATION = "structure_annotation"
    VARIATION_ANNOTATION = "variation_annotation"
    OCR_ANNOTATION = "ocr_annotation"
    LANGUAGE_ANNOTATION = "language_annotation"
    SEGMENTATION_ANNOTATION = "segmentation_annotation"


class AnnotationType(str, Enum):
    SEGMENTATION = "segmentation"
    ALIGNMENT = "alignment"

    CHAPTER = "chapter"
    PAGINATION = "pagination"
    DURCHEN = "durchen"
    SAPCHE = "sapche"

    OCR_CONFIDENCE = "ocr_confidence"
    LANGUAGE = "language"
    CITATION = "citation"
    BOOK_TITLE = "book_title"


class LayerGroupEnum(Enum):
    STRUCTURE_TYPE = "structure_type"
    SPELLING_VARIATION = "spelling_variation"
    OCR_CONFIDENCE_TYPE = "ocr_confidence_type"
    LANGUAGE_TYPE = "language_type"
    SEGMENTATION_TYPE = "segmentation_type"


def get_layer_group(layer_type: AnnotationType) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""

    if layer_type in [AnnotationType.SEGMENTATION, AnnotationType.ALIGNMENT]:
        return LayerGroupEnum.SEGMENTATION_TYPE

    if layer_type in [
        AnnotationType.CHAPTER,
        AnnotationType.SAPCHE,
        AnnotationType.PAGINATION,
    ]:
        return LayerGroupEnum.STRUCTURE_TYPE

    if layer_type == AnnotationType.LANGUAGE:
        return LayerGroupEnum.LANGUAGE_TYPE

    if layer_type == AnnotationType.OCR_CONFIDENCE:
        return LayerGroupEnum.OCR_CONFIDENCE_TYPE

    if layer_type == AnnotationType.DURCHEN:
        return LayerGroupEnum.SPELLING_VARIATION

    raise ValueError(f"Layer type {layer_type} has no defined LayerGroupEnum")


def get_layer_collection(layer_type: AnnotationType) -> LayerCollectionEnum:
    """return the annotation category where annotation type falls in"""

    if layer_type in [AnnotationType.SEGMENTATION, AnnotationType.ALIGNMENT]:
        return LayerCollectionEnum.SEGMENTATION_ANNOTATION

    if layer_type in [
        AnnotationType.CHAPTER,
        AnnotationType.SAPCHE,
        AnnotationType.PAGINATION,
    ]:
        return LayerCollectionEnum.STRUCTURE_ANNOTATION

    if layer_type == AnnotationType.LANGUAGE:
        return LayerCollectionEnum.LANGUAGE_ANNOTATION

    if layer_type == AnnotationType.OCR_CONFIDENCE:
        return LayerCollectionEnum.OCR_ANNOTATION

    if layer_type == AnnotationType.DURCHEN:
        return LayerCollectionEnum.VARIATION_ANNOTATION

    raise ValueError(f"Layer type {layer_type} has no defined LayerCollectionEnum")
