import shutil
import tempfile
from pathlib import Path

from openpecha.storages import (  # Adjust import based on your script name
    update_git_folder,
)


def test_update_git_folder():
    source = tempfile.mkdtemp(prefix="source_P0001")
    dest = tempfile.mkdtemp(prefix="dest_P0001")

    source_path = Path(source)
    dest_path = Path(dest)

    try:
        # Create test files in source directory
        (source_path / "base").mkdir(parents=True, exist_ok=True)
        (source_path / "base" / "0001.txt").write_text("Updated base Content!")
        (source_path / "layers" / "0001").mkdir(parents=True, exist_ok=True)
        (source_path / "layers" / "0001" / "Meaning_Segment-8679.json").write_text(
            "{Updated Annotation file}"
        )

        # Create test files in dest directory
        (dest_path / "base").mkdir(parents=True, exist_ok=True)
        (dest_path / "base" / "0001.txt").write_text("OLd base Content!")
        (dest_path / "layers" / "0001").mkdir(parents=True, exist_ok=True)
        (dest_path / "layers" / "0001" / "Meaning_Segment-8679.json").write_text(
            "{ Old Annotation file}"
        )

        # Create .git and .github directories that should not be deleted
        (dest_path / ".git").mkdir(exist_ok=True)
        (dest_path / ".github").mkdir(exist_ok=True)

        update_git_folder(source_path, dest_path)

        # Check if destination folder is updated correctly
        assert (dest_path / "base" / "0001.txt").exists()
        assert (dest_path / "layers" / "0001" / "Meaning_Segment-8679.json").exists()
        assert (dest_path / "base" / "0001.txt").read_text() == "Updated base Content!"
        assert (
            dest_path / "layers" / "0001" / "Meaning_Segment-8679.json"
        ).read_text() == "{Updated Annotation file}"

        # Ensure .git and .github directories are still present
        assert (dest_path / ".git").exists()
        assert (dest_path / ".github").exists()

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
