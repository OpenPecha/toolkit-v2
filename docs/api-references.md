# API REFERENCES

## Pecha

* [Pecha.from_path()](#pechafrom_path)
* [Pecha.create()](#pechacreate)
* [Pecha.base_path()](#pechabase_path)
* [Pecha.layer_path()](#pechalayer_path)
* [Pecha.metadata_path()](#pechametadata_path)
* [Pecha.get_base()](#pechaget_base)
* [Pecha.set_base()](#pechaset_base)
* [Pecha.get_layers()](#pechaget_layers)
* [Pecha.get_segmentation_layer_path()](#pechaget_segmentation_layer_path)
* [Pecha.get_first_layer_path()](#pechaget_first_layer_path)
* [Pecha.get_layer_by_ann_type()](#pechaget_layer_by_ann_type)
* [Pecha.get_layer_by_filename()](#pechaget_layer_by_filename)
* [Pecha.publish()](#pechapublish)
* [Pecha.merge_pecha()](#pechamerge_pecha)

### `Pecha.from_path()`
Loads a Pecha instance from a local path.

- **Parameters:**
  - `pecha_path` (Path): Path to the Pecha directory
- **Returns:** `Pecha` instance
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha import Pecha
  
  pecha = Pecha.from_path(Path("/path/to/pecha"))
  ```

### `Pecha.create()`
Creates a new Pecha instance in the specified output directory.

- **Parameters:**
  - `output_path` (Path): Directory where the Pecha should be created
  - `pecha_id` (str, optional): Custom Pecha ID. If not provided, a new ID will be generated
- **Returns:** `Pecha` instance
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha import Pecha
  
  pecha = Pecha.create(Path("./output"))
  ```

### `Pecha.base_path()`
Returns the path to the base directory which contains all the base files. If the directory does not exist, it is created.

- **Returns:** Path object pointing to the base directory
- **Example:**
  ```python
  base_dir = pecha.base_path
  print(base_dir)  # /path/to/pecha/base
  ```

### `Pecha.layer_path()`
Returns the path to the layers directory which contains all the annotation files. If the directory does not exist, it is created.

- **Returns:** Path object pointing to the layers directory
- **Example:**
  ```python
  layer_dir = pecha.layer_path
  print(layer_dir)  # /path/to/pecha/layers
  ```

### `Pecha.metadata_path()`
Returns the path to the metadata file.

- **Returns:** Path object pointing to the metadata file
- **Example:**
  ```python
  metadata_file = pecha.metadata_path
  print(metadata_file)  # /path/to/pecha/metadata.json
  ```

### `Pecha.get_base()`
Gets the content of a base file by its name.

- **Parameters:**
  - `base_name` (str): Name of the base file
- **Returns:** str containing the base text content
- **Example:**
  ```python
  base_text = pecha.get_base("base1")
  ```

### `Pecha.set_base()`
Sets the content of a base file.

- **Parameters:**
  - `content` (str): Text content to write to the base file
  - `base_name` (str, optional): Name for the base file. If not provided, a new ID will be generated
- **Returns:** str containing the base name
- **Example:**
  ```python
  base_name = pecha.set_base("This is the text content", "base1")
  ```

### `Pecha.get_layers()`
Returns all layers from the Pecha associated with the given base.

- **Parameters:**
  - `base_name` (str): Name of the base file
  - `from_cache` (bool, optional): Whether to load from cache. Defaults to False
- **Returns:** Generator yielding tuples of (layer_name, AnnotationStore)
- **Example:**
  ```python
  for layer_name, layer_store in pecha.get_layers("base1"):
      print(layer_name, layer_store)
  ```

### `Pecha.get_segmentation_layer_path()`
Gets the path to the first segmentation layer file.

- **Returns:** str containing the relative path to the segmentation layer file
- **Example:**
  ```python
  layer_path = pecha.get_segmentation_layer_path()
  ```

### `Pecha.get_first_layer_path()`
Gets the path to the first layer file.

- **Returns:** str containing the relative path to the first layer file
- **Example:**
  ```python
  layer_path = pecha.get_first_layer_path()
  ```

### `Pecha.get_layer_by_ann_type()`
Gets layers by annotation type.

- **Parameters:**
  - `base_name` (str): Name of the base file
  - `layer_type` (AnnotationType): Type of annotation to retrieve
- **Returns:** Tuple of (AnnotationStore or list of AnnotationStore, Path or list of Path)
- **Example:**
  ```python
  layer, layer_path = pecha.get_layer_by_ann_type("base1", AnnotationType.SEGMENTATION)
  ```

### `Pecha.get_layer_by_filename()`
Gets a layer by its filename.

- **Parameters:**
  - `base_name` (str): Name of the base file
  - `filename` (str): Name of the layer file
- **Returns:** AnnotationStore or None if not found
- **Example:**
  ```python
  layer = pecha.get_layer_by_filename("base1", "segmentation-1234.json")
  ```

### `Pecha.publish()`
Publishes the Pecha to GitHub and optionally creates a release with assets.

- **Parameters:**
  - `asset_path` (Path, optional): Path to the asset directory
  - `asset_name` (str, optional): Name for the asset. Defaults to "source_data"
  - `branch` (str, optional): Branch to publish to. Defaults to "main"
  - `is_private` (bool, optional): Whether the repository should be private. Defaults to False
- **Example:**
  ```python
  pecha.publish(
      asset_path=Path("./assets"),
      asset_name="source_data",
      branch="main",
      is_private=False
  )
  ```

### `Pecha.merge_pecha()`
Merges the layers of a source pecha into the current pecha.

- **Parameters:**
  - `source_pecha` (Pecha): The source Pecha instance
  - `source_base_name` (str): The base name of the source pecha
  - `target_base_name` (str): The base name of the target (current) pecha
- **Example:**
  ```python
  pecha.merge_pecha(source_pecha, "source_base", "target_base")
  ```
