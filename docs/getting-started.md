# Getting started



## 1. Prerequisites

```Python version >=3.10```

## 2. Installation
**Stable version:**
```bash
pip install openpecha
```

**Development version:**
```bash
pip install git+https://github.com/OpenPecha/toolkit-v2.git
```

## 3. Load Pecha

```python
from pathlib import Path 
from openpecha.pecha import Pecha

pecha_path = Path("I34515448")
pecha = Pecha.from_path(pecha_path)
```

## 4. Read Annotations
This step shows how to access and iterate over annotations (e.g., segmentation, alignment) stored in a specific layer file using the STAM-based AnnotationStore.


```python
from stam import AnnotationStore

layer_path = "76C5/Segmentation-97DE.json"
annotation_path = pecha.layer_path / layer_path

for ann in AnnotationStore(file=str(annotation_path)):
    print(str(ann))

```

## 5. Reach out to us
If you encounter any issues, please create an issue [here](https://github.com/OpenPecha/toolkit-v2/issues/new).
You can also contact us 
- [@10zinten](https://github.com/10zinten)
- [@tsundue](https://github.com/tenzin3)
- [@ta4tsering](https://github.com/ta4tsering)



