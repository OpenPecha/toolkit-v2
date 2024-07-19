from pathlib import Path
from typing import Generator, Union

from stam import AnnotationStore

from openpecha import utils


class Pecha:
    def __init__(self, path: Union[Path, str]):
        path = Path(path)
        self.run_checks(path)
        self.path = path.resolve()
        self.parent = self.path.parent
        self.pecha_id = self.path.name

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

    def get_layers(self, base_name) -> Generator[AnnotationStore, None, None]:
        """
        This function returns the layers of the pecha.

        Args:
            base_name (str): The base name to identify specific layers.

        Returns:
            Generator[AnnotationStore, None, None]: Yields instances of `AnnotationStore` as they are read from directory files.
        """

        for layer_fn in (self.layers_path / base_name).iterdir():
            rel_layer_fn = layer_fn.relative_to(self.parent)
            with utils.cwd(self.parent):
                store = AnnotationStore(file=str(rel_layer_fn))
            yield store

    def update_base(self, base_name, content):
        """
        This function updates the base layer of the pecha to a new text. It will recompute the existing layers into the new base layer.
        """
        for layer in self.get_layers(base_name):
            old_base = layer.resource(base_name).text()
            print(old_base)
        # self.set_base(base_name, content)
