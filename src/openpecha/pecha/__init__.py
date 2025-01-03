import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, Generator, List, Optional, Tuple, Union

import stam
from git import Repo
from stam import Annotation, AnnotationStore, Offset, Selector

from openpecha import utils
from openpecha.config import PECHAS_PATH
from openpecha.github_utils import clone_repo, create_release
from openpecha.ids import get_annotation_id, get_base_id, get_initial_pecha_id, get_uuid
from openpecha.pecha.blupdate import update_layer
from openpecha.pecha.layer import LayerEnum, get_layer_collection, get_layer_group
from openpecha.pecha.metadata import PechaMetaData
from openpecha.storages import GithubStorage, Storage, commit_and_push

BASE_NAME = str
layer_type = str


class StamPecha:
    def __init__(self, path: Union[Path, str]):
        path = Path(path)
        self.run_checks(path)
        self.path: Path = path.resolve()
        self.parent: Path = self.path.parent
        self.pecha_id: str = self.path.name
        self.layers: Dict[BASE_NAME, Dict[layer_type, AnnotationStore]] = defaultdict(
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

    def get_layer(self, base_name, layer_type):
        """
        This function returns a specific layer of the pecha.
        """
        if not self.layers[base_name]:
            self.get_layers(base_name)
        return self.layers[base_name][layer_type]

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
                layer.set_filename(str(target_layer_fn))
                layer.add_resource(
                    id=target_base_name,
                    filename=f"../../base/{target_base_fn.stem}.txt",
                )
                source_resouce = layer.resource(source_base_name)
                target_resource = layer.resource(target_base_name)
                layer = self.change_resource(source_resouce, target_resource, layer)
                layer.save()


class Pecha:
    def __init__(self, pecha_id: str, pecha_path: Path) -> None:
        self.id = pecha_id
        self.pecha_path = pecha_path
        self.metadata = self.load_metadata()
        self.bases = self.load_bases()
        self.layers = self.load_layers()
        self.storage: Optional[Storage] = None

    @classmethod
    def from_id(cls, pecha_id: str):
        pecha_path = clone_repo(pecha_id, PECHAS_PATH)
        return Pecha.from_path(pecha_path)

    @classmethod
    def from_path(cls, pecha_path: Path) -> "Pecha":
        pecha_id = pecha_path.stem
        return cls(pecha_id, pecha_path)

    @classmethod
    def create(cls, output_path: Path) -> "Pecha":
        pecha_id = get_initial_pecha_id()
        pecha_path = output_path / pecha_id
        pecha_path.mkdir(parents=True, exist_ok=True)
        return cls(pecha_id, pecha_path)

    @property
    def base_path(self) -> Path:
        base_path = self.pecha_path / "base"
        if not base_path.exists():
            base_path.mkdir(parents=True, exist_ok=True)
        return base_path

    @property
    def layer_path(self):
        layer_path = self.pecha_path / "layers"
        if not layer_path.exists():
            layer_path.mkdir(parents=True, exist_ok=True)
        return layer_path

    @property
    def metadata_path(self):
        return self.pecha_path / "metadata.json"

    def load_metadata(self):
        if not self.metadata_path.exists():
            return None

        with open(self.metadata_path) as f:
            metadata = json.load(f)

        return PechaMetaData(**metadata)

    def load_bases(self):
        bases = {}
        for base_file in self.base_path.rglob("*.txt"):
            base_name = base_file.stem
            bases[base_name] = base_file.read_text(encoding="utf-8")
        return bases

    def load_layers(self):
        layers: Dict[str, Dict[LayerEnum, List[AnnotationStore]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for layer_file in self.layer_path.rglob("*.json"):
            base_name = layer_file.parent.name
            ann_enum = LayerEnum(layer_file.stem.split("-")[0])
            layers[base_name][ann_enum].append(AnnotationStore(file=str(layer_file)))
        return layers

    def set_base(self, content: str, base_name=None):
        """
        This function sets the base layer of the pecha to a new text.
        """
        base_name = base_name if base_name else get_base_id()
        (self.base_path / f"{base_name}.txt").write_text(content)

        # add base to the attribute 'bases'
        if base_name not in self.bases:
            self.bases[base_name] = content

        # make a folder for the base in the 'layers' folder
        (self.layer_path / base_name).mkdir(parents=True, exist_ok=True)
        return base_name

    def add_layer(self, base_name: str, layer_type: LayerEnum):
        """
        Inputs:
            base_name: .txt file which this annotation is associated with
            layer_type: the type of annotation layer, it should be include in LayerEnum

        Process:
            - create an annotation store
            - add the resource to the annotation store
            - add the dataset to the annotation store

        Output:
            - annotation store
        """
        if base_name not in self.bases:
            raise ValueError(f"Base {base_name} does not exist.")

        ann_store = AnnotationStore(id=self.id)
        ann_store_path = (
            self.layer_path / base_name / f"{layer_type.value}-{get_base_id()}.json"
        )
        ann_store.set_filename(str(ann_store_path))
        ann_store.add_resource(
            id=base_name,
            filename=f"../../base/{base_name}.txt",
        )
        dataset_id = get_layer_collection(layer_type).value
        ann_store.add_dataset(id=dataset_id)
        self.layers[base_name][layer_type].append(ann_store)

        return ann_store, ann_store_path

    def check_annotation(self, annotation: Dict, layer_type: LayerEnum):
        """
        Inputs:annotation: annotation data
        Process: - check if the annotation data is valid
                - raise error if the annotation data is invalid
        """

        # Check if an annotation with LayerEnum is present in the annotation data
        if layer_type.value not in annotation.keys():
            raise ValueError(f"Annotation data should contain {layer_type.value} key.")

        # Check if the annotation with LayerEnum has Span value as tuple
        if not isinstance(annotation[layer_type.value], Dict):
            raise ValueError(
                f"The {layer_type.value} annotation should have a Span of 'start' and 'end'."
            )

        # Check if the annotataion data has a valid value
        for ann_name, ann_value in annotation.items():
            if not isinstance(ann_name, str):
                raise ValueError("The annotation metadata key should be a string.")

            if not isinstance(ann_value, (str, int, List, Dict)):
                raise ValueError(
                    "The annotation value should be either a string, int or a Span Dictionary."
                )

    def add_annotation(
        self, ann_store: AnnotationStore, annotation: Dict, layer_type: LayerEnum
    ):
        """
        Inputs: layer: annotation store, data: annotation data
        Process: add the annotation to the annotation store
        Output:annotation
        """
        self.check_annotation(annotation, layer_type)

        ann_resource = next(ann_store.resources())
        ann_dataset = next(ann_store.datasets())

        # Get annotation metadata / payloads
        ann_data = {k: v for k, v in annotation.items() if not isinstance(v, Dict)}
        # Add main annotation such as Chapter, Sabche, Segment into the annotation data
        ann_data[get_layer_group(layer_type).value] = layer_type.value

        # Get the start and end of the annotation
        start, end = (
            annotation[layer_type.value]["start"],
            annotation[layer_type.value]["end"],
        )
        text_selector = Selector.textselector(ann_resource, Offset.simple(start, end))

        # If ann data already exists, use it . Otherwise create a new one with new id
        prepared_ann_data = []
        for k, v in ann_data.items():
            try:
                ann_datas = list(ann_store.data(set=ann_dataset.id(), key=k, value=v))
                prepared_ann_data.append(ann_datas[0])
            except:  # noqa
                prepared_ann_data.append(
                    {
                        "id": get_annotation_id(),
                        "set": ann_dataset.id(),
                        "key": k,
                        "value": v,
                    }
                )

        ann_store.annotate(
            target=text_selector, data=prepared_ann_data, id=get_annotation_id()
        )
        return ann_store

    def set_metadata(self, pecha_metadata: PechaMetaData):
        self.metadata = pecha_metadata
        with open(self.metadata_path, "w") as f:
            json.dump(self.metadata.to_dict(), f, ensure_ascii=False, indent=2)

        return self.metadata

    def get_layer(self, basefile_name: str, annotation_type: LayerEnum):
        dir_to_search = self.layer_path / basefile_name
        ann_store_files = list(dir_to_search.glob(f"{annotation_type.value}*.json"))

        annotation_stores = [
            AnnotationStore(file=str(annotation_file))
            for annotation_file in ann_store_files
        ]

        if len(annotation_stores) == 1:
            return annotation_stores[0], ann_store_files[0]
        return annotation_stores, ann_store_files

    def publish(
        self,
        asset_path: Optional[Path] = None,
        asset_name: Optional[str] = "source_data",
        branch: Optional[str] = "main",
        is_private: bool = False,
    ):
        def prepare_repo_description(title):
            """
            Input: title which can be string, List of string, or an dictionary
            Return: a string, which will be used as repo description
            """
            if isinstance(title, str):
                return title
            if isinstance(title, list):
                return ", ".join(title)

            if isinstance(title, dict):
                return ", ".join([f"{k}: {v}" for k, v in title.items()])

            return title

        if not self.storage:
            self.storage = GithubStorage()
        if isinstance(self.storage, GithubStorage) and self.storage.is_git_repo(
            self.pecha_path
        ):
            local_repo = Repo(self.pecha_path)
            commit_and_push(repo=local_repo, message="Pecha update", branch=branch)
        else:
            self.storage.add_dir(
                path=self.pecha_path,
                description=prepare_repo_description(self.metadata.title),
                is_private=is_private,
                branch=branch,
            )
        asset_paths = []
        if asset_path:
            repo_name = self.id
            shutil.make_archive(asset_path.parent / asset_name, "zip", asset_path)
            asset_paths.append(f"{asset_path.parent / asset_name}.zip")
            create_release(
                repo_name,
                prerelease=False,
                asset_paths=asset_paths,
                org=self.storage.org_name,
                token=self.storage.token,
            )
            (asset_path.parent / f"{asset_name}.zip").unlink()
