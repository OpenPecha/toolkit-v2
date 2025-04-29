from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    structure_annotation = "Structure_Annotation"
    variation_annotation = "Variation_Annotation"
    ocr_annotation = "Ocr_Annotation"
    language_annotation = "language_Annotation"
    segmentation_annotation = "Segmentation_Annotation"


class LayerEnum(str, Enum):
    segmentation = "Segmentation"
    alignment = "Alignment"

    chapter = "Chapter"
    pagination = "Pagination"
    durchen = "Durchen"
    sapche = "Sapche"

    ocr_confidence = "OCRConfidence"
    language = "Language"
    citation = "Citation"
    book_title = "BookTitle"


class LayerGroupEnum(Enum):
    structure_type = "Structure_Type"
    spelling_variation = "Spelling_Variation"
    ocr_confidence_type = "Ocr_Type"
    language_type = "Language_Type"
    segmentation_type = "Segmentation_Type"


def get_layer_group(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""

    if layer_type in [LayerEnum.segmentation, LayerEnum.alignment]:
        return LayerGroupEnum.segmentation_type

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.pagination,
    ]:
        return LayerGroupEnum.structure_type

    if layer_type == LayerEnum.language:
        return LayerGroupEnum.language_type

    if layer_type == LayerEnum.ocr_confidence:
        return LayerGroupEnum.ocr_confidence_type

    if layer_type == LayerEnum.durchen:
        return LayerGroupEnum.spelling_variation

    raise ValueError(f"Layer type {layer_type} has no defined LayerGroupEnum")


def get_layer_collection(layer_type: LayerEnum) -> LayerCollectionEnum:
    """return the annotation category where annotation type falls in"""

    if layer_type in [LayerEnum.segmentation, LayerEnum.alignment]:
        return LayerCollectionEnum.segmentation_annotation

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.pagination,
    ]:
        return LayerCollectionEnum.structure_annotation

    if layer_type == LayerEnum.language:
        return LayerCollectionEnum.language_annotation

    if layer_type == LayerEnum.ocr_confidence:
        return LayerCollectionEnum.ocr_annotation

    if layer_type == LayerEnum.durchen:
        return LayerCollectionEnum.variation_annotation

    raise ValueError(f"Layer type {layer_type} has no defined LayerCollectionEnum")
