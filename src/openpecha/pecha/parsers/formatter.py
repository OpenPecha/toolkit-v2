from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional
from uuid import uuid4

from openpecha import config
from openpecha.pecha.parsers.layers import _attr_names
from openpecha.utils import read_json, write_json


class Global2LocalId:
    """Map global id of annotation in a layer to local id of a layer."""

    def __init__(self, local_id_dict: Optional[Dict[str, int]] = None):
        self.start_local_id = 200_000
        self.global2local_id: Dict[str, Any] = self._initialize(local_id_dict)
        self.local2global_id: Dict[int, str] = {
            l_id["local_id"]: g_id for g_id, l_id in self.global2local_id.items()
        }
        self.last_local_id = self.find_last()

    def _initialize(self, local_id_dict: Optional[Dict[str, int]]) -> Dict[str, Any]:
        g2lid: Dict[str, Any] = {}
        if not local_id_dict:
            return g2lid
        for global_id, local_id in local_id_dict.items():
            g2lid[global_id] = {"local_id": local_id, "is_found": False}
        return g2lid

    def find_last(self) -> int:
        """Return last local id in a layer."""
        if self.global2local_id:
            return list(self.global2local_id.values()).pop()["local_id"]
        return self.start_local_id - 1

    def add(self, global_id: str) -> None:
        """Map given `global_id` to the last local id."""
        next_local_id = self.last_local_id + 1
        self.global2local_id[global_id] = next_local_id
        self.last_local_id = next_local_id

    def get_local_id(self, global_id: str) -> Optional[Any]:
        """Return `local_id` associated to given `global_id`."""
        return self.global2local_id.get(global_id, None)

    def get_global_id(self, local_id: int) -> Optional[str]:
        """Return `global_id` associated to given `local_id`."""
        global_id = self.local2global_id.get(local_id, None)
        if not global_id:
            return None
        self.global2local_id[global_id]["is_found"] = True
        return global_id

    def serialize(self) -> Dict[str, Any]:
        """Return just the global and local id pairs."""
        result: Dict[str, Any] = {}
        for global_id, id_obj in self.global2local_id.items():
            if isinstance(id_obj, int):
                result[global_id] = id_obj
            elif id_obj["is_found"]:
                result[global_id] = id_obj["is_found"]
        return result


class LocalIdManager:
    """Maintains local_id to uuid map for echa layer."""

    def __init__(self, layers: Dict[str, Dict[str, Dict[str, Any]]]):
        self.map_name = _attr_names.LOCAL_ID
        self.maps: Dict[str, Dict[str, Global2LocalId]] = self._get_local_id_maps(
            layers
        )

    def _get_local_id_maps(
        self, layers: Dict[str, Dict[str, Dict[str, Any]]]
    ) -> Dict[str, Dict[str, Global2LocalId]]:
        maps: Dict[str, Dict[str, Global2LocalId]] = defaultdict(dict)
        for layer in layers:
            for vol in layers[layer]:
                maps[layer][vol] = Global2LocalId(
                    layers[layer][vol].get(self.map_name, {})
                )
        return maps

    def add(self, layer_name: str, vol_id: str, global_id: str) -> None:
        """Add `global_id` to layer's global2local id map."""
        if layer_name not in self.maps or vol_id not in self.maps[layer_name]:
            self.maps[layer_name][vol_id] = Global2LocalId()
        self.maps[layer_name][vol_id].add(global_id)

    def get_serialized_global2local_id(
        self, layer_name: str, vol_id: str
    ) -> Dict[str, Any]:
        """Convert map of given `layer_name` in global and local id pairs."""
        serialized_dict = self.maps[layer_name][vol_id].serialize()
        del self.maps[layer_name][vol_id]
        return serialized_dict


