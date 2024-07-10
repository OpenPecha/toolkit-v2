import os
import subprocess
from pathlib import Path
from shutil import rmtree

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


def clone_github_repo(repo_name: str, destination_folder: Path):
    repo_path = destination_folder / repo_name
    if repo_path.exists():
        rmtree(repo_path)
    else:
        try:
            repo_url = f"https://github.com/{ORG_NAME}/{repo_name}.git"
            env = {"GIT_ASKPASS": "echo", "GIT_PASSWORD": GITHUB_TOKEN}
            subprocess.run(
                ["git", "clone", repo_url, str(repo_path)],
                check=True,
                capture_output=True,
                env={k: str(v) for k, v in env.items()},
            )
            return repo_path
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {repo_name} repository: {e}")
            return None
