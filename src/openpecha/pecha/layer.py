from enum import Enum


class LayerEnum(Enum):
    root_segment = "Root_Segment"
    comment = "Comment"
    metadata = "Meta_data"


class LayerGroupEnum(Enum):
    structure_type = "Structure Type"
    resource_type = "Resource Type"
