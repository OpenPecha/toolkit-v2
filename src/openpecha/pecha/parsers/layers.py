"""
This module contains format variable for all the annotations
"""


class _attr_names:
    # Layer
    ID = "id"  # Uique id for annotation of specific Pecha or Abstract work. type: str
    ANNOTATION_TYPE = "annotation_type"  # Name of annotation, type: str
    REVISION = "revision"  # Revision number. type: int
    ANNOTATION = "annotations"  # Annotations are stored in list . type: dict
    LOCAL_ID = "local_ids"

    # Spans
    SPAN = "span"
    VOL = "vol"
    START = "start"
    END = "end"

    # Page
    IMGNUM = "imgnum"
    PAGE_INDEX = "page_index"  # Page number based on Volume specified, type: int
    PAGE_REFERENCE = "reference"  # Any reference of page, eg: img_url. type: str

    # Text
    WORK_ID = "work_id"

    # Correction
    CORRECTION = "correction"  # Correct text suggestion. type: str
    CERTAINTY = "certainty"  # Certainty of the suggested correct text. type: int

    # Peydurma
    NOTE = "note"  # syls, word or phrase to be compared to other publication

    # Archaic word
    MODERN = "modern"

    # Tsawa, Citation
    ISVERSE = "isverse"  # Boolean flag to indicate a sache in verse format or not

    # Footnote
    FOOTNOTE_REF = "footnote_ref"


def Layer(id_, type_, rev=f"{1:05}"):
    return {
        _attr_names.ID: id_,
        _attr_names.ANNOTATION_TYPE: type_,
        _attr_names.REVISION: rev,
        _attr_names.ANNOTATION: {},
    }


# Text annotation
Text = {
    "parts": [],
    "span": [],
    "work_id": "",
}  # list of SubText  # list of CrossVolSpan
