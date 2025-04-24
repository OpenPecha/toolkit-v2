class GithubRepoError(Exception):
    """Base class for exceptions in this module."""

    pass


class GithubTokenNotSetError(Exception):
    """Raised when the GitHub token is not set."""

    pass


class InvalidTokenError(GithubRepoError):
    """Raised when the GitHub token is invalid."""

    pass


class OrganizationNotFoundError(GithubRepoError):
    """Raised when the specified organization is not found."""

    pass


class FileUploadError(GithubRepoError):
    """Raised when there is an error uploading files to the repository."""

    pass


class GithubCloneError(GithubRepoError):
    """Raised when there is an error cloning github repo"""

    pass


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


class BaseUpdateFailedError(Exception):
    """Raised when the base update mechanism failed."""

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
