# ChonjukChapterParser Class Documentation

## Overview

The `ChonjukChapterParser` class is responsible for extracting chapter annotations from Tibetan text data that contains specific chapter markers. 

## Input Data format

```
chX-"Chapter Title" Chapter Text
```

- X represents the chapter number.
- Chapter Title is the title of the chapter in double quotes.
- Chapter Text is the body of the chapter.

## Class Methods

### `__init__(self)`

- Initializes the `ChonjukChapterParser` instance.
- Sets up the configuration needed for parsing chapter annotations.

### `get_updated_text(self, text: str) -> str`

- Cleans the input text by removing chapter markers.
- Returns the cleaned text.

### `get_annotations(self, text: str) -> List[Dict]`

- Extracts chapter annotations from the input text.
- Get the updated annotation span after removing chapter markers.
- Returns a list of chapter annotations.

### `parse(self, input: str, output_path: Path = PECHAS_PATH, metadata: Union[Dict, Path] = None)`

- Extract chapter annotations from the text.
- Instantiate `Pecha` class and save the chapter annotations to the output path.


## Example Usage

Here is an example of how to use the `ChonjukChapterParser` to parse text and extract chapter annotations.

```python
from pathlib import Path

# Initialize the parser
parser = ChonjukChapterParser()

# Example input text
input_text = '''
རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར། 

བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ། 

ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།" བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །
ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །

ch2-"སྡིག་པ་བཤགས་པ།" དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །
'''

# Parse the input text and save to an output path
parser.parse(input_text, output_path=Path("/path/to/output"))
```

After running the above code, the chapter annotations will be extracted from the input text and saved to the specified output path.The `annotations` attribute of parser would look like this.

```python
assert parser.annotations == [
{
    "chapter_number": "1",
    "chapter_title": "བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།",
    "Chapter": {"start": 145, "end": 446},
},
{
    "chapter_number": "2",
    "chapter_title": "སྡིག་པ་བཤགས་པ།",
    "Chapter": {"start": 449, "end": 896},
},
]
```

The file structure on the output path would look like this:

```
- output_path(dir)
    - I00B6F749(dir)
        - base(dir)
            - da0c.txt
        - layers(dir)
            - da0c
                - Chapter-123.json
```

