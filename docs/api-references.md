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

## JsonSerializer

* [JsonSerializer.get_base()](#jsonserializerget_base)
* [JsonSerializer.to_dict()](#jsonserializerto_dict)
* [JsonSerializer.get_annotations()](#jsonserializerget_annotations)

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

## DocxAnnotationParser

* [DocxAnnotationParser.add_annotation()](#docxannotationparseradd_annotation)

## DocxAnnotationUpdate

* [DocxAnnotationUpdate.extract_layer_name()](#docxannotationupdateextract_layer_name)
* [DocxAnnotationUpdate.extract_layer_id()](#docxannotationupdateextract_layer_id)
* [DocxAnnotationUpdate.extract_layer_enum()](#docxannotationupdateextract_layer_enum)
* [DocxAnnotationUpdate.update_annotation()](#docxannotationupdateupdate_annotation)

## TranslationAlignmentTransfer

* [TranslationAlignmentTransfer.is_empty()](#translationalignmenttransferis_empty)
* [TranslationAlignmentTransfer.get_segmentation_ann_path()](#translationalignmenttransferget_segmentation_ann_path)
* [TranslationAlignmentTransfer.map_layer_to_layer()](#translationalignmenttransfermap_layer_to_layer)
* [TranslationAlignmentTransfer.get_root_pechas_mapping()](#translationalignmenttransferget_root_pechas_mapping)
* [TranslationAlignmentTransfer.get_translation_pechas_mapping()](#translationalignmenttransferget_translation_pechas_mapping)
* [TranslationAlignmentTransfer.mapping_to_text_list()](#translationalignmenttransfermapping_to_text_list)
* [TranslationAlignmentTransfer.get_serialized_translation_alignment()](#translationalignmenttransferget_serialized_translation_alignment)
* [TranslationAlignmentTransfer.get_serialized_translation_segmentation()](#translationalignmenttransferget_serialized_translation_segmentation)

## CommentaryAlignmentTransfer

* [CommentaryAlignmentTransfer.is_valid_ann()](#commentaryalignmenttransferis_valid_ann)
* [CommentaryAlignmentTransfer.get_segmentation_ann_path()](#commentaryalignmenttransferget_segmentation_ann_path)
* [CommentaryAlignmentTransfer.index_annotations_by_root()](#commentaryalignmenttransferindex_annotations_by_root)
* [CommentaryAlignmentTransfer.map_layer_to_layer()](#commentaryalignmenttransfermap_layer_to_layer)
* [CommentaryAlignmentTransfer.get_root_pechas_mapping()](#commentaryalignmenttransferget_root_pechas_mapping)
* [CommentaryAlignmentTransfer.get_commentary_pechas_mapping()](#commentaryalignmenttransferget_commentary_pechas_mapping)
* [CommentaryAlignmentTransfer.get_serialized_commentary()](#commentaryalignmenttransferget_serialized_commentary)
* [CommentaryAlignmentTransfer.get_serialized_commentary_segmentation()](#commentaryalignmenttransferget_serialized_commentary_segmentation)
* [CommentaryAlignmentTransfer.format_serialized_commentary()](#commentaryalignmenttransferformat_serialized_commentary)
* [CommentaryAlignmentTransfer.process_commentary_ann()](#commentaryalignmenttransferprocess_commentary_ann)

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
      metadata={"title": "Commentary Title", "type": "commentary", "parent": "P0001"},
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

### <a id="docxannotationparseradd_annotation"></a>`DocxAnnotationParser.add_annotation() -> Tuple[Pecha, annotation_path]`
Adds annotations to an existing Pecha from a DOCX file.

- **Parameters:**
  - `pecha` (Pecha): The Pecha instance to add annotations to
  - `type` (AnnotationType | str): Type of annotation to extract (ALIGNMENT, SEGMENTATION, or FOOTNOTE)
  - `docx_file` (Path): Path to the DOCX file containing annotations
  - `metadatas` (List[Any]): List of metadata objects to determine if the Pecha is root-related
- **Returns:** Tuple containing:
  - Pecha: The updated Pecha instance
  - annotation_path: Path to the created annotation layer file
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha.layer import AnnotationType
  from openpecha.pecha.parsers.docx.annotation import DocxAnnotationParser
  
  parser = DocxAnnotationParser()
  pecha, layer_path = parser.add_annotation(
      pecha=existing_pecha,
      type=AnnotationType.FOOTNOTE,
      docx_file=Path("path/to/annotations.docx"),
      metadatas=[metadata]
  )
  ```
- **Note:** 
  - The parser supports three types of annotations: ALIGNMENT, SEGMENTATION, and FOOTNOTE
  - For FOOTNOTE annotations, it uses DocxFootnoteParser
  - For root-related Pechas, it uses DocxRootParser
  - For other cases, it uses DocxSimpleCommentaryParser
  - The coordinates of annotations are automatically updated to match the base text

### <a id="docxannotationupdateextract_layer_name"></a>`DocxAnnotationUpdate.extract_layer_name() -> str`
Extracts the layer name from a layer path.

- **Parameters:**
  - `layer_path` (str): Path to the layer file
- **Returns:** str containing the layer name (filename without extension)
- **Example:**
  ```python
  updater = DocxAnnotationUpdate()
  layer_name = updater.extract_layer_name("path/to/segmentation-1234.json")
  print(layer_name)  # "segmentation-1234"
  ```

### <a id="docxannotationupdateextract_layer_id"></a>`DocxAnnotationUpdate.extract_layer_id() -> str`
Extracts the layer ID from a layer path.

- **Parameters:**
  - `layer_path` (str): Path to the layer file
- **Returns:** str containing the layer ID (last part of the filename after the hyphen)
- **Example:**
  ```python
  updater = DocxAnnotationUpdate()
  layer_id = updater.extract_layer_id("path/to/segmentation-1234.json")
  print(layer_id)  # "1234"
  ```

### <a id="docxannotationupdateextract_layer_enum"></a>`DocxAnnotationUpdate.extract_layer_enum() -> AnnotationType`
Extracts the annotation type from a layer path.

- **Parameters:**
  - `layer_path` (str): Path to the layer file
- **Returns:** AnnotationType enum value corresponding to the layer type
- **Example:**
  ```python
  updater = DocxAnnotationUpdate()
  layer_type = updater.extract_layer_enum("path/to/segmentation-1234.json")
  print(layer_type)  # AnnotationType.SEGMENTATION
  ```

### <a id="docxannotationupdateupdate_annotation"></a>`DocxAnnotationUpdate.update_annotation() -> Pecha`
Updates annotations in an existing Pecha from a DOCX file while preserving the layer ID.

- **Parameters:**
  - `pecha` (Pecha): The Pecha instance to update annotations in
  - `annotation_path` (str): Path to the existing annotation layer file
  - `docx_file` (Path): Path to the DOCX file containing new annotations
  - `metadatas` (List[Any]): List of metadata objects to determine if the Pecha is root-related
- **Returns:** Updated Pecha instance
- **Example:**
  ```python
  from pathlib import Path
  from openpecha.pecha.parsers.docx.update import DocxAnnotationUpdate
  
  updater = DocxAnnotationUpdate()
  updated_pecha = updater.update_annotation(
      pecha=existing_pecha,
      annotation_path="path/to/segmentation-1234.json",
      docx_file=Path("path/to/updated_annotations.docx"),
      metadatas=[metadata]
  )
  ```
- **Note:** 
  - The method preserves the original layer ID when updating annotations
  - It automatically determines the annotation type from the existing layer path
  - Uses DocxAnnotationParser internally to handle the actual annotation update

### <a id="translationalignmenttransferis_empty"></a>`TranslationAlignmentTransfer.is_empty() -> bool`
Checks if a text string is empty (contains only whitespace and newlines).

- **Parameters:**
  - `text` (str): The text to check
- **Returns:** bool indicating if the text is empty
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  is_empty = transfer.is_empty("  \n  ")  # True
  is_empty = transfer.is_empty("Some text")  # False
  ```

### <a id="translationalignmenttransferget_segmentation_ann_path"></a>`TranslationAlignmentTransfer.get_segmentation_ann_path() -> Path`
Gets the path to the first segmentation layer JSON file in a Pecha.

- **Parameters:**
  - `pecha` (Pecha): The Pecha instance to search in
- **Returns:** Path object pointing to the segmentation layer file
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  seg_path = transfer.get_segmentation_ann_path(pecha)
  ```

### <a id="translationalignmenttransfermap_layer_to_layer"></a>`TranslationAlignmentTransfer.map_layer_to_layer() -> Dict[int, List[int]]`
Maps annotations from source layer to target layer based on span overlap or containment.

- **Parameters:**
  - `src_layer` (AnnotationStore): Source annotation layer
  - `tgt_layer` (AnnotationStore): Target annotation layer
- **Returns:** Dictionary mapping source indices to lists of target indices
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  mapping = transfer.map_layer_to_layer(source_layer, target_layer)
  ```
- **Note:** 
  - Maps based on span overlap or containment
  - Excludes edge overlaps
  - Returns a sorted dictionary

### <a id="translationalignmenttransferget_root_pechas_mapping"></a>`TranslationAlignmentTransfer.get_root_pechas_mapping() -> Dict[int, List[int]]`
Gets mapping from a Pecha's alignment layer to its segmentation layer.

- **Parameters:**
  - `pecha` (Pecha): The Pecha instance
  - `alignment_id` (str): ID of the alignment layer
- **Returns:** Dictionary mapping alignment indices to segmentation indices
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  mapping = transfer.get_root_pechas_mapping(pecha, "alignment-1234.json")
  ```

### <a id="translationalignmenttransferget_translation_pechas_mapping"></a>`TranslationAlignmentTransfer.get_translation_pechas_mapping() -> Dict[int, List]`
Gets mapping from segmentation to alignment layer in a translation Pecha.

- **Parameters:**
  - `pecha` (Pecha): The translation Pecha instance
  - `alignment_id` (str): ID of the alignment layer
  - `segmentation_id` (str): ID of the segmentation layer
- **Returns:** Dictionary mapping segmentation indices to alignment indices
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  mapping = transfer.get_translation_pechas_mapping(
      pecha,
      "alignment-1234.json",
      "segmentation-5678.json"
  )
  ```

### <a id="translationalignmenttransfermapping_to_text_list"></a>`TranslationAlignmentTransfer.mapping_to_text_list() -> List[str]`
Flattens a mapping from translation to root text into a list of texts.

- **Parameters:**
  - `mapping` (Dict[int, List[str]]): Mapping of indices to text lists
- **Returns:** List of texts, with empty strings for missing indices
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  texts = transfer.mapping_to_text_list({1: ["text1"], 3: ["text2"]})
  # ["text1", "", "text2"]
  ```

### <a id="translationalignmenttransferget_serialized_translation_alignment"></a>`TranslationAlignmentTransfer.get_serialized_translation_alignment() -> List[str]`
Serializes root translation alignment text mapped to root segmentation text.

- **Parameters:**
  - `root_pecha` (Pecha): The root Pecha instance
  - `root_alignment_id` (str): ID of the root alignment layer
  - `root_translation_pecha` (Pecha): The translation Pecha instance
  - `translation_alignment_id` (str): ID of the translation alignment layer
- **Returns:** List of texts aligned with root segmentation
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  texts = transfer.get_serialized_translation_alignment(
      root_pecha,
      "alignment-1234.json",
      translation_pecha,
      "alignment-5678.json"
  )
  ```

### <a id="translationalignmenttransferget_serialized_translation_segmentation"></a>`TranslationAlignmentTransfer.get_serialized_translation_segmentation() -> List[str]`
Serializes root translation segmentation text mapped to root segmentation text.

- **Parameters:**
  - `root_pecha` (Pecha): The root Pecha instance
  - `root_alignment_id` (str): ID of the root alignment layer
  - `translation_pecha` (Pecha): The translation Pecha instance
  - `translation_alignment_id` (str): ID of the translation alignment layer
  - `translation_segmentation_id` (str): ID of the translation segmentation layer
- **Returns:** List of texts aligned with root segmentation
- **Example:**
  ```python
  transfer = TranslationAlignmentTransfer()
  texts = transfer.get_serialized_translation_segmentation(
      root_pecha,
      "alignment-1234.json",
      translation_pecha,
      "alignment-5678.json",
      "segmentation-9012.json"
  )
  ```


### <a id="commentaryalignmenttransferis_valid_ann"></a>`CommentaryAlignmentTransfer.is_valid_ann() -> bool`
Checks if an annotation is valid (exists and has non-empty text).

- **Parameters:**
  - `anns` (Dict[int, Dict[str, Any]]): Dictionary of annotations
  - `idx` (int): Index to check
- **Returns:** bool indicating if the annotation is valid
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  is_valid = transfer.is_valid_ann(annotations, 1)
  ```

### <a id="commentaryalignmenttransferget_segmentation_ann_path"></a>`CommentaryAlignmentTransfer.get_segmentation_ann_path() -> Path`
Gets the path to the first segmentation layer JSON file in a Pecha.

- **Parameters:**
  - `pecha` (Pecha): The Pecha instance to search in
- **Returns:** Path object pointing to the segmentation layer file
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  seg_path = transfer.get_segmentation_ann_path(pecha)
  ```

### <a id="commentaryalignmenttransferindex_annotations_by_root"></a>`CommentaryAlignmentTransfer.index_annotations_by_root() -> Dict[int, Dict[str, Any]]`
Indexes annotations by their root index.

- **Parameters:**
  - `anns` (List[Dict[str, Any]]): List of annotation dictionaries
- **Returns:** Dictionary mapping root indices to annotation dictionaries
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  indexed_anns = transfer.index_annotations_by_root(annotations)
  ```

### <a id="commentaryalignmenttransfermap_layer_to_layer"></a>`CommentaryAlignmentTransfer.map_layer_to_layer() -> Dict[int, List[int]]`
Maps annotations from source layer to target layer based on span overlap or containment.

- **Parameters:**
  - `src_layer` (AnnotationStore): Source annotation layer
  - `tgt_layer` (AnnotationStore): Target annotation layer
- **Returns:** Dictionary mapping source indices to lists of target indices
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  mapping = transfer.map_layer_to_layer(source_layer, target_layer)
  ```
- **Note:** 
  - Maps based on span overlap or containment
  - Excludes edge overlaps
  - Returns a sorted dictionary
  - Handles complex alignment indices (e.g., "1,2-4")

### <a id="commentaryalignmenttransferget_root_pechas_mapping"></a>`CommentaryAlignmentTransfer.get_root_pechas_mapping() -> Dict[int, List[int]]`
Gets mapping from a Pecha's alignment layer to its segmentation layer.

- **Parameters:**
  - `pecha` (Pecha): The Pecha instance
  - `alignment_id` (str): ID of the alignment layer
- **Returns:** Dictionary mapping alignment indices to segmentation indices
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  mapping = transfer.get_root_pechas_mapping(pecha, "alignment-1234.json")
  ```

### <a id="commentaryalignmenttransferget_commentary_pechas_mapping"></a>`CommentaryAlignmentTransfer.get_commentary_pechas_mapping() -> Dict[int, List[int]]`
Gets mapping from commentary Pecha's segmentation layer to alignment layer.

- **Parameters:**
  - `pecha` (Pecha): The commentary Pecha instance
  - `alignment_id` (str): ID of the alignment layer
  - `segmentation_id` (str): ID of the segmentation layer
- **Returns:** Dictionary mapping segmentation indices to alignment indices
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  mapping = transfer.get_commentary_pechas_mapping(
      pecha,
      "alignment-1234.json",
      "segmentation-5678.json"
  )
  ```

### <a id="commentaryalignmenttransferget_serialized_commentary"></a>`CommentaryAlignmentTransfer.get_serialized_commentary() -> List[str]`
Serializes commentary annotations with root/segmentation mapping and formatting.

- **Parameters:**
  - `root_pecha` (Pecha): The root Pecha instance
  - `root_alignment_id` (str): ID of the root alignment layer
  - `commentary_pecha` (Pecha): The commentary Pecha instance
  - `commentary_alignment_id` (str): ID of the commentary alignment layer
- **Returns:** List of formatted commentary texts
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  texts = transfer.get_serialized_commentary(
      root_pecha,
      "alignment-1234.json",
      commentary_pecha,
      "alignment-5678.json"
  )
  ```

### <a id="commentaryalignmenttransferget_serialized_commentary_segmentation"></a>`CommentaryAlignmentTransfer.get_serialized_commentary_segmentation() -> List[str]`
Serializes commentary segmentation annotations with root/segmentation mapping and formatting.

- **Parameters:**
  - `root_pecha` (Pecha): The root Pecha instance
  - `root_alignment_id` (str): ID of the root alignment layer
  - `commentary_pecha` (Pecha): The commentary Pecha instance
  - `commentary_alignment_id` (str): ID of the commentary alignment layer
  - `commentary_segmentation_id` (str): ID of the commentary segmentation layer
- **Returns:** List of formatted commentary texts
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  texts = transfer.get_serialized_commentary_segmentation(
      root_pecha,
      "alignment-1234.json",
      commentary_pecha,
      "alignment-5678.json",
      "segmentation-9012.json"
  )
  ```

### <a id="commentaryalignmenttransferformat_serialized_commentary"></a>`CommentaryAlignmentTransfer.format_serialized_commentary() -> str`
Formats a commentary text with chapter and segment information.

- **Parameters:**
  - `chapter_num` (int): Chapter number
  - `seg_idx` (int): Segment index
  - `text` (str): Commentary text
- **Returns:** Formatted string in the format "<chapter><segment>text"
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  formatted = transfer.format_serialized_commentary(1, 2, "Commentary text")
  # "<1><2>Commentary text"
  ```

### <a id="commentaryalignmenttransferprocess_commentary_ann"></a>`CommentaryAlignmentTransfer.process_commentary_ann() -> str | None`
Processes a single commentary annotation and returns the serialized string.

- **Parameters:**
  - `ann` (dict): The commentary annotation to process
  - `root_anns` (dict): Dictionary of root annotations
  - `root_map` (dict): Mapping from root alignment to segmentation
  - `root_segmentation_anns` (dict): Dictionary of root segmentation annotations
- **Returns:** Formatted commentary string or None if not valid
- **Example:**
  ```python
  transfer = CommentaryAlignmentTransfer()
  result = transfer.process_commentary_ann(
      commentary_ann,
      root_anns,
      root_map,
      root_segmentation_anns
  )
  ```


### <a id="jsonserializerget_base"></a>`JsonSerializer.get_base(pecha: Pecha) -> str`
Returns the base text from the first base in the given Pecha.

- **Parameters:**
  - `pecha` (Pecha): The Pecha object to extract the base from
- **Returns:** str containing the base text
- **Example:**
  ```python
  from openpecha.pecha.serializers.json_serializer import JsonSerializer
  base = JsonSerializer().get_base(pecha)
  ```

### <a id="jsonserializerto_dict"></a>`JsonSerializer.to_dict(ann_store: AnnotationStore, ann_type: AnnotationType) -> list[dict]`
Converts an AnnotationStore to a list of annotation dictionaries for the given annotation type.

- **Parameters:**
  - `ann_store` (AnnotationStore): The annotation store to convert
  - `ann_type` (AnnotationType): The type of annotation
- **Returns:** List of annotation dictionaries
- **Example:**
  ```python
  anns = JsonSerializer.to_dict(ann_store, AnnotationType.SEGMENTATION)
  ```

### <a id="jsonserializerget_annotations"></a>`JsonSerializer.get_annotations(pecha: Pecha, layer_paths: str | list[str]) -> dict`
Gets the base text and annotations for one or more layer paths from a Pecha.

- **Parameters:**
  - `pecha` (Pecha): The Pecha object
  - `layer_paths` (str or list of str): Layer path(s) like "B5FE/segmentation-4FD1.json"
- **Returns:** Dict with keys `base` (str) and `annotations` (dict of annotation lists)
- **Example:**
  ```python
  serializer = JsonSerializer()
  result = serializer.get_annotations(pecha, ["B5FE/segmentation-4FD1.json"])
  print(result["base"])
  print(result["annotations"])
  ```
