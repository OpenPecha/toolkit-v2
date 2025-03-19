from enum import Enum


class LayerCollectionEnum(Enum):
    """In STAM, this is used for setting DataSet id"""

    translation = "Translation"
    root_commentory = "Root_Commentary"
    metadata = "Meta_Data"
    structure_annotation = "Structure_Annotation"
    variation_annotation = "Variation_Annotation"
    ocr_annotation = "Ocr_Annotation"
    language_annotation = "language_Annotation"


class LayerEnum(Enum):
    # Existing v2 segments
    meaning_segment = "Meaning_Segment"
    root_segment = "Root_Segment"
    commentary_segment = "Commentary_Segment"
    tibetan_segment = "Tibetan_Segment"
    english_segment = "English_Segment"
    chinese_segment = "Chinese_Segment"
    sanskrit_segment = "Sanskrit_Segment"
    italian_segment = "Italian_Segment"
    russian_segment = "Russian_Segment"
    pecha_display_alignment_segment = "Pecha_Display_Alignment_Segment"

    # Common attributes (keeping v2 naming)
    chapter = "Chapter"
    sapche = "Sapche"  # Note: v1 had "Sabche"
    metadata = "Meta_Data"
    tsawa = "Tsawa"
    pagination = "Pagination"
    durchen = "Durchen"
    ocr_confidence = "OCRConfidence"
    language = "Language"

    # Additional attributes from v1
    index = "index"
    book_title = "BookTitle"
    sub_title = "SubTitle"
    book_number = "BookNumber"
    poti_title = "PotiTitle"
    author = "Author"
    topic = "Text"
    sub_topic = "SubText"
    citation = "Citation"
    correction = "Correction"
    error_candidate = "ErrorCandidate"
    peydurma = "Peydurma"
    pedurma_note = "PedurmaNote"
    yigchung = "Yigchung"
    archaic = "Archaic"
    footnote = "Footnote"
    segment = "Segment"
    transcription_time_span = "TranscriptionTimeSpan"


class LayerGroupEnum(Enum):
    structure_type = "Structure_Type"
    translation_segment = "Translation_Segment"
    associated_alignment = "Associated_Alignment"
    spelling_variation = "Spelling_Variation"


def get_layer_group(layer_type: LayerEnum) -> LayerGroupEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type in [
        LayerEnum.tibetan_segment,
        LayerEnum.english_segment,
        LayerEnum.chinese_segment,
        LayerEnum.sanskrit_segment,
        LayerEnum.italian_segment,
        LayerEnum.russian_segment,
        LayerEnum.pecha_display_alignment_segment,
    ]:
        return LayerGroupEnum.translation_segment

    if layer_type in [LayerEnum.root_segment, LayerEnum.commentary_segment]:
        return LayerGroupEnum.associated_alignment

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.tsawa,
        LayerEnum.meaning_segment,
        LayerEnum.pagination,
    ]:
        return LayerGroupEnum.structure_type

    if layer_type == LayerEnum.durchen:
        return LayerGroupEnum.spelling_variation

    raise ValueError(f"Layer type {layer_type} has no defined LayerGroupEnum")


def get_layer_collection(layer_type: LayerEnum) -> LayerCollectionEnum:
    """return the annotation category where annotation type falls in"""
    if layer_type in [
        LayerEnum.tibetan_segment,
        LayerEnum.english_segment,
        LayerEnum.chinese_segment,
        LayerEnum.sanskrit_segment,
        LayerEnum.italian_segment,
        LayerEnum.russian_segment,
        LayerEnum.pecha_display_alignment_segment,
    ]:
        return LayerCollectionEnum.translation

    if layer_type == LayerEnum.metadata:
        return LayerCollectionEnum.metadata

    if layer_type in [LayerEnum.root_segment, LayerEnum.commentary_segment]:
        return LayerCollectionEnum.root_commentory

    if layer_type in [
        LayerEnum.chapter,
        LayerEnum.sapche,
        LayerEnum.tsawa,
        LayerEnum.meaning_segment,
        LayerEnum.pagination,
    ]:
        return LayerCollectionEnum.structure_annotation

    if layer_type == LayerEnum.durchen:
        return LayerCollectionEnum.variation_annotation

    raise ValueError(f"Layer type {layer_type} has no defined LayerCollectionEnum")
