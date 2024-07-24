from enum import Enum


class LayerEnum(Enum):
    root_segment = "Root_Segment"
    comment = "Comment"
    metadata = "Meta_data"


class LayerGroupEnum(Enum):
    structure_type = "Structure Type"
    resource_type = "Resource Type"


def get_annotation_category(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type == LayerEnum.metadata:
        return LayerGroupEnum.resource_type
    return LayerGroupEnum.structure_type
