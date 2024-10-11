import os
import subprocess
import time
from pathlib import Path

from github import Github
from github.GithubException import (
    BadCredentialsException,
    GithubException,
    UnknownObjectException,
)

from openpecha.config import PECHA_DATA_ORG, _mkdir
from openpecha.exceptions import (
    FileUploadError,
    GithubCloneError,
    GithubRepoError,
    InvalidTokenError,
    OrganizationNotFoundError,
)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise OSError("[ERROR]: GITHUB_TOKEN environment variable not set.")

org = None


def _get_openpecha_data_org(org_name=None, token=None):
    """OpenPecha github org singleton."""
    global org
    if org is None:
        if not token:
            token = os.environ.get("GITHUB_TOKEN")
        if not org_name:
            org_name = os.environ["OPENPECHA_DATA_GITHUB_ORG"]
        g = Github(token)
        org = g.get_organization(org_name)
    return org


def get_github_repo(repo_name, org_name, token):
    org = _get_openpecha_data_org(org_name, token)
    repo = org.get_repo(repo_name)
    return repo


def create_github_repo(path, org_name, token, private=False, description=None):
    org = _get_openpecha_data_org(org_name, token)
    repo = org.create_repo(
        path.name,
        description=description,
        private=private,
        has_wiki=False,
        has_projects=False,
    )
    time.sleep(2)
    return repo._html_url.value


def upload_folder_to_github(
    repo_name: str, folder_path: Path, org_name: str = PECHA_DATA_ORG
) -> None:
    """
    Upload a folder to a GitHub repository.

    :param org_name: The name of the GitHub organization.
    :param repo_name: The name of the repository.
    :param folder_path: The local folder path to upload (as a Path object).
    """
    try:
        g = Github(GITHUB_TOKEN)
        org = g.get_organization(org_name)
        repo = org.get_repo(repo_name)

        for file_path in folder_path.rglob("*"):
            if file_path.is_file():
                with file_path.open("r", encoding="utf-8") as f:
                    content = f.read()

                relative_path = file_path.relative_to(folder_path)
                try:
                    repo.create_file(
                        str(relative_path), f"Upload {relative_path}", content
                    )
                    print(f"[SUCCESS]: {relative_path} uploaded successfully")
                except GithubException as e:
                    if e.status == 422:
                        # File already exists, so we update it instead
                        contents = repo.get_contents(str(relative_path))
                        repo.update_file(
                            contents.path,
                            f"Update {relative_path}",
                            content,
                            contents.sha,
                        )
                    else:
                        raise FileUploadError(
                            f"[ERROR]: Failed to upload {relative_path}. Error: {e.data}"
                        )
    except BadCredentialsException:
        raise InvalidTokenError("[ERROR]: Invalid GitHub token.")
    except UnknownObjectException:
        raise OrganizationNotFoundError(
            f"[ERROR]: Organization '{org_name}' or repository '{repo_name}' not found."
        )
    except Exception as e:
        raise GithubRepoError(f"[ERROR]: An unexpected error occurred. Error: {e}")


def clone_repo(
    repo_name: str, output_path: Path, org_name: str = PECHA_DATA_ORG
) -> Path:
    if not output_path.is_dir():
        raise NotADirectoryError("Given path should be directory !!!")

    target_path = output_path / repo_name

    if (target_path).exists():
        _mkdir(target_path)

    repo_url = f"https://github.com/{org_name}/{repo_name}.git"  # noqa
    try:
        subprocess.run(
            ["git", "clone", repo_url, str(target_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return target_path
    except subprocess.CalledProcessError as e:
        raise GithubCloneError(f"Failed to clone {repo_name}. Error: {e}")
