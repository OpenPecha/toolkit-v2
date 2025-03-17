import logging
import re
from pathlib import Path
from zipfile import ZipFile

from bs4 import BeautifulSoup

from openpecha.buda.api import image_group_to_folder_name
from openpecha.utils import load_json


class BDRCGBTestFileProvider:
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
        self.image_info = {}
        self.cur_zip = None
        self.cur_image_group_id = None

    def _get_image_list(self, image_group_id):
        return load_json(self.bdrc_image_list_path / str(image_group_id + ".json"))

    def get_image_list(self, image_group_id):
        self.get_images_info(image_group_id)
        buda_il = self._get_image_list(image_group_id)
        # format should be a list of image_id (/ file names)
        return map(lambda ii: ii["filename"], buda_il)

    def get_hocr_filename(self, image_id):
        for filename, img_ref in self.images_info.items():
            img_id = img_ref
            if img_id == image_id:
                return filename

    def get_images_info(self, image_group_id):
        vol_folder = image_group_to_folder_name(self.bdrc_scan_id, image_group_id)
        image_info_path = (
            Path(f"{self.ocr_disk_path}") / "info" / vol_folder / "gb-bdrc-map.json"
        )
        self.images_info = load_json(image_info_path)

    def get_source_info(self):
        image_group_ids = []
        self.source_info = self.buda_data
        curr = {}
        vol_paths = list((Path(self.ocr_disk_path) / "output").iterdir())
        for vol_path in vol_paths:
            image_group_id = re.split(r"-", vol_path.name)[1]
            image_group_ids.append(image_group_id)

        curr["image_groups"] = {
            image_group_ids[0]: self.source_info["image_groups"][image_group_ids[0]],
            image_group_ids[1]: self.source_info["image_groups"][image_group_ids[1]],
        }
        self.source_info["image_groups"] = curr["image_groups"]
        return self.source_info

    def get_image_group_data(self, image_group_id):
        if image_group_id == self.cur_image_group_id and self.cur_zip is not None:
            return self.cur_zip
        vol_folder = image_group_to_folder_name(self.bdrc_scan_id, image_group_id)
        zip_path = Path(f"{self.ocr_disk_path}") / "output" / vol_folder / "html.zip"
        self.cur_zip = ZipFile(zip_path)
        return self.cur_zip

    def get_image_data(self, image_group_id, image_filename):
        hocr_filename = self.get_hocr_filename(image_filename) + ".html"
        zf = self.get_image_group_data(image_group_id)
        try:
            for filename in zf.filelist:
                if filename.filename.split("/")[-1] == hocr_filename:
                    with zf.open(filename.filename) as hocr_file:
                        return hocr_file.read()
        except:
            return


class HOCRIATestFileProvider:
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
        self.image_hocr = {}
        self.image_info = {}

    def get_image_list(self, image_group_id):
        self.get_images_info(image_group_id)
        buda_il = self._get_image_list(image_group_id)
        # format should be a list of image_id (/ file names)
        return map(lambda ii: ii["filename"], buda_il)

    def _get_image_list(self, image_group_id):
        return load_json(self.bdrc_image_list_path / str(image_group_id + ".json"))

    def get_images_info(self, image_group_id):
        curr_image = {}
        image_list = self._get_image_list(image_group_id)
        image_group_hocr = self.get_image_group_hocr(image_group_id)
        if image_group_hocr:
            hocr_html = BeautifulSoup(image_group_hocr, "html.parser")
            pages_hocr = hocr_html.find_all("div", {"class": "ocr_page"})
            for image_number, image_filename in enumerate(image_list):
                filename = image_filename["filename"]
                for page_hocr in pages_hocr:
                    if int(page_hocr["id"][5:]) == image_number:
                        curr_image[filename] = {"page_info": page_hocr}
                        self.image_info.update(curr_image)
                        curr_image = {}

    def get_image_group_hocr(self, image_group_id):
        vol_num = self.source_info["image_groups"][image_group_id]["volume_number"]
        image_group_hocr_path = (
            Path(f"{self.ocr_disk_path}")
            / f"bdrc-{self.bdrc_scan_id}-{vol_num}_hocr.html"
        )
        try:
            hocr_html = image_group_hocr_path.read_text(encoding="utf-8")
            return hocr_html
        except:
            return

    def get_source_info(self):
        image_group_ids = []
        self.source_info = self.buda_data
        curr = {}
        vol_paths = list(Path(self.ocr_disk_path).iterdir())
        for vol_path in vol_paths:
            vol_num = re.split(r"-", vol_path.stem)[2][:-5]
            for image_group_id, info in self.source_info["image_groups"].items():
                if int(info["volume_number"]) == int(vol_num):
                    image_group_ids.append(image_group_id)

        curr["image_groups"] = {
            image_group_ids[0]: self.source_info["image_groups"][image_group_ids[0]],
            image_group_ids[1]: self.source_info["image_groups"][image_group_ids[1]],
        }
        self.source_info["image_groups"] = curr["image_groups"]
        return self.source_info

    def get_image_data(self, image_group_id, image_filename):
        try:
            page_hocr = self.image_info[image_filename]["page_info"]
            return page_hocr
        except:
            return
