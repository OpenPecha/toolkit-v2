class GithubRepoError(Exception):
    """Base class for exceptions in this module."""

    pass


class InvalidTokenError(GithubRepoError):
    """Raised when the GitHub token is invalid."""

    pass


class OrganizationNotFoundError(GithubRepoError):
    """Raised when the specified organization is not found."""

    pass


class RepositoryCreationError(GithubRepoError):
    """Raised when there is an error creating the repository."""

    pass


class FileUploadError(GithubRepoError):
    """Raised when there is an error uploading files to the repository."""

    pass


class GithubCloneError(GithubRepoError):
    """Raised when there is an error cloning github repo"""

    pass


class GithubRepoNotFoundError(GithubRepoError):
    """Raised when the specified github repo is not found"""

    pass


class FileNotFoundError(Exception):
    """Raised when the specified file is not found."""

    pass


class EmptyFileError(Exception):
    """Raised when the specified file is empty."""

    pass


class MetaDataMissingError(Exception):
    """Raised when the metadata is missing in the file."""

    pass


class MetaDataValidationError(Exception):
    """Raised when the metadata is not valid."""

    pass


class PechaCategoryNotFoundError(Exception):
    """Raised when the specified pecha category is not found."""

    pass


class BaseUpdateFailedError(Exception):
    """Raised when the base update mechanism failed."""

    pass


class AlignmentAnnotationTransferFailedError(Exception):
    """Raised when the alignment annotation transfer failed."""

    pass
