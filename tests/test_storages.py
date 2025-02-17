import shutil
import tempfile
from pathlib import Path

from openpecha.storages import (  # Adjust import based on your script name
    update_git_folder,
)


def test_update_git_folder():
    source = tempfile.mkdtemp(prefix="source_")
    dest = tempfile.mkdtemp(prefix="dest_")

    source_path = Path(source)
    dest_path = Path(dest)

    try:
        # Create test files in source directory
        (source_path / "source_file1.txt").write_text("Hello, World!")
        (source_path / "subdir").mkdir()
        (source_path / "subdir" / "source_file2.json").write_text("{Nested file}")

        # Create dummy files in destination directory
        (dest_path / "dest_file1.txt").write_text("To be deleted")
        (dest_path / "old_subdir").mkdir()
        (dest_path / "old_subdir" / "dest_file2.json").write_text("{To be deleted too}")

        # Create .git and .github directories that should not be deleted
        (dest_path / ".git").mkdir()
        (dest_path / ".github").mkdir()

        update_git_folder(source_path, dest_path)

        # Check if destination folder is updated correctly
        assert not (dest_path / "dest_file1.txt").exists()
        assert not (dest_path / "old_subdir").exists()
        assert (dest_path / "source_file1.txt").exists()
        assert (dest_path / "subdir" / "source_file2.json").exists()
        assert (dest_path / "source_file1.txt").read_text() == "Hello, World!"
        assert (
            dest_path / "subdir" / "source_file2.json"
        ).read_text() == "{Nested file}"

        # Ensure .git and .github directories are still present
        assert (dest_path / ".git").exists()
        assert (dest_path / ".github").exists()

    finally:
        shutil.rmtree(source)
        shutil.rmtree(dest)
