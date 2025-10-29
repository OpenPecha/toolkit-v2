# Getting Started & Usage Guide

## Quickstart

### I. Create Pecha
To create a new Pecha (an annotated text corpus), you can use the `Pecha.create` method directly, or use a parser (e.g., for DOCX files):

```python
from pathlib import Path
from openpecha.pecha import Pecha

# Create an empty Pecha in a given output directory
output_path = Path("./output")
pecha = Pecha.create(output_path)
```

Or, to create a Pecha after parsing:

```python
from openpecha.pecha.parsers.docx.root import DocxRootParser
from openpecha.pecha.layer import AnnotationType

parser = DocxRootParser()
pecha, annotation_path = parser.parse(
    input="/path/to/file.docx",
    annotation_type=AnnotationType.SEGMENTATION,
    metadata={"title": {"en": "Sample Title"}, "language": "bo"},
    output_path=Path("/output_path/")
)
```
### II. Load Pecha
You can load an existing Pecha either from a local path after downloading from the openpecha backend:

```python
from openpecha.pecha import Pecha
from pathlib import Path

# Load from local path
pecha = Pecha.from_path(Path("/path/to/pecha"))

```

### III. Pecha Attributes
A `Pecha` object exposes several useful attributes:

- `pecha.id`: The Pecha's unique ID, generated from 8 digits UUID
- `pecha.pecha_path`: Filesystem path to the Pecha
- `pecha.metadata`: Metadata object (see below)
- `pecha.bases`: Dictionary of base file names to text
- `pecha.layers`: Dictionary of annotation layers


### IV. Metadata
Each Pecha has a `metadata` attribute, which is a `PechaMetaData` object. Example fields include:

- `id`: Pecha ID
- `title`: Title (can be a dict with language keys)
- `author`: Author(s)
- `language`: Language code (e.g., 'bo', 'en')
- `parser`: Name of the parser used
- `initial_creation_type`: How the Pecha was created (e.g., 'google_docx', 'ocr')
- `source_metadata`: Additional source info
- `copyright`, `licence`, etc.

You can update metadata by passing a dictionary:

```python
pecha.set_metadata({
    "title": {"en": "New Title"},
    "author": "Author Name",
    # ... other fields ...
})
```

### V. Base File
The base file is the plain text of the work. You can access and set base files:

```python
# Get base text by name
base_text = pecha.get_base("base1")

# Set a new base text
pecha.set_base("This is the text.", base_name="base1")
```

### VI. Annotations
Annotations are stored in layers, each corresponding to a type (segmentation, alignment, etc.).

- To access all layers for a base:

```python
for layer_name, layer_store in pecha.get_layers("base1"):
    print(layer_name, layer_store)
```

- To add a new annotation layer:

```python
from openpecha.pecha.layer import AnnotationType
layer, layer_path = pecha.add_layer("base1", AnnotationType.SEGMENTATION)
```

- To add an annotation to a layer:

```python
from openpecha.pecha.annotations import Span, SegmentationAnnotation
ann = SegmentationAnnotation(span=Span(start=0, end=10), index=1)
pecha.add_annotation(layer, ann, AnnotationType.SEGMENTATION)
layer.save()
```

- To get annotation data:

```python
from openpecha.pecha import get_anns
anns = get_anns(layer)
for ann in anns:
    print(ann)
```

### VII. Alignment Transfer

Alignment transfer allows you to map and serialize aligned segments between a root text and a commentary or translation Pecha. This is useful for exporting how commentary or translation segments correspond to the root text.

#### Commentary Alignment Transfer

To transfer alignment from a root Pecha to a commentary Pecha:

```python
from openpecha.pecha import Pecha
from openpecha.alignment.commentary_transfer import CommentaryAlignmentTransfer

# Load the root and commentary Pechas
root_pecha = Pecha.from_path("/path/to/root_pecha")
commentary_pecha = Pecha.from_path("/path/to/commentary_pecha")

# Specify the alignment layer IDs (relative to the layer directory)
root_alignment_id = "B5FE/alignment-6707.json"
commentary_alignment_id = "B014/alignment-2127.json"

# Get the transferred commentary segments as a list of strings
transfer = CommentaryAlignmentTransfer()
aligned_commentary = transfer.get_serialized_commentary(
    root_pecha,
    root_alignment_id,
    commentary_pecha,
    commentary_alignment_id,
)

for segment in aligned_commentary:
    print(segment)
```

If your commentary Pecha also has a segmentation layer, you can use:

```python
commentary_segmentation_id = "B014/segmentation-33FC.json"
aligned_commentary = transfer.get_serialized_commentary_segmentation(
    root_pecha,
    root_alignment_id,
    commentary_pecha,
    commentary_alignment_id,
    commentary_segmentation_id,
)
```

#### Translation Alignment Transfer

For translation alignment transfer, use the `TranslationAlignmentTransfer` class:

```python
from openpecha.pecha import Pecha
from openpecha.alignment.translation_transfer import TranslationAlignmentTransfer

root_pecha = Pecha.from_path("/path/to/root_pecha")
translation_pecha = Pecha.from_path("/path/to/translation_pecha")

root_alignment_id = "B5FE/alignment-6707.json"
translation_alignment_id = "B014/alignment-2127.json"

transfer = TranslationAlignmentTransfer()
aligned_translation = transfer.get_serialized_translation_alignment(
    root_pecha,
    root_alignment_id,
    translation_pecha,
    translation_alignment_id,
)

for segment in aligned_translation:
    print(segment)
```

If your translation Pecha also has a segmentation layer, use:

```python
translation_segmentation_id = "B014/segmentation-33FC.json"
aligned_translation = transfer.get_serialized_translation_segmentation(
    root_pecha,
    root_alignment_id,
    translation_pecha,
    translation_alignment_id,
    translation_segmentation_id,
)
```

#### Notes

- The alignment and segmentation layer IDs are typically found in the `layers` directory of each Pecha.
- The output is a list of strings, each representing a segment in the commentary or translation, aligned to the root text.


