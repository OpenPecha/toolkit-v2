class FileNotFoundError(Exception):
    """Raised when the specified file is not found."""

    pass


class EmptyFileError(Exception):
    """Raised when the specified file is empty."""

    pass


class MetaDataMissingError(Exception):
    """Raised when the metadata is missing."""

    pass


class MetaDataValidationError(Exception):
    """Raised when the metadata is not valid."""

    pass


class StamAnnotationStoreLoadError(Exception):
    """Raised when there is an error loading annotation store in STAM."""

    pass


class StamAddAnnotationError(Exception):
    """Raised when there is an error adding annotation in STAM."""

    pass


class ParseNotReadyForThisAnnotation(Exception):
    """Raised when the parser is not ready for this annotation."""

    pass


class InValidAnnotationLayerName(Exception):
    """Raised when the layer name is not associated with any Annotations"""

    pass


class AnnotationLayerIsNotSegmentationOrAlignment(Exception):
    """Raise when a annotation layer is not Segmentation or Alignment Layer"""

    def __init__(self, pecha_id: str, layer_name: str) -> None:
        message = f"Pecha {pecha_id} layer {layer_name} is not segmentation or alignment layer to map other layer."
        super().__init__(message)

    pass
