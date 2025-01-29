from enum import Enum


class AlignmentEnum(Enum):
    """
    This Enum values are used to specify the type of alignment in metadata.json
    """

    translation_alignment = "translation_alignments"
    commentary_alignment = "commentary_alignments"
    pecha_display_alignments = "pecha_display_alignments"
