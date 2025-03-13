import csv
import json
import os
from contextlib import contextmanager
from typing import List


@contextmanager
def cwd(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def read_json(file_path):
    with open(file_path) as f:
        data = json.load(f)
    return data


def write_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_text_direction_with_lang(lang):
    # Left-to-Right (LTR) languages
    ltr_languages = [
        "bo",  # Tibetan
        "dz",  # Dzongkha
        "en",  # English
        "es",  # Spanish
        "fr",  # French
        "hi",  # Hindi
        "ja",  # Japanese
        "ko",  # Korean
        "mn",  # Mongolian
        "mr",  # Marathi
        "ms",  # Malay
        "ne",  # Nepali
        "pt",  # Portuguese
        "ru",  # Russian
        "sw",  # Swahili
        "th",  # Thai
        "vi",  # Vietnamese
        "zh",  # Chinese (both Simplified and Traditional)
    ]

    # Right-to-Left (RTL) languages
    rtl_languages = ["ar", "he"]  # Arabic  # Hebrew

    if lang in ltr_languages:
        return "ltr"
    elif lang in rtl_languages:
        return "rtl"
    else:
        # Default to LTR if language is unknown
        return "ltr"


def parse_root_mapping(root_mapping) -> List[int]:
    """
    Parse the root_mapping into List of Integers.
    Examples:>
    Input: 1  Output: [1]
    Input: 1,2,3,4,5 Output: [1,2,3,4,5]
    Input: 1-3  Output: [1,2,3]
    Input: 1-3,5-7 Output: [1,2,3,5,6,7]
    """
    root_mapping = root_mapping.replace(" ", "").strip()
    root_mapping_list = []
    for mapping in root_mapping.split(","):
        if "-" in mapping:
            start, end = mapping.split("-")
            root_mapping_list.extend(list(range(int(start), int(end) + 1)))
        else:
            root_mapping_list.append(int(mapping))
    return root_mapping_list


def chunk_strings(strings, chunk_size=100):
    """
    Splits a list of strings into smaller lists of at most chunk_size elements each.

    Args:
    strings (list of str): The list of strings to be chunked.
    chunk_size (int): The maximum size of each chunk.

    Returns:
    list of list of str: A list of lists, where each inner list contains up to chunk_size elements.
    """
    return [strings[i : i + chunk_size] for i in range(0, len(strings), chunk_size)]


def read_csv(file_path) -> List[List[str]]:
    with open(file_path, newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        rows = list(reader)
    return rows


def write_csv(file_path, data) -> None:
    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerows(data)


"""Utilities functions from toolkit v1
"""
import gzip
import io
import shutil
import urllib
from collections import defaultdict
from pathlib import Path
from typing import Dict

import requests
import yaml
from git import Repo
from git.cmd import GitCommandError

from openpecha import config
from openpecha.core import metadata
from openpecha.core.layer import LayerEnum
from openpecha.exceptions import PechaNotFound
from openpecha.github_utils import create_release
from openpecha.storages import GithubStorage, setup_auth_for_old_repo

INFO = "[INFO] {}"

# use yaml.CSafeLoader / if available but don't crash if it isn't
try:
    yaml_loader = yaml.CSafeLoader
except (ImportError, AttributeError):
    yaml_loader = yaml.SafeLoader

try:
    yaml_dumper = yaml.CSafeDumper
except (ImportError, AttributeError):
    yaml_dumper = yaml.SafeDumper


def simple_enum_to_yaml(representer, node):
    return representer.represent_data(node.value)


yaml_dumper.add_multi_representer(LayerEnum, simple_enum_to_yaml)
yaml_dumper.add_multi_representer(metadata.InitialCreationType, simple_enum_to_yaml)
yaml_dumper.add_multi_representer(metadata.CopyrightStatus, simple_enum_to_yaml)
yaml_dumper.add_multi_representer(metadata.LicenseType, simple_enum_to_yaml)


def gzip_str(string_):
    # taken from https://gist.github.com/Garrett-R/dc6f08fc1eab63f94d2cbb89cb61c33d
    out = io.BytesIO()

    with gzip.GzipFile(fileobj=out, mode="w") as fo:
        fo.write(string_.encode())

    bytes_obj = out.getvalue()
    return bytes_obj


def _mkdir(path):
    if path.is_dir():
        return path
    path.mkdir(exist_ok=True, parents=True)
    return path


def ocr_result_input(path):
    return path


def create_release_with_assets(path):
    asset_paths = []
    for asset_path in (path / "releases").iterdir():
        shutil.make_archive(asset_path, "zip", asset_path)
        asset_paths.append(f"{str(asset_path)}.zip")

    create_release(path.name, asset_paths=asset_paths)


class Vol2FnManager:
    def __init__(self, metadata):
        self.name = "vol2fn"
        self.vol_num = 0
        self.vol2fn = self._get_vol2fn(metadata)
        self.fn2vol = {fn: vol for vol, fn in self.vol2fn.items()}

    def _get_vol2fn(self, metadata):
        if self.name in metadata:
            return metadata[self.name]
        else:
            return defaultdict(dict)

    def get_fn(self, vol):
        return self.vol2fn.get(vol)

    def get_vol_id(self, fn):
        vol_id = self.fn2vol.get(fn)
        if vol_id:
            return vol_id
        else:
            self.vol_num += 1
            vol_id = f"v{self.vol_num:03}"
            self.vol2fn[vol_id] = fn
            return vol_id


def dump_yaml(data: Dict, output_fn: Path) -> Path:
    with output_fn.open("w", encoding="utf-8") as fn:
        yaml.dump(
            data,
            fn,
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
            Dumper=yaml_dumper,
        )
    return output_fn


def load_json(file_path: str):
    """Loads a JSON file and returns its content as a dictionary."""
    file_path = Path(file_path)  # Ensure it's a Path object
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with file_path.open(encoding="utf-8") as f:
        return json.load(f)  # Parses JSON file content and returns as a dictionary

def load_yaml(fn: Path) -> None:
    return yaml.load(fn.open(encoding="utf-8"), Loader=yaml_loader)


def load_yaml_str(s: str) -> None:
    return yaml.load(s, Loader=yaml_loader)


def _eval_branch(repo, branch):
    """return default branch as fallback branch."""
    if branch in repo.refs or f"origin/{branch}" in repo.refs:
        return branch
    elif "main" in repo.refs:
        return "main"
    else:
        return "master"


def download_pecha(pecha_id, out_path=None, needs_update=True, branch="main") -> Path:
    """Download pecha from github

    Note: If pecha is already downloaded before and needs_update,
          it will update the pecha by pulling the remote `branch`.

    Args:
        pecha_id (str): pecha id
        out_path (str, optional): path to download pecha. Defaults to None.
        needs_update (bool, optional): if True, update pecha. Defaults to True.
        branch (str, optional): branch name. Defaults to "main".

    Returns:
        Path: pecha path
    """
    # resolve defaults kwargs
    needs_update = needs_update if needs_update is not None else True
    branch = branch if branch is not None else "main"
    storage = GithubStorage()

    # create pecha path
    if out_path:
        out_path = Path(out_path)
        out_path.mkdir(exist_ok=True, parents=True)
        pecha_path = out_path / pecha_id
    else:
        pecha_path = config.PECHAS_PATH / pecha_id

    if pecha_path.is_dir():
        repo = Repo(str(pecha_path))
        branch = _eval_branch(repo, branch)
        repo.git.checkout(branch)
        if needs_update:
            repo.git.config("pull.rebase", "false")
            repo.git.pull("origin", branch)
    else:
        pecha_url = storage.get_authenticated_repo_remote_url(pecha_id)
        try:
            Repo.clone_from(pecha_url, str(pecha_path))
        except GitCommandError:
            raise PechaNotFound(f"Pecha with id {pecha_id} doesn't exist")
        repo = Repo(str(pecha_path))
        branch = _eval_branch(repo, branch)
        repo.git.checkout(branch)

    # setup auth
    setup_auth_for_old_repo(repo, org=storage.org_name, token=storage.token)

    return pecha_path


def download_pecha_assets(pecha_id: str, asset_type: str, download_dir: Path):
    """Download pecha assets from latest release

    Args:
        pecha_id (str): pecha id
        asset_type (str): asset type can be src web page or ocr output
        download_dir (Path): directory where you want to download the assets

    Returns:
        Path: zip file path of downloaded asset
    """

    response = requests.get(
        f"https://api.github.com/repos/OpenPecha-data/{pecha_id}/releases/latest"
    )
    res = response.json()
    for asset in res["assets"]:
        if asset["name"] == f"{asset_type}.zip":
            asset_download_url = asset["browser_download_url"]
            break
    f = urllib.request.urlopen(asset_download_url)
    assets = f.read()
    zip_asset_file_path = download_dir / f"{pecha_id}_{asset_type}.zip"

    zip_asset_file_path.write_bytes(assets)

    return zip_asset_file_path
