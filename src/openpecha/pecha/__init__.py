from collections import defaultdict
from pathlib import Path
from typing import Dict, Generator, Tuple, Union

from stam import AnnotationStore

from openpecha import utils
from openpecha.pecha.blupdate import update_layer

BASE_NAME = str
LAYER_NAME = str


class Pecha:
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

    def merge_pecha(
        self,
        source_pecha_path: Union[Path, str],
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

        source_pecha = Pecha(source_pecha_path)
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
                layer.add_resource(filename=str(target_base_fn))
                layer.set_filename(str(target_layer_fn))
                layer.save()
