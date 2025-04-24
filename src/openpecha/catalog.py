import ast
from pathlib import Path
from typing import List

from git import Repo

from openpecha.config import GITHUB_ORG_NAME, PECHAS_PATH
from openpecha.github_utils import clone_repo
from openpecha.storages import commit_and_push
from openpecha.utils import read_csv, write_csv


class PechaDataCatalog:
    def __init__(self, output_path: Path = PECHAS_PATH):
        self.org_name = GITHUB_ORG_NAME
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

    def get_pecha_id_with_title(self, title: str) -> str | None:
        """
        1.Get pecha/opf catalog data
        2.Compare title with each entry
        3.When matched, return the pecha id
        """
        for cat_data in self.catalog_data[1:]:
            pecha_id = cat_data[0]
            entry_title_str = cat_data[1]

            try:
                entry_title = ast.literal_eval(entry_title_str)
            except (ValueError, SyntaxError):
                entry_title = entry_title_str

            if isinstance(entry_title, dict):
                if title in entry_title.values():
                    return pecha_id

            elif isinstance(entry_title, str):
                if title == entry_title:
                    return pecha_id
        return None
