from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    translation = "Translation"
    root_commentory = "Root_Commentary"


class LayerEnum(Enum):
    root_segment = "Root_Segment"
    commentary = "Commentary"
    metadata = "Meta_data"


class LayerGroupEnum(Enum):
    structure_type = "Structure Type"
    resource_type = "Resource Type"


def get_annotation_category(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type == LayerEnum.metadata:
        return LayerGroupEnum.resource_type
    return LayerGroupEnum.structure_type