class BaseFormatter:
    """
    OpenPecha Base class Formatter to parse annotated text into openpecha format.
    """

    def __init__(self, output_path: str, metadata: Any):
        self.output_path = Path(output_path if output_path else config.PECHAS_PATH)
        self.metadata = metadata

    def get_unique_id(self) -> str:
        return uuid4().hex

    def _build_dirs(self, input_path: Path, id_: Optional[str] = None) -> None:
        """
        Build the necessary directories for OpenPecha format.
        """
        if id_:
            self.pecha_id = id_
        else:
            self.pecha_id = input_path.stem

        self.dirs = {
            "opf_path": self.output_path / f"{self.pecha_id}/{self.pecha_id}.opf"
        }
        self.dirs["layers_path"] = self.dirs["opf_path"] / "layers"
        self.dirs["base_path"] = self.dirs["opf_path"] / "base"

        self.dirs["layers_path"].mkdir(parents=True, exist_ok=True)
        self.dirs["base_path"].mkdir(parents=True, exist_ok=True)

    @property
    def opf_path(self) -> Path:
        return self.dirs["opf_path"]

    @property
    def pecha_path(self) -> Path:
        return self.opf_path.parent

    @property
    def meta_fn(self) -> Path:
        return self.opf_path / "meta.json"

    def normalizeUni(self, strNFC):
        strNFC = strNFC.replace("\u0F00", "\u0F68\u0F7C\u0F7E")  # ༀ
        strNFC = strNFC.replace("\u0F43", "\u0F42\u0FB7")  # གྷ
        strNFC = strNFC.replace("\u0F48", "\u0F47\u0FB7")  # ཈
        strNFC = strNFC.replace("\u0F4D", "\u0F4C\u0FB7")  # ཌྷ
        strNFC = strNFC.replace("\u0F52", "\u0F51\u0FB7")  # དྷ
        strNFC = strNFC.replace("\u0F57", "\u0F56\u0FB7")  # བྷ
        strNFC = strNFC.replace("\u0F5C", "\u0F5B\u0FB7")  # ཛྷ
        strNFC = strNFC.replace("\u0F69", "\u0F40\u0FB5")  # ཀྵ
        strNFC = strNFC.replace("\u0F73", "\u0F71\u0F72")  # ཱི
        strNFC = strNFC.replace("\u0F75", "\u0F71\u0F74")  # ཱུ
        strNFC = strNFC.replace("\u0F76", "\u0FB2\u0F80")  # ྲྀ
        strNFC = strNFC.replace("\u0F77", "\u0FB2\u0F71\u0F80")  # ཷ
        strNFC = strNFC.replace("\u0F78", "\u0FB3\u0F80")  # ླྀ
        strNFC = strNFC.replace("\u0F79", "\u0FB3\u0F71\u0F80")  # ཹ
        strNFC = strNFC.replace("\u0F81", "\u0F71\u0F80")  # ཱྀ
        strNFC = strNFC.replace("\u0F93", "\u0F92\u0FB7")  # ྒྷ
        strNFC = strNFC.replace("\u0F9D", "\u0F9C\u0FB7")  # ྜྷ
        strNFC = strNFC.replace("\u0FA2", "\u0FA1\u0FB7")  # ྡྷ
        strNFC = strNFC.replace("\u0FA7", "\u0FA6\u0FB7")  # ྦྷ
        strNFC = strNFC.replace("\u0FAC", "\u0FAB\u0FB7")  # ྫྷ
        strNFC = strNFC.replace("\u0FB9", "\u0F90\u0FB5")  # ྐྵ
        return strNFC

    def text_preprocess(self, text):
        raise NotImplementedError(
            "Text preprocessing depends on type of text format, \
                                   should be implemented in sub-class."
        )

    def get_input(self, input_path):
        """
        Return a preprocess text from given input_file path
        """
        m_text = self.text_preprocess(input_path.read_text())
        return self.normalizeUni(m_text)

    def get_old_layers(self, new_layers: List[str]) -> Dict[str, Dict[str, Any]]:
        layers: Dict[str, Dict[str, Any]] = defaultdict(dict)
        for layer in new_layers:
            for vol in self.dirs["layers_path"].iterdir():
                vol_layer_fn = vol / f"{layer}.json"
                if not vol_layer_fn.is_file():
                    continue
                layers[layer][vol.name] = read_json(vol_layer_fn)
        return layers

    def _inc_layer_revision(self, layer):
        inc_rev_int = int(layer["revision"]) + 1
        layer["revision"] = f"{inc_rev_int:05}"

    def build_layers(self, text: str) -> Any:
        """
        Parse all the layers annotation from the given text.
        """
        raise NotImplementedError(
            "Parsing annotation depends type of annotation in the text, \
                                  should be implemented in sub-class."
        )

    def get_base_text(self, m_text):
        "Returns text with all annotation removed"
        raise NotImplementedError(
            "Every type of text have different format for annotation, \
                                  should be implemented in sub-class."
        )

    def create_opf(self, input_path):
        input_path = Path(input_path)
        self._build_dirs(input_path)

        m_text = self.get_input(input_path)
        layers = self.build_layers(m_text)
        base_text = self.get_base_text(m_text)

        # save layers
        for layer, ann in layers.items():
            layer_fn = self.dirs["layers_path"] / f"{layer}.json"
            write_json(layer_fn, ann)

        # save base_text
        (self.dirs["opf_path"] / "base.txt").write_text(base_text)
