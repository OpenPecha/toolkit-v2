from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    translation = "Translation"
    root_commentory = "Root_Commentary"
    metadata = "Meta_Data"


class LayerEnum(Enum):
    meaning_segment = "Meaning_Segment"
    root_segment = "Root_Segment"
    commentary_segment = "Commentary_Segment"
    tibetan_segment = "Tibetan_Segment"
    english_segment = "English_Segment"
    chapter = "Chapter"
    sapche = "Sapche"


class LayerGroupEnum(Enum):
    structure_type = "Structure_Type"
    translation_segment = "Translation_Segment"
    associated_alignment = "Associated_Alignment"


def get_layer_group(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type in [LayerEnum.tibetan_segment, LayerEnum.english_segment]:
        return LayerGroupEnum.translation_segment

    return LayerGroupEnum.structure_type


def get_layer_collection(layer_type: LayerEnum) -> LayerCollectionEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type in [LayerEnum.tibetan_segment, LayerEnum.english_segment]:
        return LayerCollectionEnum.translation

    return LayerCollectionEnum.root_commentory
