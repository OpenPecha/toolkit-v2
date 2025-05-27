
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">Toolkit V2</h3>

## Description

**Toolkit V2** is the second version of the existing toolkit.

A Python package designed for working with annotations within the **Openpecha** framework. Openpecha houses data in a distinct format called STAM.

**The Stand-off Text Annotation Model (STAM)** is a data model for stand-off text annotation, where all information related to a text is represented as annotations.

## Installation
Stable version:
```python
pip install openpecha
```

Daily Development version:
```
pip install git+https://github.com/OpenPecha/toolkit-v2.git
```

## Quickstart
To get started with the toolkit, we recommend following this [documentation](docs/getting-started.md).

## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@10zinten](https://github.com/10zinten)
- [@tsundue](https://github.com/tenzin3)


## Diving Deeper
- To learn more about the STAM data model, please refer to their following resources
  - [stam github](https://github.com/annotation/stam)
  - [stam python github](https://github.com/annotation/stam-python)
  - [stam python documentation](https://stam-python.readthedocs.io/en/latest/)
  - [stam python tutorial](https://github.com/annotation/stam-python/blob/master/tutorial.ipynb)

- To learn more about our Openpecha data framework refer to our own openpecha published paper [Taming the Wild Etext: Managing, Annotating, and Sharing Tibetan Corpora in Open Spaces](https://dl.acm.org/doi/abs/10.1145/3418060).

## Key Components

- **Pecha**: Core class for managing text and annotations
- **Parsers**: For various input formats (DOCX, OCR, Pedurma, etc.) converting to Pecha object.
- **Serializers**: For converting Pecha objects to different output formats
- **Layers**: Managing different types of annotations (segmentation, alignment, etc.)
- **Metadata**: Handling Pecha metadata and copyright information

