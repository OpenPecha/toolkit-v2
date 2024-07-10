import os
from pathlib import Path

from github import Github, GithubException

from openpecha.config import ORG_NAME

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise Exception("GITHUB_TOKEN is not set in the environment.")


def create_github_repo(repo_name: str):
    try:
        g = Github(GITHUB_TOKEN)
        org = g.get_organization(ORG_NAME)
        org.create_repo(repo_name)

    except GithubException as e:
        raise GithubException(f"Error creating repo: {e}")


def upload_files_to_github_repo(repo_name: str, folder_path: Path):
    try:
        g = Github(GITHUB_TOKEN)
        org = g.get_organization(ORG_NAME)
        repo = org.get_repo(repo_name)

        for file in folder_path.rglob("*"):
            if file.is_dir():
                continue
            file_path = file.relative_to(folder_path)
            with open(file) as f:
                content = f.read()
                repo.create_file(str(file_path), f"committing {file.name}", content)
    except GithubException as e:
        raise GithubException(f"Error uploading files to github: {e}")
