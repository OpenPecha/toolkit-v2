import enum
import os
import shutil
from pathlib import Path
from typing import Optional

import git
from git import GitCommandError, Repo
from github import Github

from openpecha.config import GITHUB_ORG_NAME
from openpecha.github_utils import create_github_repo

URL: str


class Storages(enum.Enum):
    GITHUB = enum.auto()


def _getenv(name, optional):
    env = os.getenv(name)
    if env:
        return env
    elif optional:
        return env
    else:
        raise RuntimeError(f"Please set {name} environment variable")


def _get_value(value, env_name, optional=False):
    return value if value else _getenv(env_name, optional)


def get_authenticated_remote_url(url, org, token):
    old_url = url.split("//")
    auth_remote_url = f"{old_url[0]}//{org}:{token}@{old_url[1]}"  # noqa
    return auth_remote_url


def setup_auth_for_new_repo(repo, org, token, remote_url):
    auth_remote_url = get_authenticated_remote_url(remote_url, org, token)
    repo.create_remote("origin", auth_remote_url)
    return repo


def is_repo_authenticated(repo) -> bool:
    remote_url = repo.remote().url
    if "@" in remote_url:
        return True
    return False


def setup_auth_for_old_repo(repo, org, token):
    remote_url = repo.remote().url
    if is_repo_authenticated(repo):
        return repo
    auth_remote_url = get_authenticated_remote_url(remote_url, org, token)
    repo.remote().set_url(auth_remote_url)
    return repo


def commit_and_push(repo, message, branch=None):
    try:
        if not branch:
            branch = repo.active_branch.name
        repo.git.add("-A")

        # Check if there are changes to commit
        if not repo.is_dirty(untracked_files=True):
            # "No changes to commit. Working tree is clean.
            return

        repo.git.commit("-m", message)
        repo.git.push("-u", "origin", branch)
    except GitCommandError as e:
        print(f"Git command error: {e}")


class Storage:
    def add_dir(
        self,
        path: Path,
        description: str,
        is_private: bool = False,
        branch: Optional[str] = None,
    ):
        raise NotImplementedError

    def remove_dir_with_name(self, name: str):
        raise NotImplementedError

    def remove_dir_with_path(self, path: Path):
        raise NotImplementedError


class GithubStorage(Storage):
    """class representing Github Storage

    This storage create, update, and delete github repo and files

    Args:
        org (str, optional): github organization name
        token (str, optional): github oauth token
        username (str, optional): github username
        email (str, optional): github linked email

    """

    def __init__(
        self,
        org: Optional[str] = None,
        token: Optional[str] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ):
        self.org_name = GITHUB_ORG_NAME
        self.token = _get_value(token, "GITHUB_TOKEN")
        self._username = _get_value(username, "GITHUB_USERNAME", optional=True)
        self._email = _get_value(email, "GITHUB_EMAIL", optional=True)
        self._org = None

    @property
    def org(self):
        if not self._org:
            self._org = Github(self.token).get_organization(self.org_name)
        return self._org

    @property
    def username(self):
        if not self._username:
            raise RuntimeError(
                "Please set usename attr or env variable GITHUB_USERNAME."
            )
        return self._username

    @property
    def email(self):
        if not self._email:
            raise RuntimeError("Please set email attr or env variable GITHUB_EMAIL.")
        return self._email

    def _init_local_repo(self, path: Path, remote_url: str):
        repo = Repo.init(path, initial_branch="main")
        repo = setup_auth_for_new_repo(repo, self.org_name, self.token, remote_url)
        repo.config_writer().set_value("user", "name", self.username).release()
        repo.config_writer().set_value("user", "email", self.email).release()
        return repo

    def _init_remote_repo(self, path: Path, description: str, is_private: bool):
        """Creates remote repo in Github and returns it's url."""
        remote_repo_url = create_github_repo(
            path=path,
            org_name=self.org_name,
            token=self.token,
            private=is_private,
            description=description,
        )
        return remote_repo_url

    def is_git_repo(self, path):
        try:
            _ = git.Repo(path).git_dir
            return True
        except git.exc.InvalidGitRepositoryError:
            return False

    def get_authenticated_repo_remote_url(self, repo_name: str):
        return f"https://{self.username}:{self.token}@github.com/{self.org_name}/{repo_name}.git"  # noqa

    def add_dir(
        self,
        path: Path,
        description: str,
        is_private: bool = False,
        branch: Optional[str] = None,
    ):
        """dir local dir to github."""
        remote_repo_url = self._init_remote_repo(
            path=path, description=description, is_private=is_private
        )
        local_repo = self._init_local_repo(path=path, remote_url=remote_repo_url)
        commit_and_push(repo=local_repo, message="Initial commit", branch=branch)
        return local_repo

    def remove_dir_with_name(self, name: str):
        repo = self.org.get_repo(name)
        repo.delete()

    def remove_dir_with_path(self, path: Path):
        """Remove repo with local path, assumes that local and remote name is same."""
        repo = self.org.get_repo(path.name)
        repo.delete()
        shutil.rmtree(str(path))

    def get_dir_with_name(self, name: str):
        repo = self.org.get_repo(name)
        return repo

    def get_dir_with_path(self, path: Path):
        repo = self.org.get_repo(path.name)
        return repo

    def add_file(
        self, dir_name: str, path: str, content: str, message: str, update=False
    ):
        """add file to `name` repo.

        Args:
            dir_name: name of repo to add file to.
            path: path to add the file.
            content: content of the file.
            message: git commit message.
        """

        repo = self.org.get_repo(dir_name)
        if update:
            old_content = repo.get_contents(path)
            repo.update_file(old_content.path, message, content, old_content.sha)
        else:
            repo.create_file(path, message, content)

    def get_file(self, dir_name, path: str, branch="master"):
        repo = self.org.get_repo(dir_name)
        contents = repo.get_contents(path, ref=branch)
        return contents

    def remove_file(
        self, dir_name: str, path: str, message: str, branch: str = "master"
    ):
        repo = self.org.get_repo(dir_name)
        contents = repo.get_contents(path, ref=branch)
        repo.delete_file(contents.path, message, contents.sha, branch=branch)


def update_git_folder(update_source_folder_path: Path, update_dest_folder_path: Path):
    # delete files from the new repo
    for file in update_dest_folder_path.glob("*"):
        if file.name in [".git", ".github"]:
            continue

        if file.is_dir():
            shutil.rmtree(file)
        else:
            file.unlink()

    # Copy files from input data dir to new git repo
    for file in update_source_folder_path.rglob("*"):
        if file.is_file():
            relative_path = file.relative_to(update_source_folder_path)
            dest_path = update_dest_folder_path / relative_path

            dest_path.parent.mkdir(parents=True, exist_ok=True)

            shutil.copy2(file, dest_path)


def update_github_repo(input_data_dir: Path, repo_path: Path):
    """
    Overwrite the files in the github repo with the files in the input data dir
    1. Clone the repo from the github organization
    2. Delete files from the new repo
    2. Copy files from input data dir to new git repo
    3. Commit and push the changes in main branch
    """

    update_git_folder(input_data_dir, repo_path)

    # Commit and push the changes in main branch
    local_repo = Repo(repo_path)
    # Get Git user details from environment variables
    git_user_name = os.getenv("GITHUB_USERNAME")
    git_user_email = os.getenv("GITHUB_EMAIL")

    with local_repo.config_writer() as config:
        config.set_value("user", "name", git_user_name)
        config.set_value("user", "email", git_user_email)

    commit_and_push(local_repo, message="Pecha update")
