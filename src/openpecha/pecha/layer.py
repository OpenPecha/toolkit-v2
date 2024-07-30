from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    translation = "Translation"
    root_commentory = "Root_Commentary"
    metadata = "Meta_Data"


class LayerEnum(Enum):
    root_segment = "Root_Segment"
    commentary = "Commentary"


class LayerGroupEnum(Enum):
    structure_type = "Structure Type"


def get_annotation_category(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    return LayerGroupEnum.structure_type
