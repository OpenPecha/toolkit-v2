# API REFERENCES

## Pecha

* [Pecha.from_path()](#pechafrom_path)
* [Pecha.create()](#pechacreate)
* [Pecha.base_path()](#pechabase_path)


### Pecha.from_path()
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

### Pecha.create()
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

### Pecha.base_path()
Returns the path to the base directory which contains all the base files. If the directory does not exist, it is created.

- **Returns:** Path object pointing to the base directory
- **Example:**
  ```python
  base_dir = pecha.base_path
  print(base_dir)  # /path/to/pecha/base
  ```
