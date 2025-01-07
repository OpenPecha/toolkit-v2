from pathlib import Path
from typing import Dict, Union

from openpecha.alignment.serializers.translation import TextTranslationSerializer
from openpecha.pecha.parsers.google_doc.google_api import GoogleDocAndSheetsDownloader
from openpecha.pecha.parsers.google_doc.translation import GoogleDocTranslationParser


def parse_translation(
    docx_file: Path, metadata: Path, source_path: Union[str, None] = None
):
    """
    Parse translation from google docx and google sheet(metadata)
    There are two types
        i)  Root text
        ii) Root text's translation(need source_path arg i.e root text's layer path)
    """
    parser = GoogleDocTranslationParser(source_path)
    output_dir = Path("output")
    pecha, layer_path = parser.parse(
        input=docx_file, metadata=metadata, output_path=output_dir
    )
    return pecha, layer_path


def serialize_translation(bo_pecha_path: Path, en_pecha_path: Path):
    """
    Serialize the root opf and translation opf to JSON
    """
    serializer = TextTranslationSerializer()
    json_output_path = serializer.serialize(
        root_opf_path=bo_pecha_path,
        translation_opf_path=en_pecha_path,
        output_path=Path("json_output"),
        is_pecha_display=False,
    )
    return json_output_path


def translation_pipeline(bo_links: Dict, en_links: Dict):

    bo_docx_url, bo_sheet_url = bo_links["docx"], bo_links["sheet"]
    en_docx_url, en_sheet_url = en_links["docx"], en_links["sheet"]

    # Download
    bo_downloader = GoogleDocAndSheetsDownloader(
        google_docs_link=bo_docx_url,
        google_sheets_link=bo_sheet_url,
        credentials_path="cred.json",
        output_dir=Path("./bo"),
    )
    en_downloader = GoogleDocAndSheetsDownloader(
        google_docs_link=en_docx_url,
        google_sheets_link=en_sheet_url,
        credentials_path="cred.json",
        output_dir=Path("./en"),
    )

    # Parse
    assert bo_downloader.docx_path is not None
    assert en_downloader.docx_path is not None

    bo_pecha, bo_layer_path = parse_translation(
        bo_downloader.docx_path, bo_downloader.sheets_path
    )
    bo_pecha.publish(asset_path=Path("./bo"), asset_name="google_docx")
    en_pecha, _ = parse_translation(
        docx_file=en_downloader.docx_path,
        metadata=en_downloader.sheets_path,
        source_path=bo_layer_path.as_posix(),
    )
    en_pecha.publish(asset_path=Path("./en"), asset_name="google_docx")

    # Serialize
    json_output_path = serialize_translation(bo_pecha.pecha_path, en_pecha.pecha_path)
    return json_output_path
