# API REFERENCES

## Pecha

* [Pecha.from_path()](#pechafrom_path)
* [Pecha.create()](#pechacreate)
* [Pecha.base_path()](#pechabase_path)
* [Pecha.layer_path()](#pechalayer_path)
* [Pecha.metadata_path()](#pechametadata_path)
* [Pecha.get_base()](#pechaget_base)
* [Pecha.set_base()](#pechaset_base)
* [Pecha.add_layer()](#pechaadd_layer)
* [Pecha.add_annotation()](#pechaadd_annotation)
* [Pecha.set_metadata()](#pechaset_metadata)
* [Pecha.get_layers()](#pechaget_layers)
* [Pecha.get_segmentation_layer_path()](#pechaget_segmentation_layer_path)
* [Pecha.get_first_layer_path()](#pechaget_first_layer_path)
* [Pecha.get_layer_by_ann_type()](#pechaget_layer_by_ann_type)
* [Pecha.get_layer_by_filename()](#pechaget_layer_by_filename)
* [Pecha.publish()](#pechapublish)
* [Pecha.merge_pecha()](#pechamerge_pecha)

## DocxRootParser

* [DocxRootParser.parse()](#docxrootparserparse)
* [DocxRootParser.extract_anns()](#docxrootparserextract_anns)
* [DocxRootParser.extract_segmentation_anns()](#docxrootparserextract_segmentation_anns)
* [DocxRootParser.extract_alignment_anns()](#docxrootparserextract_alignment_anns)

## DocxSimpleCommentaryParser

* [DocxSimpleCommentaryParser.parse()](#docxsimplecommentaryparserparse)
* [DocxSimpleCommentaryParser.extract_anns()](#docxsimplecommentaryparserextract_anns)
* [DocxSimpleCommentaryParser.extract_segmentation_anns()](#docxsimplecommentaryparserextract_segmentation_anns)
* [DocxSimpleCommentaryParser.extract_alignment_anns()](#docxsimplecommentaryparserextract_alignment_anns)

### <a id="pechafrom_path"></a>`Pecha.from_path() -> Pecha`
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

### <a id="pechacreate"></a>`Pecha.create() -> Pecha`
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

### <a id="pechabase_path"></a>`Pecha.base_path() -> Path`
Returns the path to the base directory which contains all the base files. If the directory does not exist, it is created.

- **Returns:** Path object pointing to the base directory
- **Example:**
  ```python
  base_dir = pecha.base_path
  print(base_dir)  # /path/to/pecha/base
  ```

### <a id="pechalayer_path"></a>`Pecha.layer_path() -> Path`
Returns the path to the layers directory which contains all the annotation files. If the directory does not exist, it is created.

- **Returns:** Path object pointing to the layers directory
- **Example:**
  ```python
  layer_dir = pecha.layer_path
  print(layer_dir)  # /path/to/pecha/layers
  ```

### <a id="pechametadata_path"></a>`Pecha.metadata_path() -> Path`
Returns the path to the metadata file.

- **Returns:** Path object pointing to the metadata file
- **Example:**
  ```python
  metadata_file = pecha.metadata_path
  print(metadata_file)  # /path/to/pecha/metadata.json
  ```

### <a id="pechaget_base"></a>`Pecha.get_base() -> str`
Gets the content of a base file by its name.

- **Parameters:**
  - `base_name` (str): Name of the base file
- **Returns:** str containing the base text content
- **Example:**
  ```python
  base_text = pecha.get_base("base1")
  ```

### <a id="pechaset_base"></a>`Pecha.set_base() -> str`
Sets the content of a base file.

- **Parameters:**
  - `content` (str): Text content to write to the base file
  - `base_name` (str, optional): Name for the base file. If not provided, a new ID will be generated
- **Returns:** str containing the base name
- **Example:**
  ```python
  base_name = pecha.set_base("This is the text content", "base1")
  ```

### <a id="pechaadd_layer"></a>`Pecha.add_layer() -> Tuple[AnnotationStore, Path]`
Adds a new annotation layer for a given base.

- **Parameters:**
  - `base_name` (str): Name of the base file to associate with this layer
  - `layer_type` (AnnotationType): Type of annotation layer (must be included in AnnotationType enum)
- **Returns:** Tuple of (AnnotationStore, Path) containing:
  - AnnotationStore: The created annotation store
  - Path: Path to the layer file
- **Example:**
  ```python
  from openpecha.pecha.layer import AnnotationType
  
  # Add a segmentation layer
  layer, layer_path = pecha.add_layer("base1", AnnotationType.SEGMENTATION)
  
  # Add a chapter layer
  layer, layer_path = pecha.add_layer("base1", AnnotationType.CHAPTER)
  ```
- **Note:** The layer file will be created with a name format of `{layer_type}-{random_id}.json` in the layers directory under the base name folder.

### <a id="pechaadd_annotation"></a>`Pecha.add_annotation() -> AnnotationStore`
Adds an annotation to an existing annotation layer (Annotation Store).

- **Parameters:**
  - `ann_store` (AnnotationStore): The annotation store/layer to add the annotation to
  - `annotation` (BaseAnnotation): The annotation object to add (e.g., SegmentationAnnotation, CitationAnnotation)
  - `layer_type` (AnnotationType): The type of annotation (must match the layer type)
- **Returns:** AnnotationStore with the added annotation
- **Example:**
  ```python
  from openpecha.pecha.annotations import Span, SegmentationAnnotation
  from openpecha.pecha.layer import AnnotationType
  
  # Create a segmentation annotation
  ann = SegmentationAnnotation(span=Span(start=0, end=10), index=1)
  
  # Add the annotation to the layer
  layer = pecha.add_annotation(layer, ann, AnnotationType.SEGMENTATION)
  
  # Save the layer after adding annotations
  layer.save()
  ```
- **Note:** 
  - The annotation's span must be valid for the base text
  - The layer_type must match the type of annotation being added
  - The layer must be saved after adding annotations to persist the changes

### <a id="pechaset_metadata"></a>`Pecha.set_metadata() -> PechaMetaData`
Updates the Pecha's metadata with new values while preserving existing metadata fields if not overridden.

- **Parameters:**
  - `pecha_metadata` (Dict): Dictionary containing metadata fields to update. Can include:
    - `title` (Dict[str, str] | str): Title in different languages or single language
    - `author` (List[str] | Dict[str, str] | str): Author(s) information
    - `language` (str): Language code (e.g., 'bo', 'en')
    - `parser` (str): Name of the parser used
    - `initial_creation_type` (str): How the Pecha was created
    - `source_metadata` (Dict): Additional source information
    - `copyright` (Dict): Copyright information
    - `licence` (str): License type
- **Returns:** Updated PechaMetaData object
- **Example:**
  ```python
  # Update metadata with new values
  pecha.set_metadata({
      "title": {"en": "New Title", "bo": "གསར་བཅོས་ཁ་བྱང་།"},
      "author": ["Author 1", "Author 2"],
      "language": "bo",
      "source_metadata": {
          "id": "source123",
          "publisher": "Publisher Name"
      }
  })
  
  # Update specific fields while preserving others
  pecha.set_metadata({
      "title": {"en": "Updated Title"},
      "copyright": {
          "year": "2024",
          "holder": "Copyright Holder"
      }
  })
  ```
- **Note:** 
  - Existing metadata fields not included in the update dictionary will be preserved
  - The parser and initial_creation_type fields will be preserved from existing metadata if not specified
  - The metadata is automatically saved to the metadata.json file
  - Invalid metadata will raise a ValueError

### <a id="pechaget_layers"></a>`Pecha.get_layers() -> Generator[Tuple[str, AnnotationStore]`
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

### <a id="pechaget_segmentation_layer_path"></a>`Pecha.get_segmentation_layer_path() -> str`
Gets the path to the first segmentation layer file.

- **Returns:** str containing the relative path to the segmentation layer file
- **Example:**
  ```python
  layer_path = pecha.get_segmentation_layer_path()
  ```

### <a id="pechaget_first_layer_path"></a>`Pecha.get_first_layer_path() -> str`
Gets the path to the first layer file.

- **Returns:** str containing the relative path to the first layer file
- **Example:**
  ```python
  layer_path = pecha.get_first_layer_path()
  ```

### <a id="pechaget_layer_by_ann_type"></a>`Pecha.get_layer_by_ann_type() -> Union[Tuple[AnnotationStore, Path], Tuple[List[AnnotationStore], List[Path]]]`
Gets layers by annotation type.

- **Parameters:**
  - `base_name` (str): Name of the base file
  - `layer_type` (AnnotationType): Type of annotation to retrieve
- **Returns:** Tuple of (AnnotationStore or list of AnnotationStore, Path or list of Path)
- **Example:**
  ```python
  layer, layer_path = pecha.get_layer_by_ann_type("base1", AnnotationType.SEGMENTATION)
  ```

### <a id="pechaget_layer_by_filename"></a>`Pecha.get_layer_by_filename() -> Optional[AnnotationStore]`
Gets a layer by its filename.

- **Parameters:**
  - `base_name` (str): Name of the base file
  - `filename` (str): Name of the layer file
- **Returns:** AnnotationStore or None if not found
- **Example:**
  ```python
  layer = pecha.get_layer_by_filename("base1", "segmentation-1234.json")
  ```

### <a id="pechapublish"></a>`Pecha.publish() -> None`
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

### <a id="pechamerge_pecha"></a>`Pecha.merge_pecha() -> None`
Merges the layers of a source pecha into the current pecha.

- **Parameters:**
  - `source_pecha` (Pecha): The source Pecha instance
  - `source_base_name` (str): The base name of the source pecha
  - `target_base_name` (str): The base name of the target (current) pecha
- **Example:**
  ```python
  pecha.merge_pecha(source_pecha, "source_base", "target_base")
  ```

### <a id="docxrootparserparse"></a>`DocxRootParser.parse() -> Tuple[Pecha, annotation_path]`
Parses a DOCX file and creates a Pecha object with annotations.

- **Parameters:**
  - `input` (str | Path): Path to the DOCX file to be parsed
  - `annotation_type` (AnnotationType): Type of annotation to extract (SEGMENTATION or ALIGNMENT)
  - `metadata` (Dict): Dictionary containing metadata for the Pecha
  - `output_path` (Path, optional): Directory where the Pecha should be created. Defaults to PECHAS_PATH
  - `pecha_id` (str | None, optional): Custom Pecha ID. If not provided, a new ID will be generated
- **Returns:** Tuple containing:
  - Pecha: The created Pecha instance
  - annotation_path: Path to the created annotation layer file
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha.layer import AnnotationType
  from openpecha.pecha.parsers.docx.root import DocxRootParser
  
  parser = DocxRootParser()
  pecha, layer_path = parser.parse(
      input="path/to/file.docx",
      annotation_type=AnnotationType.SEGMENTATION,
      metadata={"title": "Sample Title"},
      output_path=Path("./output")
  )
  ```

### <a id="docxrootparserextract_anns"></a>`DocxRootParser.extract_anns() -> Tuple[List[BaseAnnotation], str]`
Extracts text and annotations from a DOCX file.

- **Parameters:**
  - `docx_file` (Path): Path to the DOCX file
  - `annotation_type` (AnnotationType): Type of annotation to extract (SEGMENTATION or ALIGNMENT)
- **Returns:** Tuple containing:
  - List[BaseAnnotation]: List of extracted annotations
  - str: The extracted base text
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha.layer import AnnotationType
  from openpecha.pecha.parsers.docx.root import DocxRootParser
  
  parser = DocxRootParser()
  anns, base = parser.extract_anns(
      Path("path/to/file.docx"),
      AnnotationType.SEGMENTATION
  )
  ```

### <a id="docxrootparserextract_segmentation_anns"></a>`DocxRootParser.extract_segmentation_anns() -> Tuple[List[SegmentationAnnotation], str]`
Extracts segmentation annotations from numbered text.

- **Parameters:**
  - `numbered_text` (Dict[str, str]): Dictionary mapping segment numbers to text content
- **Returns:** Tuple containing:
  - List[SegmentationAnnotation]: List of segmentation annotations
  - str: The concatenated base text
- **Example:**
  ```python
  from openpecha.pecha.parsers.docx.root import DocxRootParser
  
  parser = DocxRootParser()
  numbered_text = {
      "1": "First segment",
      "2": "Second segment"
  }
  anns, base = parser.extract_segmentation_anns(numbered_text)
  ```

### <a id="docxrootparserextract_alignment_anns"></a>`DocxRootParser.extract_alignment_anns() -> Tuple[List[AlignmentAnnotation], str]`
Extracts alignment annotations from numbered text.

- **Parameters:**
  - `numbered_text` (Dict[str, str]): Dictionary mapping segment numbers to text content
- **Returns:** Tuple containing:
  - List[AlignmentAnnotation]: List of alignment annotations
  - str: The concatenated base text
- **Example:**
  ```python
  from openpecha.pecha.parsers.docx.root import DocxRootParser
  
  parser = DocxRootParser()
  numbered_text = {
      "1": "First segment",
      "2": "Second segment"
  }
  anns, base = parser.extract_alignment_anns(numbered_text)
  ```

### <a id="docxsimplecommentaryparserparse"></a>`DocxSimpleCommentaryParser.parse() -> Tuple[Pecha, annotation_path]`
Parses a DOCX file and creates a commentary Pecha object with annotations.

- **Parameters:**
  - `input` (str | Path): Path to the DOCX file to be parsed
  - `annotation_type` (AnnotationType): Type of annotation to extract (SEGMENTATION or ALIGNMENT)
  - `metadata` (Dict[str, Any]): Dictionary containing metadata for the Pecha
  - `output_path` (Path, optional): Directory where the Pecha should be created. Defaults to PECHAS_PATH
  - `pecha_id` (str | None, optional): Custom Pecha ID. If not provided, a new ID will be generated
- **Returns:** Tuple containing:
  - Pecha: The created Pecha instance
  - annotation_path: Path to the created annotation layer file
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha.layer import AnnotationType
  from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
  
  parser = DocxSimpleCommentaryParser()
  pecha, layer_path = parser.parse(
      input="path/to/commentary.docx",
      annotation_type=AnnotationType.ALIGNMENT,
      metadata={"title": "Commentary Title", "commentary_of": "P0001"},
      output_path=Path("./output")
  )
  ```

### <a id="docxsimplecommentaryparserextract_anns"></a>`DocxSimpleCommentaryParser.extract_anns() -> Tuple[List[BaseAnnotation], str]`
Extracts text and annotations from a commentary DOCX file.

- **Parameters:**
  - `docx_file` (Path): Path to the DOCX file
  - `annotation_type` (AnnotationType): Type of annotation to extract (SEGMENTATION or ALIGNMENT)
- **Returns:** Tuple containing:
  - List[BaseAnnotation]: List of extracted annotations
  - str: The extracted base text
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha.layer import AnnotationType
  from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
  
  parser = DocxSimpleCommentaryParser()
  anns, base = parser.extract_anns(
      Path("path/to/commentary.docx"),
      AnnotationType.ALIGNMENT
  )
  ```

### <a id="docxsimplecommentaryparserextract_segmentation_anns"></a>`DocxSimpleCommentaryParser.extract_segmentation_anns() -> Tuple[List[SegmentationAnnotation], str]`
Extracts segmentation annotations from numbered commentary text.

- **Parameters:**
  - `numbered_text` (Dict[str, str]): Dictionary mapping segment numbers to text content
- **Returns:** Tuple containing:
  - List[SegmentationAnnotation]: List of segmentation annotations
  - str: The concatenated base text
- **Example:**
  ```python
  from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
  
  parser = DocxSimpleCommentaryParser()
  numbered_text = {
      "1": "First commentary segment",
      "2": "Second commentary segment"
  }
  anns, base = parser.extract_segmentation_anns(numbered_text)
  ```

### <a id="docxsimplecommentaryparserextract_alignment_anns"></a>`DocxSimpleCommentaryParser.extract_alignment_anns() -> Tuple[List[AlignmentAnnotation], str]`
Extracts alignment annotations from numbered commentary text, handling root text references.

- **Parameters:**
  - `numbered_text` (Dict[str, str]): Dictionary mapping segment numbers to text content
- **Returns:** Tuple containing:
  - List[AlignmentAnnotation]: List of alignment annotations with root text references
  - str: The concatenated base text
- **Example:**
  ```python
  from openpecha.pecha.parsers.docx.commentary.simple import DocxSimpleCommentaryParser
  
  parser = DocxSimpleCommentaryParser()
  numbered_text = {
      "1": "1-2 First commentary segment",
      "2": "3-4 Second commentary segment"
  }
  anns, base = parser.extract_alignment_anns(numbered_text)
  ```
- **Note:** The commentary text can include root text references in the format "1-2 Commentary text" where "1-2" refers to the root text segments being commented on.
