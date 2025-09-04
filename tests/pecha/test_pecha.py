import pytest
from pathlib import Path
from openpecha.pecha import Pecha
from openpecha.exceptions import FileNotFoundError

def test_pecha_from_path_with_file_raises_error():
    """Test that passing a file instead of directory raises ValueError"""
    with pytest.raises(ValueError, match="Pecha path must be a directory, not a file"):
        Pecha.from_path(Path("tests/pecha/data/test_opf.zip"))

def test_pecha_from_path_with_nonexistent_path():
    """Test that passing a non-existent path raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError, match="Pecha path does not exist"):
        Pecha.from_path(Path("tests/pecha/data/nonexistent_path"))