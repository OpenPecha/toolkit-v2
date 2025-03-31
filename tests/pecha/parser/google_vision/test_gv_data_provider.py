import gzip
import json

from openpecha.buda.api import image_group_to_folder_name
from openpecha.config import get_logger
from openpecha.utils import read_json

# Initialize the logger
logger = get_logger(__name__)


class GoogleVisionTestFileProvider:
    def __init__(
        self,
        bdrc_scan_id,
        bdrc_image_list_path,
        buda_data,
        ocr_import_info,
        ocr_disk_path,
    ):
        self.ocr_import_info = ocr_import_info
        self.ocr_disk_path = ocr_disk_path
        self.bdrc_scan_id = bdrc_scan_id
        self.buda_data = buda_data
        self.bdrc_image_list_path = bdrc_image_list_path

    def get_image_list(self, image_group_id):
        bdrc_image_list = read_json(
            self.bdrc_image_list_path / str(image_group_id + ".json")
        )
        if not bdrc_image_list:
            return []
        return map(lambda ii: ii["filename"], bdrc_image_list)

    def get_source_info(self):
        return self.buda_data

    def get_image_data(self, image_group_id, image_id):
        vol_folder = image_group_to_folder_name(self.bdrc_scan_id, image_group_id)
        expected_ocr_filename = image_id[: image_id.rfind(".")] + ".json.gz"
        image_ocr_path = self.ocr_disk_path / vol_folder / expected_ocr_filename
        ocr_object = None
        try:
            ocr_object = json.load(gzip.open(str(image_ocr_path), "rb"))
        except Exception as e:
            logger.exception(f"could not read {image_ocr_path}: {e}")
        return ocr_object
