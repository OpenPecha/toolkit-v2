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
        repo_path = clone_repo("catalog", output_path)
        return repo_path

    def add_entry_to_opf_catalog(self, new_entry: List[str]) -> None:
        """
        Update a Pecha information to PechaData opf catalog
        """
        csv_path = self.repo_path / self.opf_catalog_file
        catalog_data = read_csv(csv_path)

        # Check if new entry already exists in the catalog data
        formated_new_entry = [
            str(data) if data is not None else "" for data in new_entry
        ]
        if formated_new_entry not in catalog_data:
            catalog_data.append(new_entry)
            write_csv(csv_path, catalog_data)
            commit_and_push(
                Repo(self.repo_path), message="Update catalog", branch="main"
            )
