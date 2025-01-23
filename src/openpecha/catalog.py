from pathlib import Path
from typing import List

from git import Repo

from openpecha.config import PECHA_DATA_ORG, PECHAS_PATH
from openpecha.github_utils import clone_repo
from openpecha.storages import commit_and_push
from openpecha.utils import read_csv, write_csv


class PechaDataCatalog:
    def __init__(self, output_path: Path = PECHAS_PATH):
        self.org_name = PECHA_DATA_ORG
        self.repo_name = "catalog"
        self.opf_catalog_file = "opf_catalog.csv"
        self.repo_path = self.clone_catalog(output_path)

    def clone_catalog(self, output_path: Path):
        repo_path = clone_repo("catalog", PECHAS_PATH)
        return repo_path

    def update_opf_catalog(self, row: List[str]) -> None:
        """
        Update a Pecha information to PechaData opf catalog
        """

        csv_path = self.repo_path / self.opf_catalog_file
        catalog_csv = read_csv(csv_path)
        catalog_csv.append(row)
        write_csv(csv_path, catalog_csv)
        commit_and_push(Repo(self.repo_path), message="Update catalog", branch="main")
