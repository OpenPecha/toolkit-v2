# OpenPecha Toolkit V2

<p align="center">
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
</p>

<h3 align="center">Toolkit V2</h3>

A Python package for working with stand-off text annotations in the [OpenPecha](https://openpecha.org) framework, built around the Stand-off Text Annotation Model (STAM). Toolkit V2 features robust parsing, transformation, and serialization of annotated buddhist textual corpora.

---

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Key Concepts](#key-concepts)
- [Quickstart](#quickstart)
- [Usage Guide](#Usage-Guide)
- [Tutorial](#Tutorial)
- [Diving Deeper](#diving-deeper)
- [Contributing](#contributing)
- [License](#license)
- [Project Owners](#project-owners)

---

## Introduction

**Toolkit V2** is the next-generation Python toolkit for managing annotated texts in the OpenPecha ecosystem. It provides:
- Tools for creating, editing, and serializing annotated corpora using the STAM model.
- Support for multiple annotation types (segmentation, alignment, pagination, language, etc.).
- Parsers for various input formats (DOCX, OCR, Pedurma, etc.).
- Serializers for exporting annotated data.

**STAM (Stand-off Text Annotation Model)** is a flexible data model for representing all information about a text as stand-off annotations, keeping the base text and annotations separate for maximum interoperability.

**OpenPecha Backend** hosted on Firebase, serves as the central storage system for texts and their corresponding annotations. While the toolkit handles parsing, editing, and serialization, all storage, access, and import operations are managed by the backend.

---

## Installation

**Stable version:**
```bash
pip install openpecha
```

**Development version:**
```bash
pip install git+https://github.com/OpenPecha/toolkit-v2.git
```

---
## Key Concepts

### Pecha
A Pecha is the core data model representing a text corpus with its annotations and metadata. Each Pecha:
- Has a unique ID (8-digit UUID)
- Contains one or more base texts
- Stores multiple annotation layers
- Includes metadata (title, author, language, etc.)
- Can be created from scratch or parsed from various formats (DOCX, OCR, etc.)

```Pecha (P0001)
├── metadata.json
├── base/
│   ├── base1.txt
│   └── base2.txt
└── layers/
    ├── segmentation-1234.json
    ├── alignment-5678.json
    ├── pagination-9012.json
    └── footnote-3456.json
```

Example of a Pecha's internal structure:
```Pecha (P0001)
├── metadata.json
│   ├── id: "P0001"
│   ├── title: {"en": "Sample Text", "bo": "དཔེ་ཚན།"}
│   ├── author: "Author Name"
│   └── language: "bo"
├── base/
│   └── base1.txt
│       └── "ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།..."
└── layers/
    ├── Segmentation-1234.json
    │   └── {"index": 1, "span": {"start": 0, "end": 10}, ...}
    ├── Alignment-5678.json
    │   └── {"alignment_index": "1-2", "span": {"start": 0, "end":   20}, ...}
    └── Pagination-9012.json
        └── {"page": 1, "span": {"start": 0, "end": 100}, ...}
```

### Layer
A Layer is a collection of annotations of a specific type for a given base text. Key features:
- Each layer has a specific type (e.g., Segmentation, Alignment, Pagination)
- Layers are stored as JSON files in the STAM format
- Common layer types include:
  - Segmentation: Divides text into meaningful segments
  - Alignment: Maps segments between different texts (e.g., root text and commentary)
  - Pagination: Marks page boundaries
  - Language: Indicates language of text segments
  - Footnote: Contains footnote annotations

### STAM (Stand-off Text Annotation Model)
STAM is the underlying data format for storing annotations. It:
- Keeps base text and annotations separate
- Uses a flexible JSON structure
- Supports multiple annotation types
- Enables interoperability between different systems
- Allows for complex annotation relationships

### Alignment Transfer
The toolkit provides specialized classes for handling alignment between texts:
- `CommentaryAlignmentTransfer`: Maps commentary segments to root text
- `TranslationAlignmentTransfer`: Maps translation segments to root text
- Both support serialization with chapter and segment information


```
Root Pecha (P0001)
├── metadata.json
├── base/
│   └── base1.txt
│       └── "ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།..."
└── layers/
    ├── Segmentation-1234.json
    │   └── {"index": 1, "span": {"start": 0, "end": 10}, ...}
    ├── Alignment-5678.json
        └── {"alignment_index": "1", "span": {"start": 0, "end":   20}, ...}

```

```
Commentary Pecha (P0002)
├── metadata.json
|      - type: commentary
|      - parent: P0001
├── base/
│   └── base1.txt
│       └── "ཨོཾ་མ་ཎི་པདྨེ་ཧཱུྃ།..."
└── layers/
    ├── Alignment-3904.json
        └── {"alignment_index": "1-2", "span": {"start": 0, "end":   30}, ...}

```

### Alignment Transfer Explained

The alignment transfer system is a crucial component that enables mapping and serialization of aligned segments between different types of Pechas. Here's a detailed breakdown:

#### 1. Root Pecha Structure
- Contains the original text in the base file
- Has a segmentation layer that divides the text into meaningful segments
- Includes an alignment layer that serves as the reference point for other Pechas

#### 2. Commentary Pecha Structure
- Contains the commentary text in its base file
- Has its own segmentation layer for dividing commentary into segments
- Contains an alignment layer that maps commentary segments to root text segments
- The alignment layer uses `alignment_index` to reference corresponding segments in the root text

#### 3. Alignment Process
- The alignment transfer system uses the alignment layers to:
  - Map commentary segments to their corresponding root text segments
  - Maintain the structural relationship between commentary and root text
  - Enable proper serialization of aligned content
  - Preserve the hierarchical relationship between texts

#### 4. Serialization Output
- The system generates serialized output that shows:
  - The relationship between commentary and root text segments
  - The hierarchical structure of the text
  - The mapping between different versions of the text

#### 5. Key Components
- `CommentaryAlignmentTransfer`: Handles mapping between root text and commentary
- `TranslationAlignmentTransfer`: Handles mapping between root text and translation
- Alignment layers: Store the mapping information between texts
- Segmentation layers: Define the segment boundaries in each text

#### 6. Usage Example
```python
# Create alignment transfer instance
transfer = CommentaryAlignmentTransfer()

# Get serialized commentary with alignment
aligned_commentary = transfer.get_serialized_commentary(
    root_pecha,
    root_alignment_id,
    commentary_pecha,
    commentary_alignment_id
)

# Process aligned segments
for segment in aligned_commentary:
    print(segment)  # Output: "<1><1>Commentary on first segment"
```

#### 7. Benefits
- Maintains structural integrity between different versions of the text
- Enables proper display of commentary in relation to root text
- Supports multiple levels of commentary and translation
- Preserves the hierarchical relationship between texts
- Facilitates easy navigation between related segments

---

## Quickstart

To get started, see the [Getting Started Guide](docs/getting-started.md).

---

## Usage Guide

To see Usage Guide, see the [Usage Guide](docs/usage.md).

---


## Tutorial Guide

To see Tutorial Guide, see the [Tutorial Guide](docs/tutorials.md)

---

## Diving Deeper
- [STAM GitHub](https://github.com/annotation/stam)
- [STAM Python GitHub](https://github.com/annotation/stam-python)
- [STAM Python Documentation](https://stam-python.readthedocs.io/en/latest/)
- [STAM Python Tutorial](https://github.com/annotation/stam-python/blob/master/tutorial.ipynb)
- [OpenPecha Paper](https://dl.acm.org/doi/abs/10.1145/3418060)

---

## Contributing
We welcome contributions! Please open issues or pull requests. For major changes, please open an issue first to discuss what you would like to change.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Project Owners
- [@10zinten](https://github.com/10zinten)
- [@tsundue](https://github.com/tenzin3)
- [@ta4tsering](https://github.com/ta4tsering)

