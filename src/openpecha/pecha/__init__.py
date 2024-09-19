import json
from collections import defaultdict
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Union

import stam
from stam import Annotation, AnnotationStore, Selector

from openpecha import utils
from openpecha.config import PECHAS_PATH
from openpecha.github_utils import clone_repo
from openpecha.ids import get_uuid
from openpecha.pecha.blupdate import update_layer
from openpecha.pecha.layer import LayerEnum, get_layer_collection, get_layer_group

BASE_NAME = str
LAYER_NAME = str


class StamPecha:
    def __init__(self, path: Union[Path, str]):
        path = Path(path)
        self.run_checks(path)
        self.path: Path = path.resolve()
        self.parent: Path = self.path.parent
        self.pecha_id: str = self.path.name
        self.layers: Dict[BASE_NAME, Dict[LAYER_NAME, AnnotationStore]] = defaultdict(
            dict
        )

    @staticmethod
    def run_checks(path: Path):
        """
        This function checks if the pecha path is valid or not.
        """
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")
        if not path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")

        if not (path / "base").exists():
            raise FileNotFoundError(f"{path} does not have a base layer.")

        if not (path / "layers").exists():
            raise FileNotFoundError(f"{path} does not have any layers.")

    @property
    def base_path(self) -> Path:
        return self.path / "base"

    @property
    def layers_path(self) -> Path:
        return self.path / "layers"

    def get_base(self, base_name) -> str:
        """
        This function returns the base layer of the pecha.
        """
        return (self.base_path / f"{base_name}.txt").read_text()

    def set_base(self, base_name, content) -> None:
        """
        This function sets the base layer of the pecha to a new text.
        """
        (self.base_path / f"{base_name}.txt").write_text(content)

    def get_layers(
        self, base_name, from_cache=False
    ) -> Generator[Tuple[str, AnnotationStore], None, None]:
        """
        This function returns the layers of the pecha.

        Args:
            base_name (str): The base name to identify specific layers.

        Returns:
            Generator[AnnotationStore, None, None]: Yields instances of `AnnotationStore` as they are read from directory files.
        """

        for layer_fn in (self.layers_path / base_name).iterdir():
            rel_layer_fn = layer_fn.relative_to(self.parent)
            if from_cache:
                store = self.layers[base_name].get(rel_layer_fn.name)
            else:
                store = None

            if store:
                yield layer_fn.name, store
            else:
                with utils.cwd(self.parent):
                    store = AnnotationStore(file=str(rel_layer_fn))
                self.layers[base_name][rel_layer_fn.name] = store
                yield layer_fn.name, store

    def get_layer(self, base_name, layer_name):
        """
        This function returns a specific layer of the pecha.
        """
        if not self.layers[base_name]:
            self.get_layers(base_name)
        return self.layers[base_name][layer_name]

    def update_base(self, base_name, new_base, save=True):
        """
        This function updates the base layer of the pecha to a new text. It will recompute the existing layers into the new base layer.
        """
        for _, layer in self.get_layers(base_name):
            old_base = layer.resource(base_name).text()
            update_layer(base_name, old_base, new_base, layer)
            if save:
                with utils.cwd(self.parent):
                    layer.save()
        if save:
            self.set_base(base_name, new_base)

    @staticmethod
    def change_resource(
        source_resource: stam.TextResource,
        target_resource: stam.TextResource,
        layer: stam.AnnotationStore,
    ) -> stam.AnnotationStore:
        """
        Update all annotations referencing to `source` to `target` resource.

        Args:
            source_resource(stam.Resource): source resource
            target_resource(stam.Resource): target resource
            layer(stam.AnnotationStore): layer to be edited

        Retuns:
            layer(stam.AnnotationStore): edited layer
        """
        for ann in layer.annotations():
            ann_id = ann.id()
            offset = ann.offset()
            data = list(ann.data())

            layer.remove(ann, strict=True)

            layer.annotate(
                id=ann_id,
                target=Selector.textselector(target_resource, offset),
                data=data,
            )

        layer.remove(source_resource, strict=True)

        return layer

    def merge_pecha(
        self,
        source_pecha: "StamPecha",
        source_base_name: str,
        target_base_name: str,
    ):
        """
        This function merges the layers of the source pecha into the current pecha.

        Args:
            source_pecha_path (Union[Path, str]): The path of the source pecha.
            source_base_name (str): The base name of the source pecha.
            target_base_name (str): The base name of the target (current) pecha.
        """

        target_base = self.get_base(target_base_name)

        source_pecha.update_base(source_base_name, target_base, save=False)

        for layer_fn, layer in source_pecha.get_layers(
            source_base_name, from_cache=True
        ):

            with utils.cwd(self.parent):
                target_base_fn = (
                    self.base_path.relative_to(self.parent) / f"{target_base_name}.txt"
                )
                target_layer_fn = self.layers_path / target_base_name / layer_fn
                layer.add_resource(id=target_base_name, filename=str(target_base_fn))
                source_resouce = layer.resource(source_base_name)
                target_resource = layer.resource(target_base_name)
                layer = self.change_resource(source_resouce, target_resource, layer)
                layer_json_string = layer.to_json_string()
                layer_json_string = layer_json_string.replace("null,", "")
                target_layer_fn.write_text(layer_json_string)


