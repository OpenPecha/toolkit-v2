# import re
# from pathlib import Path
# from typing import Any, Dict

# from openpecha.config import PECHAS_PATH
# from openpecha.pecha import Pecha
# from openpecha.pecha.layer import AnnotationType
# from openpecha.pecha.parsers import BaseParser


# class plaintextparser(BaseParser):
#     def __init__(self):
#         self.temp_state = {
#             "base_text": "",
#             "annotations": {
#                 "segments": {},
#                 "pages": {},
#             },
#             "prev_info_dict": {},
#         }

#     def extract_segment_id_and_line(self, text):
#         pattern = r"\[(\d+[ab](?:\.\d+)?)\]"
#         results = []

#         matches = list(re.finditer(pattern, text))

#         if not matches:
#             results.append({"page_number": None, "line": text.strip()})
#             return results

#         if matches[0].start() > 0:
#             pre_content = text[: matches[0].start()].strip()
#             if pre_content:
#                 results.append({"page_number": None, "line": pre_content})

#         for i, match in enumerate(matches):
#             page_number = match.group(1)
#             start = match.end()
#             end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
#             content = text[start:end].strip()

#             if not content:
#                 results.append({"page_number": page_number, "line": ""})
#                 continue

#             lines = content.splitlines()
#             for line in lines:
#                 line = line.strip()
#                 line = re.sub(r"^\{.*?\}#?", "", line)
#                 if line:
#                     results.append({"page_number": page_number, "line": line})

#         return results

#     def get_page_id(self, segment_id):
#         if "." in segment_id:
#             return segment_id.split(".")[0]
#         else:
#             return segment_id

#     def get_info_dict(self, segment_id, page_id, text):
#         text_len = len(text)
#         curr_dict: Dict[str, Any] = {"annotations": {"segments": {}, "pages": {}}}
#         if self.temp_state["prev_info_dict"]:
#             segment_start = (
#                 self.temp_state["prev_info_dict"]["segments"]["span"]["end"] + 1
#             )
#             segment_end = segment_start + text_len
#             curr_dict["annotations"]["segments"][segment_id] = {
#                 "span": {"start": segment_start, "end": segment_end}
#             }
#             if page_id == self.temp_state["prev_info_dict"]["page_id"]:
#                 page_start = self.temp_state["prev_info_dict"]["pages"]["span"]["start"]
#                 curr_dict["annotations"]["pages"][page_id] = {
#                     "span": {"start": page_start, "end": segment_end}
#                 }
#             elif page_id != self.temp_state["prev_info_dict"]["page_id"]:
#                 page_start = (
#                     self.temp_state["prev_info_dict"]["pages"]["span"]["end"] + 1
#                 )
#                 curr_dict["annotations"]["pages"][page_id] = {
#                     "span": {"start": page_start, "end": page_start + text_len}
#                 }
#         else:
#             curr_dict["annotations"]["segments"][segment_id] = {
#                 "span": {"start": 0, "end": text_len}
#             }
#             curr_dict["annotations"]["pages"][page_id] = {
#                 "span": {"start": 0, "end": text_len}
#             }
#         return curr_dict

#     def parse_bo(self, text):
#         text_list = text.split("\n")
#         for segment in text_list:
#             result = self.extract_segment_id_and_line(segment)
#             for line in result:
#                 segment_id = line["page_number"]
#                 line_text = line["line"]
#                 if not segment_id or "." not in segment_id:
#                     continue
#                 page_id = self.get_page_id(segment_id)
#                 curr_dict = self.get_info_dict(segment_id, page_id, line_text)
#                 if self.temp_state["base_text"] == "":
#                     self.temp_state["base_text"] = line_text
#                 elif (
#                     self.temp_state["base_text"] != ""
#                     and self.temp_state["prev_info_dict"]["page_id"] == page_id
#                 ):
#                     self.temp_state["base_text"] += "\n" + line_text
#                 elif self.temp_state["prev_info_dict"]["page_id"] != page_id:
#                     self.temp_state["base_text"] += "\n" + line_text
#                 self.temp_state["annotations"]["segments"][segment_id] = curr_dict[
#                     "annotations"
#                 ]["segments"][segment_id]
#                 self.temp_state["annotations"]["pages"][page_id] = curr_dict[
#                     "annotations"
#                 ]["pages"][page_id]
#                 self.temp_state["prev_info_dict"] = {
#                     "segment_id": segment_id,
#                     "page_id": page_id,
#                     "segments": curr_dict["annotations"]["segments"][segment_id],
#                     "pages": curr_dict["annotations"]["pages"][page_id],
#                 }

