
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


## Diving Deeper
- To learn more about the STAM data model, please refer to their following resources
  - [stam github](https://github.com/annotation/stam)
  - [stam python github](https://github.com/annotation/stam-python)
  - [stam python documentation](https://stam-python.readthedocs.io/en/latest/)
  - [stam python tutorial](https://github.com/annotation/stam-python/blob/master/tutorial.ipynb)

### Pecha Annotation Transfer
The following code snippet demonstrates how to transfer annotations from one pecha to another pecha.
If the annotations are done in two different base files, the annotations can be transferred from the source pecha to the target pecha.

```py

from pathlib import Path
from openpecha.pecha import Pecha

source_pecha_path = Path("source pecha path")
target_pecha_path = Path("target pecha path")

source_base_name = "source base name"
target_base_name = "target base name"

source_pecha = Pecha.from_path(source_pecha_path)
target_pecha = Pecha.from_path(target_pecha_path)

target_pecha.merge_pecha(source_pecha, source_base_name, target_base_name)

```

*__Important Note:__ In a pecha, there could be more than one base file. So above code snippet will transfer only the annotations which is related to the given base file name from source pecha to target pecha.*