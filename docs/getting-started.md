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
from openpecha.pecha.serializers.json_serializer import JsonSerializer

serializer = JsonSerializer()
layer_path = "B5FE/segmentation-4FD1.json"
annotations = serializer.get_annotations(
    pecha=pecha, layer_paths=layer_path
)

```

## 5. Reach out to us
If you encounter any issues, please create an issue [here](https://github.com/OpenPecha/toolkit-v2/issues/new).
You can also contact us 
- [@10zinten](https://github.com/10zinten)
- [@tsundue](https://github.com/tenzin3)
- [@ta4tsering](https://github.com/ta4tsering)



