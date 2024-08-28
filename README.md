
<h1 align="center">
  <br>
  <a href="https://openpecha.org"><img src="https://avatars.githubusercontent.com/u/82142807?s=400&u=19e108a15566f3a1449bafb03b8dd706a72aebcd&v=4" alt="OpenPecha" width="150"></a>
  <br>
</h1>

<!-- Replace with 1-sentence description about what this tool is or does.-->

<h3 align="center">Toolkit V2</h3>

## Description

**Toolkit V2** is the second version of the existing toolkit.

A Python package designed for working with annotations within the **PechaData** framework. PechaData is a GitHub repository that houses data in a distinct format called STAM.

**The Stand-off Text Annotation Model (STAM)** is a data model for stand-off text annotation, where all information related to a text is represented as annotations.

## Quickstart
To get started with the toolkit, we recommend following this [documentation](docs/getting-started.md).

## Project owner(s)

<!-- Link to the repo owners' github profiles -->

- [@10zinten](https://github.com/10zinten)
- [@tsundue](https://github.com/tenzin3)

### Pecha Annotation Transfer


```py
source_pecha_path = Path("source pecha path")
target_pecha_path = Path("target pecha path")

source_base_name = "source base name"
target_base_name = "target base name"

source_pecha = StamPecha(source_pecha_path)
target_pecha = StamPecha(target_pecha_path)

target_pecha.merge_pecha(source_pecha, source_base_name, target_base_name)

```