class Pecha:
    def __init__(self, pecha_id: str, pecha_path: Path) -> None:
        self.id_ = pecha_id
        self.pecha_path = pecha_path

    @classmethod
    def from_id(cls, pecha_id: str):
        pecha_path = clone_repo(pecha_id, PECHAS_PATH)
        return Pecha.from_path(pecha_path)

    @classmethod
    def from_path(cls, pecha_path: Path) -> "Pecha":
        pecha_id = pecha_path.stem
        return cls(pecha_id, pecha_path)

    @property
    def base_path(self) -> Path:
        base_path = self.pecha_path / "base"
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)
        return base_path

    @property
    def ann_path(self):
        ann_path = self.pecha_path / "layers"
        if not ann_path.exists():
            ann_path.mkdir(parents=True, exist_ok=True)
        return ann_path

    @property
    def metadata(self):
        return AnnotationStore(file=str(self.pecha_path / "metadata.json"))

    def set_base(self, base_name, content) -> None:
        """
        This function sets the base layer of the pecha to a new text.
        """
        (self.base_path / f"{base_name}.txt").write_text(content)

    def create_ann_store(self, basefile_name: str, annotation_type: LayerEnum):
        ann_store = AnnotationStore(id=self.id_)
        ann_store.add_resource(
            id=basefile_name,
            filename=(self.base_path / f"{basefile_name}.txt").as_posix(),
        )

        dataset_id = get_layer_collection(annotation_type).value
        ann_store.add_dataset(id=dataset_id)

        return ann_store

    def annotate_metadata(self, ann_store: AnnotationStore, metadata: dict):
        ann_resource = next(ann_store.resources())
        ann_dataset = next(ann_store.datasets())

        ann_data = []
        for k, v in metadata.items():
            if v:
                v = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
                ann_data.append(
                    {"id": get_uuid(), "set": ann_dataset.id(), "key": k, "value": v}
                )

        ann_store.annotate(
            id=get_uuid(), target=Selector.resourceselector(ann_resource), data=ann_data
        )
        return ann_store

    def annotate(
        self,
        ann_store: AnnotationStore,
        selector: Selector,
        ann_type: LayerEnum,
        ann_data_id: str,
        data: Optional[List] = None,
    ):
        ann_id = get_uuid()
        ann_dataset = next(ann_store.datasets())
        ann_group = get_layer_group(ann_type)

        if not ann_data_id:
            ann_data_id = get_uuid()

        ann_type_data = [
            {
                "id": ann_data_id,
                "set": ann_dataset.id(),
                "key": ann_group.value,
                "value": ann_type.value,
            }
        ]
        if not data:
            data = ann_type_data
        else:
            data.extend(ann_type_data)

        ann = ann_store.annotate(id=ann_id, target=selector, data=data)
        return ann

    def get_annotation_store(self, basefile_name: str, annotation_type: LayerEnum):
        ann_store_file_paths = list(
            Path(self.ann_path / basefile_name).glob(f"{annotation_type.value}*.json")
        )
        annotation_stores = [
            AnnotationStore(file=str(annotation_file))
            for annotation_file in ann_store_file_paths
        ]

        if len(annotation_stores) == 1:
            return annotation_stores[0], ann_store_file_paths[0]

        return annotation_stores, ann_store_file_paths

    def save_ann_store(
        self, ann_store: AnnotationStore, ann_type: LayerEnum, basefile_name: str
    ):
        if ann_type == LayerEnum.metadata:
            file_name = "metadata.json"
            ann_store_path = self.pecha_path
        else:
            file_name = f"{ann_type.value}-{get_uuid()[:3]}.json"
            ann_store_path = self.ann_path / basefile_name
        ann_store_path.mkdir(parents=True, exist_ok=True)
        ann_store_json_dict = self.convert_absolute_to_relative_path(
            ann_store, ann_store_path
        )

        with open(ann_store_path / file_name, "w", encoding="utf-8") as f:
            f.write(json.dumps(ann_store_json_dict, indent=2, ensure_ascii=False))

        return ann_store_path / file_name

    @staticmethod
    def convert_absolute_to_relative_path(
        ann_store: AnnotationStore, ann_store_path: Path
    ):
        """
        convert the absolute to relative path for base file in json string of annotation store
        """
        ann_store_json_string = ann_store.to_json_string()
        json_object = json.loads(ann_store_json_string)
        for resource in json_object["resources"]:
            original_path = Path(resource["@include"])
            if ann_store_path.name == "metadata.json":
                resource["@include"] = f"base/{original_path.name}"
            else:
                resource["@include"] = f"../../base/{original_path.name}"
        return json_object


def save_stam(ann_store: AnnotationStore, ann_store_path: Path) -> Path:
    """
    Save the annotation store to a file.
    """
    ann_store_path.parent.mkdir(parents=True, exist_ok=True)

    ann_json_str = ann_store.to_json_string()
    ann_json_dict = convert_absolute_to_relative_path(ann_json_str, ann_store_path)
    with open(ann_store_path, "w", encoding="utf-8") as f:
        f.write(json.dumps(ann_json_dict, indent=2, ensure_ascii=False))

    return ann_store_path


def convert_absolute_to_relative_path(json_string: str, ann_store_path: Path):
    """
    convert the absolute to relative path for base file in json string of annotation store
    """
    json_object = json.loads(json_string)
    for resource in json_object["resources"]:
        original_path = Path(resource["@include"])
        if ann_store_path.name == "metadata.json":
            resource["@include"] = f"base/{original_path.name}"
        else:
            resource["@include"] = f"../../base/{original_path.name}"
    return json_object
