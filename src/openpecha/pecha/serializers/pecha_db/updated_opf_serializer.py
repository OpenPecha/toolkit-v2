import re
import subprocess
from typing import Dict, List

from openpecha.config import get_logger
from openpecha.exceptions import GithubRepoError
from openpecha.pecha import Pecha
from openpecha.pecha.pecha_types import is_commentary_pecha, is_translation_pecha
from openpecha.utils import read_json

logger = get_logger(__name__)


class UpdateSerializeJson:
    def get_pecha_json(self, pecha: Pecha):
        pecha_id = pecha.id
        pecha_path = pecha.pecha_path.__str__()
        try:
            subprocess.run(
                "git checkout pecha_json", cwd=pecha_path, shell=True, check=True
            )
            subprocess.run(["git pull"], cwd=pecha_path, shell=True, check=True)
            json_path = f"{pecha_path}/{pecha_id}.json"
            serialized_json = read_json(json_path)
            return serialized_json
        except GithubRepoError:
            raise GithubRepoError("Error in reading json file")

    def get_pecha_segments(self, pecha: Pecha):
        base_name = list(pecha.bases.keys())[0]
        segments = []
        for _, ann_store in pecha.get_layers(base_name=base_name):
            for ann in list(ann_store):
                segment_id = str(ann.data()[0])
                segment_text = ann.text()[0]
                segments.append({"id": segment_id, "text": segment_text})
        return segments

    def insert_text_after_tag(self, old_text, new_text):
        pattern = r"(<\d+><\d+>)"  # Regular expression to match tags like <1><2>
        match = re.match(
            pattern, old_text
        )  # Search for the pattern at the start of the string
        if match is None:
            return old_text
        mapping = match.group(1) if match else ""
        if new_text == "":
            return mapping
        updated_text = mapping + new_text
        updated_text = updated_text.replace("$", "\n")
        return updated_text

    def insert_break_after_text(self, new_text):
        updated_text = new_text + "<br>"
        updated_text = updated_text.replace("$", "\n")
        return updated_text


class UpdatedCommentarySerializer(UpdateSerializeJson):
    def get_new_content(self, opf_segments, content):
        new_content = []
        for new_segment in opf_segments:
            new_text = new_segment["text"]
            segment_id = int(new_segment["id"]) - 1
            old_text = content[segment_id]
            updated_text = self.insert_text_after_tag(old_text, new_text)
            new_content.append(updated_text)
        return new_content

    def update_json(
        self,
        pecha: Pecha,
        commentary_json: Dict,
        is_translation: bool,
    ) -> Dict:
        new_content = []
        opf_segments = self.get_pecha_segments(pecha)
        if is_translation:
            content = commentary_json["source"]["books"][0]["content"][0]
            new_content = self.get_new_content(opf_segments, content)
            commentary_json["source"]["books"][0]["content"][0] = new_content
        else:
            content = commentary_json["target"]["books"][0]["content"][0]
            new_content = self.get_new_content(opf_segments, content)
            commentary_json["target"]["books"][0]["content"][0] = new_content
        return commentary_json


class UpdatedRootSerializer(UpdateSerializeJson):
    def get_new_content(self, opf_segments):
        new_content = []
        for new_segment in opf_segments:
            new_text = new_segment["text"]
            updated_text = self.insert_break_after_text(new_text)
            new_content.append(updated_text)
        return new_content

    def update_json(
        self,
        pecha: Pecha,
        root_json: Dict,
        is_translation: bool,
    ) -> Dict:
        new_content = []
        opf_segments = self.get_pecha_segments(pecha)
        if is_translation:
            new_content = self.get_new_content(opf_segments)
            root_json["source"]["books"][0]["content"][0] = new_content
        else:
            new_content = self.get_new_content(opf_segments)
            root_json["target"]["books"][0]["content"][0] = new_content
        return root_json


def update_serialize_json(pecha: Pecha, metadatas: List[Dict], json: Dict) -> Dict:
    is_commentary = is_commentary_pecha(metadatas)
    is_translation = is_translation_pecha(metadatas)
    if is_commentary:
        return UpdatedCommentarySerializer().update_json(
            pecha=pecha, commentary_json=json, is_translation=is_translation
        )
    else:
        return UpdatedRootSerializer().update_json(
            pecha=pecha, root_json=json, is_translation=is_translation
        )
