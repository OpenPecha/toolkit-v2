# Tutorials

## A Story of Parsing, Annotating, and Serializing Tibetan Text

Let's follow a story of how we can process a Tibetan text through our pipeline. We'll use a simple example of a Tibetan verse with its translation.

### Our Sample Data

Let's say we have this Tibetan text with its English translation:

```text
བདེ་གཤེགས་སྤྱན་རས་གཟིགས་དབང་ཕྱུག་ལ་ཕྱག་འཚལ་ལོ། །
I pay homage to the Lord Avalokiteśvara.

དེ་ཡི་མཚན་ཉིད་རྣམས་ནི་མཐོང་བ་མེད། །
His characteristics cannot be seen.

དེ་ཡི་སྐུ་ནི་མཐོང་བ་མེད། །
His body cannot be seen.

དེ་ཡི་ཡི་གེ་ནི་མཐོང་བ་མེད། །
His letters cannot be seen.
```

### Chapter 1: The Parser's Tale

Our parser's job is to break this text into meaningful segments. Let's create a parser that understands Tibetan verses:

```python
from typing import List, Dict, Any
from openpecha.pecha import Pecha
from openpecha.pecha.annotations import AnnotationModel, AnnotationType

class TibetanVerseParser:
    def __init__(self):
        self.segments = []
        self.current_position = 0
    
    def parse(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse Tibetan text into verses and their translations.
        """
        # Split by double newlines to separate verses
        verses = text.split('\n\n')
        
        for verse in verses:
            # Split into Tibetan and English
            lines = verse.strip().split('\n')
            if len(lines) >= 2:
                tibetan = lines[0].strip()
                english = lines[1].strip()
                
                # Create segment for Tibetan text
                tibetan_segment = {
                    'text': tibetan,
                    'start': self.current_position,
                    'end': self.current_position + len(tibetan),
                    'type': 'tibetan'
                }
                self.current_position += len(tibetan) + 1
                
                # Create segment for English translation
                english_segment = {
                    'text': english,
                    'start': self.current_position,
                    'end': self.current_position + len(english),
                    'type': 'translation'
                }
                self.current_position += len(english) + 2  # +2 for the newlines
                
                self.segments.extend([tibetan_segment, english_segment])
        
        return self.segments

# Let's try our parser
parser = TibetanVerseParser()
segments = parser.parse(our_tibetan_text)
print("Parsed segments:", segments)
```

### Chapter 2: The Annotation Adventure

Now that we have our segments, let's add annotations to mark them as Tibetan verses and translations:

```python
def create_verse_annotations(pecha: Pecha, segments: List[Dict[str, Any]]) -> List[AnnotationModel]:
    """
    Create annotations for Tibetan verses and their translations.
    """
    annotations = []
    
    for i, segment in enumerate(segments):
        # Create text selector
        text_selector = {
            "@type": "TextSelector",
            "resource": "base",
            "offset": {
                "@type": "Offset",
                "begin": {
                    "@type": "BeginAlignedCursor",
                    "value": segment['start']
                },
                "end": {
                    "@type": "BeginAlignedCursor",
                    "value": segment['end']
                }
            }
        }
        
        # Create annotation data
        annotation_data = {
            "@type": "AnnotationData",
            "@id": f"verse_{i}",
            "key": "verse_type",
            "value": {
                "@type": "String",
                "value": segment['type']
            }
        }
        
        # Create the annotation
        annotation = {
            "@type": "Annotation",
            "@id": f"ann_{i}",
            "target": text_selector,
            "data": [annotation_data]
        }
        
        annotations.append(annotation)
    
    return annotations

# Create annotations
annotations = create_verse_annotations(pecha, segments)
print("Created annotations:", annotations)
```

### Chapter 3: The Serializer's Journey

Finally, let's create a serializer to package everything together:

```python
class TibetanVerseSerializer:
    def __init__(self):
        self.annotation_store = {
            "@type": "AnnotationStore",
            "@id": "tibetan_verse_store",
            "resources": [
                {
                    "@type": "TextResource",
                    "@id": "base",
                    "@include": "verses.txt"
                }
            ],
            "annotationsets": [
                {
                    "@type": "AnnotationDataSet",
                    "@id": "verse_annotation",
                    "keys": [
                        {
                            "@type": "DataKey",
                            "@id": "verse_type"
                        }
                    ],
                    "data": []
                }
            ],
            "annotations": []
        }
    
    def serialize(self, pecha: Pecha, annotations: List[AnnotationModel]) -> Dict[str, Any]:
        """
        Serialize the pecha and its annotations.
        """
        # Add annotations to the store
        self.annotation_store["annotations"] = annotations
        
        # Add annotation data to the dataset
        for annotation in annotations:
            for data in annotation["data"]:
                self.annotation_store["annotationsets"][0]["data"].append(data)
        
        return self.annotation_store

# Let's serialize our data
serializer = TibetanVerseSerializer()
serialized_data = serializer.serialize(pecha, annotations)

# Save the serialized data
import json
with open('tibetan_verses.json', 'w', encoding='utf-8') as f:
    json.dump(serialized_data, f, ensure_ascii=False, indent=2)
```

### The Final Output

After running our pipeline, we get a JSON file that looks like this:

```json
{
  "@type": "AnnotationStore",
  "@id": "tibetan_verse_store",
  "resources": [
    {
      "@type": "TextResource",
      "@id": "base",
      "@include": "verses.txt"
    }
  ],
  "annotationsets": [
    {
      "@type": "AnnotationDataSet",
      "@id": "verse_annotation",
      "keys": [
        {
          "@type": "DataKey",
          "@id": "verse_type"
        }
      ],
      "data": [
        {
          "@type": "AnnotationData",
          "@id": "verse_0",
          "key": "verse_type",
          "value": {
            "@type": "String",
            "value": "tibetan"
          }
        },
        {
          "@type": "AnnotationData",
          "@id": "verse_1",
          "key": "verse_type",
          "value": {
            "@type": "String",
            "value": "translation"
          }
        }
        // ... more annotations ...
      ]
    }
  ],
  "annotations": [
    {
      "@type": "Annotation",
      "@id": "ann_0",
      "target": {
        "@type": "TextSelector",
        "resource": "base",
        "offset": {
          "@type": "Offset",
          "begin": {
            "@type": "BeginAlignedCursor",
            "value": 0
          },
          "end": {
            "@type": "BeginAlignedCursor",
            "value": 45
          }
        }
      },
      "data": [
        {
          "@type": "AnnotationData",
          "@id": "verse_0",
          "set": "verse_annotation"
        }
      ]
    }
    // ... more annotations ...
  ]
}
```

### Epilogue: What We've Learned

In this story, we've seen how to:
1. Parse Tibetan text into meaningful segments
2. Add annotations to mark different types of content
3. Serialize everything into a structured format

The resulting JSON file can be used by other tools to:
- Display the text with proper formatting
- Extract specific types of content
- Perform analysis on the text
- Create translations or other derived works

Remember that this is just one way to process Tibetan text. You can extend this pipeline to handle more complex cases, such as:
- Multiple translations
- Commentary layers
- Cross-references
- Metadata about the text
- And much more!