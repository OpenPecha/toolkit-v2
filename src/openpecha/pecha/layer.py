from enum import Enum


class AnnotationCollectionType(Enum):
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


class AnnotationGroupType(Enum):
    STRUCTURE_TYPE = "structure_type"
    SPELLING_VARIATION = "spelling_variation"
    OCR_CONFIDENCE_TYPE = "ocr_confidence_type"
    LANGUAGE_TYPE = "language_type"
    SEGMENTATION_TYPE = "segmentation_type"


def get_annotation_group_type(layer_type: AnnotationType) -> AnnotationGroupType:
    """return the annotation category where annotation type falls in"""

    if layer_type in [AnnotationType.SEGMENTATION, AnnotationType.ALIGNMENT]:
        return AnnotationGroupType.SEGMENTATION_TYPE

    if layer_type in [
        AnnotationType.CHAPTER,
        AnnotationType.SAPCHE,
        AnnotationType.PAGINATION,
    ]:
        return AnnotationGroupType.STRUCTURE_TYPE

    if layer_type == AnnotationType.LANGUAGE:
        return AnnotationGroupType.LANGUAGE_TYPE

    if layer_type == AnnotationType.OCR_CONFIDENCE:
        return AnnotationGroupType.OCR_CONFIDENCE_TYPE

    if layer_type == AnnotationType.DURCHEN:
        return AnnotationGroupType.SPELLING_VARIATION

    raise ValueError(f"Layer type {layer_type} has no defined AnnotationGroupType")


def get_annotation_collection_type(
    layer_type: AnnotationType,
) -> AnnotationCollectionType:
    """return the annotation category where annotation type falls in"""

    if layer_type in [AnnotationType.SEGMENTATION, AnnotationType.ALIGNMENT]:
        return AnnotationCollectionType.SEGMENTATION_ANNOTATION

    if layer_type in [
        AnnotationType.CHAPTER,
        AnnotationType.SAPCHE,
        AnnotationType.PAGINATION,
    ]:
        return AnnotationCollectionType.STRUCTURE_ANNOTATION

    if layer_type == AnnotationType.LANGUAGE:
        return AnnotationCollectionType.LANGUAGE_ANNOTATION

    if layer_type == AnnotationType.OCR_CONFIDENCE:
        return AnnotationCollectionType.OCR_ANNOTATION

    if layer_type == AnnotationType.DURCHEN:
        return AnnotationCollectionType.VARIATION_ANNOTATION

    raise ValueError(f"Layer type {layer_type} has no defined AnnotationCollectionType")
