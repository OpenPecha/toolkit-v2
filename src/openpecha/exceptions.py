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
