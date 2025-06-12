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
- [Quickstart](#quickstart)
- [Key Concepts](#key-concepts)
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

## Quickstart

To get started, see the [Getting Started Guide](docs/getting-started.md).

---

## Key Concepts

- **Pecha**: The main object representing a text and its associated annotations and metadata.
- **Layer**: A collection of annotations of a specific type (e.g., segmentation, pagination) for a given base text.
- **Annotation**: A stand-off annotation (e.g., segment, page, language) defined by a span and optional metadata.
- **STAM**: The underlying model for stand-off annotation, enabling flexible, interoperable text annotation.

---


---


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

