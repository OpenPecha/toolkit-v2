import os
import re
import json
import pyewts
from pathlib import Path
from typing import Callable, Dict, List, Union
from stam import AnnotationStore, Offset, Selector
from openpecha.config import _mkdir
from openpecha.ids import get_initial_pecha_id, get_uuid
from openpecha.pecha import Pecha
from openpecha.pecha.layer import LayerEnum, get_layer_group

ewts = pyewts.pyewts()


class DharamanexusParser():
    def __init__(self, regex_pattern):
        self.regex_pattern = regex_pattern
        self.state = {}
        self.temp_state = {
            'base_text': "",
            'annotations': {
                'segments': {},
                'pages': {}
            },
            'prev_info_dict': {}
        }


    def get_category_wise_files(self, files_json_path):
        with open(files_json_path, 'r') as f:
            files = json.load(f)
        category_file_paths = {}
        for file in files:
            category = file["category"]
            text_name = file["textname"]
            if category not in category_file_paths.keys():
                category_file_paths[category] = {
                    text_name: [file["filename"]]
                }
            else:
                if text_name not in category_file_paths[category].keys():
                    category_file_paths[category][text_name] = [file["filename"]]
                else:
                    category_file_paths[category][text_name].append(file["filename"])
        return category_file_paths


    def read_json(self, file_path):
        with open(file_path, 'r') as f:
            return json.load(f)


    def sort_file_names(self, files):
        parts = re.findall(self.regex_pattern, files)
        key = []
        for part in parts:
            if part.isdigit():
                key.append(int(part))
            elif re.match(r'\d+\.\d+', part):
                key.append(float(part))
            else:
                key.append(part.strip())
        return key


    def get_info_dict(self, segment_id, page_id, text):
        text_len = len(text)
        curr_dict = {'annotations': {'segments': {}, 'pages': {}}}
        if self.temp_state['prev_info_dict']:
            segment_start = self.temp_state['prev_info_dict']['segments']['span']['end'] + 1
            segment_end = segment_start + text_len
            curr_dict['annotations']['segments'][segment_id] = {
                "span": {
                    "start": segment_start,
                    "end": segment_end
                }
            }
            if page_id == self.temp_state['prev_info_dict']['page_id']:
                page_start = self.temp_state['prev_info_dict']['pages']['span']['start']
                curr_dict['annotations']['pages'][page_id]={
                    'span': {
                        'start': page_start,
                        'end': segment_end
                    }
                }
            elif page_id != self.temp_state['prev_info_dict']['page_id']:
                page_start = self.temp_state['prev_info_dict']['pages']['span']['end'] + 1
                curr_dict['annotations']['pages'][page_id] = {
                    "span": {
                        "start": page_start,
                        "end": page_start + text_len
                    }
                }
        else:
            curr_dict['annotations']['segments'][segment_id] = {
                "span": {
                    "start": 0,
                    "end": text_len
                }
            }
            curr_dict['annotations']['pages'][page_id] = {
                "span": {
                    "start": 0,
                    "end": text_len
                }
            }
        return curr_dict


    def parse(self, file_dict):
        for vol, file_paths in file_dict.items():
            for file_path in file_paths:
                json_file = self.read_json(file_path)
                for info in json_file:
                    text = ewts.toUnicode(info["original"])
                    segment_id = info["segmentnr"]
                    page_id = info["folio"]
                    curr_dict = self.get_info_dict(segment_id, page_id, text)
                    if self.temp_state['base_text'] == "":
                        self.temp_state['base_text'] = text
                    elif self.temp_state['base_text'] != "" and self.temp_state['prev_info_dict']['page_id'] == page_id:
                        self.temp_state['base_text'] += " " + text
                    elif self.temp_state['prev_info_dict']['page_id'] != page_id:
                        self.temp_state['base_text'] += "\n" + text
                    self.temp_state['annotations']['segments'][segment_id] = curr_dict['annotations']['segments'][segment_id]
                    self.temp_state['annotations']['pages'][page_id] = curr_dict['annotations']['pages'][page_id]
                    self.temp_state['prev_info_dict'] = {
                            'segment_id' : segment_id,
                            'page_id': page_id,
                            'segments': curr_dict['annotations']['segments'][segment_id],
                            'pages': curr_dict['annotations']['pages'][page_id]
                        }
            self.state[vol]={
                'base_text': self.temp_state['base_text'],
                'annotations': self.temp_state['annotations']
                }
            self.temp_state = { 'base_text': "", 'annotations': { 'segments': {}, 'pages': {}},'prev_info_dict': {}}


    def get_sorted_file_paths(self, file_paths):
        self.pecha = Pecha()
        for _, texts in file_paths.items():
            sorted_texts = sorted(texts.keys(), key=self.sort_file_names)
            for text_name in sorted_texts:
                files = texts[text_name]
                sorted_files = sorted(files, key=self.sort_file_names)
        return sorted_files
