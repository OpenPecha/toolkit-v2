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
        self.repo_path = self.clone_catalog(output_path)
        self.pecha_catalog_file = self.repo_path / "opf_catalog.csv"
        self.catalog_data = read_csv(self.pecha_catalog_file)

    def clone_catalog(self, output_path: Path):
        repo_path = clone_repo("catalog", output_path)
        return repo_path

    def add_entry_to_pecha_catalog(self, new_entry: List[str]) -> None:
        """
        Update a Pecha information to PechaData pecha catalog
        """
        # Check if new entry already exists in the catalog data
        formated_new_entry = [
            str(data) if data is not None else "" for data in new_entry
        ]
        if formated_new_entry not in self.catalog_data:
            self.catalog_data.append(new_entry)
            write_csv(self.pecha_catalog_file, self.catalog_data)
            commit_and_push(
                Repo(self.repo_path), message="Update catalog", branch="main"
            )