#     def get_info_dict_for_zh(self, segment_id, segment):
#         text_len = len(segment)
#         if text_len == 0:
#             segment = "\n"
#             text_len = 1
#         curr_dict = {"annotations": {"segments": {}, "pages": {}}}
#         if self.temp_state["base_text"] == "":
#             segment_start = 0
#             segment_end = text_len
#             self.temp_state["base_text"] = segment + "\n"
#             self.temp_state["annotations"]["segments"][segment_id] = {
#                 "span": {"start": segment_start, "end": segment_end}
#             }
#         else:
#             segment_start = len(self.temp_state["base_text"])
#             segment_end = segment_start + text_len
#             if segment == "\n":
#                 self.temp_state["base_text"] += segment
#             else:
#                 self.temp_state["base_text"] += segment + "\n"
#             self.temp_state["annotations"]["segments"][segment_id] = {
#                 "span": {"start": segment_start, "end": segment_end}
#             }
#         curr_dict["annotations"]["segments"][segment_id] = {
#             "span": {"start": segment_start, "end": segment_end}
#         }
#         return curr_dict

#     def parse_zh(self, text):
#         text_list = text.split("\n")
#         for segment_id, segment in enumerate(text_list, 1):
#             curr_dict = self.get_info_dict_for_zh(segment_id, segment)
#             self.temp_state["prev_info_dict"] = {
#                 "segment_id": segment_id,
#                 "segments": curr_dict["annotations"]["segments"][segment_id],
#             }

#     def write_to_pecha(self, pecha, metadata):
#         curr_bases = {}
#         bases = []
#         order = 1
#         base_name = pecha.set_base(content=self.temp_state["base_text"])

#         total_segments = 0
#         total_pages = 0

#         if "segments" in self.temp_state["annotations"]:
#             segment, _ = pecha.add_layer(base_name, AnnotationType.segmentation)
#             for segment_id, segment_span in self.temp_state["annotations"][
#                 "segments"
#             ].items():
#                 segment_ann = {
#                     AnnotationType.segmentation.value: segment_span["span"],
#                     "segment_id": segment_id,
#                 }
#                 pecha.add_annotation(segment, segment_ann, AnnotationType.segmentation)
#             segment.save()
#             total_segments = len(self.temp_state["annotations"]["segments"])

#         if "pages" in self.temp_state["annotations"]:
#             pagination, _ = pecha.add_layer(base_name, AnnotationType.pagination)
#             for page_id, page_ann in self.temp_state["annotations"]["pages"].items():
#                 page_ann = {
#                     AnnotationType.pagination.value: page_ann["span"],
#                     "folio": page_id,
#                 }
#                 pecha.add_annotation(pagination, page_ann, AnnotationType.pagination)
#             pagination.save()
#             total_pages = len(self.temp_state["annotations"]["pages"])

#         curr_bases = {
#             base_name: {
#                 "source_metadata": {
#                     "source_id": "001",
#                     "total_segments": total_segments,
#                     "total_pages": total_pages,
#                 },
#                 "base_file": base_name,
#                 "order": order,
#             }
#         }
#         bases.append(curr_bases)

#         pecha.set_metadata(
#             {"id": pecha.id, "parser": self.name, "bases": bases, **metadata}
#         )

#     def parse(
#         self,
#         input: Any,
#         metadata: Dict|Path,
#         output_path: Path = PECHAS_PATH,
#     ):
#         text = input.read_text(encoding="utf-8")
#         if metadata["language"] == "bo":
#             self.parse_bo(text)
#         elif metadata["language"] == "zh":
#             self.parse_zh(text)
#         pecha = Pecha.create(output_path)
#         self.write_to_pecha(pecha, metadata)
#         return pecha
