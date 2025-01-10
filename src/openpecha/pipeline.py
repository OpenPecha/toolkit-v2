from pathlib import Path
from typing import Dict, List, Union

from pecha_uploader.config import Destination_url
from pecha_uploader.pipeline import upload_root

from openpecha.alignment.serializers.translation import TextTranslationSerializer
from openpecha.config import JSON_OUTPUT_PATH, PECHAS_PATH
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


def serialize_translation(
    bo_pecha_path: Path, en_pecha_path: Path, json_output_path: Path
):
    """
    Serialize the root opf and translation opf to JSON
    """
    serializer = TextTranslationSerializer()
    json_output_path = serializer.serialize(
        root_opf_path=bo_pecha_path,
        translation_opf_path=en_pecha_path,
        output_path=json_output_path,
        is_pecha_display=False,
    )
    return json_output_path


def root_text_pipeline(root_links: Dict, source_path: Union[str, None] = None):
    """
    This is to parse and and publish the root text
    """
    root_docx_path, root_sheet_path = Path(root_links["docx"]), Path(
        root_links["sheet"]
    )

    root_pecha, root_layer_path = parse_root(
        root_docx_path, root_sheet_path, source_path
    )
    asset_path = root_docx_path.parent
    root_pecha.publish(asset_path=Path(asset_path), asset_name="google_docx")

    return root_pecha, root_layer_path


def translation_pipeline(
    bo_paths: Dict,
    translation_paths: Union[List[Dict], Dict, None] = None,
    output_path: Path = JSON_OUTPUT_PATH,
    destination_url: Destination_url = Destination_url.STAGING,
):
    """
    Input:
    bo_paths: Contains the google docx path and google sheet pathof the Tibetan root text
    translation_paths: Contains the google docx path and google sheet pathof the translation text
        This could be a of three types
        i) List of Dict: contains links of more than one translation text
        ii) Dict: contains links of one translation text
        iii) None: If there is no translation text
    """
    # Root text pipeline
    root_pecha, root_layer_path = root_text_pipeline(bo_paths)

    # Translation text pipeline
    if isinstance(translation_paths, Dict):
        translation_pecha, _ = root_text_pipeline(
            translation_paths, str(root_layer_path)
        )
        json_file = serialize_translation(
            root_pecha.pecha_path, translation_pecha.pecha_path, output_path
        )
        upload_root(json_file, destination_url)

    elif isinstance(translation_paths, List):
        for translation_path in translation_paths:
            translation_pecha, _ = root_text_pipeline(
                translation_path, str(root_layer_path)
            )
            json_file = serialize_translation(
                root_pecha.pecha_path, translation_pecha.pecha_path, output_path
            )
            upload_root(json_file, destination_url)

    else:
        # Update serialize_translation to handle this case
        pass
