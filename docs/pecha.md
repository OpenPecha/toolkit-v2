# Pecha Class Documentation

## Overview

The `Pecha` class is designed to manage the loading, setting, and manipulating of text data and annotation layers associated with a Pecha. It provides functionality to load bases (text files) and layers (annotation files) from a specified path, allowing the user to add annotations, create new bases, and manage the metadata associated with these resources.

## Class Methods

### `__init__(self, pecha_id: str, pecha_path: Path)`

- Initializes the `Pecha` instance.
- Parameters:
  - `pecha_id` (str): The ID of the Pecha.
  - `pecha_path` (Path): The path to the Pecha's directory.
- Attributes:
  - `id_`: The Pecha ID.
  - `pecha_path`: The path to the Pecha.
  - `bases`: Loaded base texts.
  - `layers`: Loaded annotation layers.

### `from_id(cls, pecha_id: str)`

- Clone the repository for a Pecha ID and return a `Pecha` instance from the cloned path.
- Parameters:
  - `pecha_id` (str): The Pecha ID to clone and load.
- Returns: `Pecha` instance.

### `from_path(cls, pecha_path: Path) -> "Pecha"`

- Load a Pecha instance from a given path.
- Parameters:
  - `pecha_path` (Path): The path where the Pecha is located.
- Returns: `Pecha` instance.

### `create(cls, output_path: Path) -> "Pecha"`

- Create a new Pecha directory structure in a given output path.
- Parameters:
  - `output_path` (Path): The directory where the Pecha should be created.
- Returns: `Pecha` instance.

## Properties

### `base_path`

- Returns the path to the base directory which contains all the base files. If the directory does not exist, it is created.

### `layer_path`

- Returns the path to the layers directory which contains all the annotation files. If the directory does not exist, it is created.

### `metadata`

- Returns the metadata information for the Pecha.

## Methods

### `load_bases(self)`

- Loads the base text files from the base path into the `bases` attribute.
- Returns: Dictionary mapping base filenames to their content.

### `load_layers(self)`

- Loads annotation layers from the layer path into the `layers` attribute.
- Returns: Dictionary mapping base names to their layers and annotations.

### `set_base(self, content: str, base_name=None)`

- Set a new base text for the Pecha.
- Parameters:
  - `content` (str): The text content for the base.
  - `base_name` (str, optional): The name of the base. If not provided, a UUID is generated.
- Returns: `base_name`.

### `add_layer(self, base_name: str, layer_type: LayerEnum)`

- Add a new annotation layer for a given base.
- Parameters:
  - `base_name` (str): The name of the base file to associate with this layer.
  - `layer_type` (LayerEnum): The type of annotation layer.
- Returns: `AnnotationStore`.

### `check_annotation(self, annotation: Dict, layer_type: LayerEnum)`

- Validates the format of the annotation data.
- Parameters:
  - `annotation` (Dict): The annotation data.
  - `layer_type` (LayerEnum): The type of annotation.
- Raises `ValueError` if validation fails.

### `add_annotation(self, ann_store: AnnotationStore, annotation: Dict, layer_type: LayerEnum)`

- Add an annotation to the specified annotation store.
- Parameters:
  - `ann_store` (AnnotationStore): The annotation store/layer to add the annotation to.
  - `annotation` (Dict): The annotation data.
  - `layer_type` (LayerEnum): The type of annotation.
- Returns: `AnnotationStore`.

### `annotate_metadata(self, ann_store: AnnotationStore, metadata: dict)`

- Adds metadata to the specified annotation store.
- Parameters:
  - `ann_store` (AnnotationStore): The annotation store to add metadata to.
  - `metadata` (dict): The metadata to be added.
- Returns: `AnnotationStore`.

### `get_layer(self, basefile_name: str, annotation_type: LayerEnum)`

- Retrieve the annotation store(s) for a given base file and annotation type.
- Parameters:
  - `basefile_name` (str): The name of the base file.
  - `annotation_type` (LayerEnum): The type of annotation to retrieve.
- Returns: A single `AnnotationStore` or a list of `AnnotationStore` objects, depending on the number of matching layers found.

## Example Usage

```python
from pathlib import Path 

# Create a new Pecha instance from a path
pecha = Pecha.create(Path("output_path"))

# Add a base text
base_name = pecha.set_base("This is a new base text.")

# Add a layer
layer = pecha.add_layer(base_name, LayerEnum.chapter)

# Add an annotation to the layer
annotation = {
    "Chapter": {"start": 0, "end": 10},
    "title": "Chapter 1"
}
pecha.add_annotation(layer, annotation, LayerEnum.chapter)

# Save the layer 
layer.save()
```

## Code Deep Dive

### 1. Create a new Pecha instance
```python
from pathlib import Path 

pecha = Pecha.create(Path("output_path"))
```

This will create a new Pecha instance in the specified output path. The `Pecha` class with `pecha_id` attribute will be generated from `openpecha.ids.get_initial_pecha_id` and the `pecha_path` attribute will be set to the output path and `pecha_id` folder. After creating an `pecha` instance, the file structure will look like this:
```
- output_path(dir)
    - I00B6F749(dir)
```
I00B6F749 is the `pecha_id` generated by `openpecha.ids.get_initial_pecha_id`.

### 2. Add a base text
```python
base_name = pecha.set_base("This is a new base text.")
```

This will set a new base text for the Pecha instance. The `base_name` attribute will be set to a UUID generated by `uuid.uuid4()`. The base text will be saved in the `base_path` directory with the `base_name` as the filename.

```
- output_path(dir)
    - I00B6F749(dir)
        - base(dir)
            - da0c.txt
```

da0c.txt is the `base_name` generated by `uuid.uuid4()

### 3. Add a annotation layer
```python
layer = pecha.add_layer(base_name, LayerEnum.chapter)
```

This will add a new annotation layer for the specified base text. The `layer` attribute will be an `AnnotationStore` object with the `LayerEnum.chapter` as the layer type. When creating any annotation, the annotation must be associated with a layer where its layer type is mentioned in the `openpecha.pecha.layer.LayerEnum` class.

A particular pecha can have more than one layer with same layer type. For example, a pecha can have multiple `LayerEnum.segment` layers. So to differentiate when adding any layer, its final name will be `layer_type` and '-' followed by three randomly generated number.


### 4. Add an annotation to the layer
```python
annotation = {
    "Chapter": {"start": 0, "end": 10},
    "title": "Chapter 1"
}
pecha.add_annotation(layer, annotation, LayerEnum.chapter)
```

This will store the annotation in the `annotation store/layer`.
- The main data in the annotation such that `"Chapter": {"start": 0, "end": 10}` would be store as a text selector pointing to the base file.
- The main data in annotation should be present in the `annotation` argument and its key should be same as the `layer_type` value of the `layer`.
- Other annotation metadata such as `"title": "Chapter 1"` would be stored in the `annotation_data` attribute of the `annotation`.


### 5. Save the layer
```python
layer.save()
```

This will save the annotation layer under the `base name` which comes one level below the `layer_path` directory.



```
- output_path(dir)
    - I00B6F749(dir)
        - base(dir)
            - da0c.txt
        - layers(dir)
            - da0c
                - chapter-123.json
```