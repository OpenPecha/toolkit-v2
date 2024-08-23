from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    translation = "Translation"
    root_commentory = "Root_Commentary"
    metadata = "Meta_Data"


class LayerEnum(Enum):
    root_segment = "Root_Segment"
    commentary_segment = "Commentary_Segment"
    tibetan_segment = "Tibetan_Segment"
    english_segment = "English_Segment"
    chapter = "Chapter"


class LayerGroupEnum(Enum):
    structure_type = "Structure_Type"
    translation_segment = "Translation Segment"


def get_annotation_category(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type in [LayerEnum.root_segment, LayerEnum.commentary_segment]:
        return LayerGroupEnum.structure_type
    if layer_type in [LayerEnum.tibetan_segment, LayerEnum.english_segment]:
        return LayerGroupEnum.translation_segment

    return LayerGroupEnum.structure_type
