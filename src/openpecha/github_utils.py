import os

from github import Github
from github.GithubException import (
    BadCredentialsException,
    GithubException,
    UnknownObjectException,
)

from openpecha.config import PECHA_DATA_ORG


class GithubRepoError(Exception):
    """Base class for exceptions in this module."""

    pass


class InvalidTokenError(GithubRepoError):
    """Raised when the GitHub token is invalid."""

    pass


class OrganizationNotFoundError(GithubRepoError):
    """Raised when the specified organization is not found."""

    pass


class RepositoryExistsError(GithubRepoError):
    """Raised when the repository already exists."""

    pass


class RepositoryCreationError(GithubRepoError):
    """Raised when there is an error creating the repository."""

    pass


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise OSError("[ERROR]: GITHUB_TOKEN environment variable not set.")


def create_github_repo(repo_name: str, org_name: str = PECHA_DATA_ORG) -> bool:
    """
    Create a GitHub repository in the specified organization.

    :param org_name: The name of the GitHub organization.
    :param repo_name: The name of the repository to create.
    :return: True if the repository was created successfully, False if it already exists or an error occurred.
    """
    try:
        g = Github(GITHUB_TOKEN)
        org = g.get_organization(org_name)
        org.create_repo(repo_name)
        return True
    except BadCredentialsException:
        raise InvalidTokenError("[ERROR]: Invalid GitHub token.")
    except UnknownObjectException:
        raise OrganizationNotFoundError(
            f"[ERROR]: Organization '{org_name}' not found."
        )
    except GithubException as e:
        if e.status == 422:
            raise RepositoryExistsError(
                f"[ERROR]: Repository '{repo_name}' already exists."
            )
        else:
            raise RepositoryCreationError(
                f"[ERROR]: Failed to create repository '{repo_name}'. Error: {e.data}"
            )
    except Exception as e:
        raise GithubRepoError(f"[ERROR]: An unexpected error occurred. Error: {e}")


if __name__ == "__main__":
    create_github_repo("TSUNDUE")
