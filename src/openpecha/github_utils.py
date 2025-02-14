import os
import subprocess
import time
from pathlib import Path
from uuid import uuid4

from git import Repo
from github import Github
from github.GithubException import (
    BadCredentialsException,
    GithubException,
    UnknownObjectException,
)

from openpecha.config import GITHUB_ORG_NAME, _mkdir
from openpecha.exceptions import (
    FileUploadError,
    GithubCloneError,
    GithubRepoError,
    GithubTokenNotSetError,
    InvalidTokenError,
    OrganizationNotFoundError,
)

org = None


def _get_openpecha_data_org(org_name=GITHUB_ORG_NAME, token=None):
    """OpenPecha github org singleton."""
    global org
    if not token:
        token = os.environ.get("GITHUB_TOKEN")
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
    repo_name: str, folder_path: Path, org_name: str = GITHUB_ORG_NAME
) -> None:
    """
    Upload a folder to a GitHub repository.

    :param org_name: The name of the GitHub organization.
    :param repo_name: The name of the repository.
    :param folder_path: The local folder path to upload (as a Path object).
    """
    try:
        GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
        if not GITHUB_TOKEN:
            raise BadCredentialsException(
                "[ERROR]: GITHUB_TOKEN environment variable not set."
            )
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
    repo_name: str, output_path: Path, org_name: str = GITHUB_ORG_NAME
) -> Path:
    if not output_path.is_dir():
        raise NotADirectoryError("Given path should be directory !!!")

    target_path = output_path / repo_name

    if (target_path).exists():
        _mkdir(target_path)

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Get token from environment variable
    if not GITHUB_TOKEN:
        raise GithubTokenNotSetError("GITHUB_TOKEN environment variable not set !!!")

    repo_url = f"https://{GITHUB_TOKEN}@github.com/{org_name}/{repo_name}.git"  # noqa
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


def get_bumped_tag(repo):
    try:
        latest_release_tag = repo.get_latest_release().tag_name
    except Exception:
        return "v0.1"

    tag_number = float(latest_release_tag[1:])
    bump_tag_number = round(tag_number + 0.1, 1)
    return f"v{bump_tag_number}"


def upload_assets(release, tag_name=None, asset_paths=[]):
    if not tag_name:
        tag_name = release.tag_name
    download_url = ""
    for asset_path in asset_paths:
        asset = release.upload_asset(str(asset_path))
        download_url = asset.browser_download_url
        print(f"[INFO] Uploaded asset {asset_path}")
    return download_url


def create_release(
    repo_name,
    prerelease=False,
    asset_paths=[],
    org=None,
    token=None,
):
    repo = get_github_repo(repo_name, org, token)
    if prerelease:
        bumped_tag = uuid4().hex
        message = "Pre-release for download"
    else:
        bumped_tag = get_bumped_tag(repo)
        message = "Official Release"
    new_release = repo.create_git_release(
        bumped_tag, bumped_tag, message, prerelease=prerelease
    )
    print(f"[INFO] Created release {bumped_tag} for {repo_name}")
    asset_download_url = upload_assets(
        new_release, tag_name=bumped_tag, asset_paths=asset_paths
    )
    return asset_download_url


def commit(repo_path, message, not_includes, branch=None):
    if isinstance(repo_path, Repo):
        repo = repo_path
    else:
        repo = Repo(repo_path)

    if not branch:
        branch = repo.active_branch.name

    has_changed = False

    # add untrack fns
    for fn in repo.untracked_files:

        ignored = False
        for not_include_fn in not_includes:
            if not_include_fn in fn:
                ignored = True

        if ignored:
            continue

        if fn:
            repo.git.add(fn)
        if has_changed is False:
            has_changed = True

    # add modified fns
    if repo.is_dirty() is True:
        for fn in repo.git.diff(None, name_only=True).split("\n"):
            if fn:
                repo.git.add(fn)
            if has_changed is False:
                has_changed = True

    if has_changed is True:
        if not message:
            message = "Initial commit"
        repo.git.commit("-m", message)
        repo.git.push("origin", branch)
