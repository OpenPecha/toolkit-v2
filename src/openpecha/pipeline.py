import shutil
from pathlib import Path
from typing import Dict, List, Union

from openpecha.alignment.serializers.translation import TextTranslationSerializer
from openpecha.config import INPUT_DATA_PATH, PECHAS_PATH
from openpecha.ids import get_uuid
from openpecha.pecha.parsers.google_doc.google_api import GoogleDocAndSheetsDownloader
from openpecha.pecha.parsers.google_doc.translation import GoogleDocTranslationParser


def parse_root(docx_file: Path, metadata: Path, source_path: Union[str, None] = None):
    """
    Parse translation from google docx and google sheet(metadata)
    There are two types
        i)  Root text
        ii) Root text's translation(need source_path arg i.e root text's layer path)
    """
    parser = GoogleDocTranslationParser(source_path)
    pecha, layer_path = parser.parse(
        input=docx_file, metadata=metadata, output_path=PECHAS_PATH
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


def root_text_pipeline(root_links: Dict, source_path: Union[str, None] = None):
    """
    This is to download, parse and serialize the root text
    """
    root_docx_url, root_sheet_url = root_links["docx"], root_links["sheet"]

    # Download
    temp_download_path = INPUT_DATA_PATH / get_uuid()
    root_downloader = GoogleDocAndSheetsDownloader(
        google_docs_link=root_docx_url,
        google_sheets_link=root_sheet_url,
        credentials_path="cred.json",
        output_dir=Path(temp_download_path),
    )

    # Parse
    assert root_downloader.docx_path is not None

    root_pecha, root_layer_path = parse_root(
        root_downloader.docx_path, root_downloader.sheets_path, source_path
    )
    root_pecha.publish(asset_path=Path(temp_download_path), asset_name="google_docx")

    # Clean up
    shutil.rmtree(temp_download_path)

    return root_pecha, root_layer_path


def translation_pipeline(
    bo_links: Dict, translation_links: Union[List[Dict], Dict, None] = None
):
    """
    Input:
    bo_links: Contains the google docx link and google sheet link of the Tibetan root text
    translation_links: Contains the google docx link and google sheet link of the translation text
        This could be a of three types
        i) List of Dict: contains links of more than one translation text
        ii) Dict: contains links of one translation text
        iii) None: If there is no translation text
    """
    # Root text pipeline
    root_pecha, root_layer_path = root_text_pipeline(bo_links)

    # Translation text pipeline
    if isinstance(translation_links, Dict):
        translation_pecha, _ = root_text_pipeline(
            translation_links, str(root_layer_path)
        )
        serialize_translation(root_pecha.pecha_path, translation_pecha.pecha_path)
        shutil.rmtree(translation_pecha.pecha_path)

    elif isinstance(translation_links, List):
        for translation_link in translation_links:
            translation_pecha, _ = root_text_pipeline(
                translation_link, str(root_layer_path)
            )
            serialize_translation(root_pecha.pecha_path, translation_pecha.pecha_path)
            shutil.rmtree(translation_pecha.pecha_path)

    else:
        # Update serialize_translation to handle this case
        pass

    # Clean up
    shutil.rmtree(root_pecha.pecha_path)
