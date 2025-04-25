import re
from pathlib import Path

from docx2python import docx2python

from openpecha.config import get_logger
from openpecha.exceptions import EmptyFileError

logger = get_logger(__name__)


def normalize_whitespaces(text: str):
    """
    If there are spaces or tab between newlines, it will be removed.
    """
    return re.sub(r"\n[\s\t]+\n", "\n\n", text)


def normalize_newlines(text: str):
    """
    If there are more than 2 newlines continuously, it will replace it with 2 newlines.
    """
    return re.sub(r"\n{3,}", "\n\n", text)


def normalize_text(text: str):
    text = normalize_whitespaces(text)
    text = normalize_newlines(text)
    text = text.strip()
    return text


def extract_text_from_docx(docx_file: Path) -> str:
    text = docx2python(docx_file).text
    if not text:
        logger.warning(
            f"The docx file {str(docx_file)} is empty or contains only whitespace."
        )
        raise EmptyFileError(
            f"[Error] The document '{str(docx_file)}' is empty or contains only whitespace."
        )

    text = normalize_text(text)
    return text
