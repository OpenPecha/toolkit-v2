
# Usage

## Pecha Parser

For a data to be converted to Pecha format. The input base file should be .txt format.

### Step 1. Splitting the text into atomic units
For effective text annotating, the text should be split into atomic units. 

#### Input base content
```
སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །

ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།" བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་།
```

#### Splited text in list
```
[
    'སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ',
    ' ',
    '།',
    '\n',
    'ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།"',
    ' ',
    'བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་།'
]
```

Important Notes:
- The atomic units is list of string where each string is a atomic unit.
- The atomic units should be split in a way that it should not break the meaning of the text.
- The string are split by space and new line characters as delimiter.
- The delimiter is also considered as atomic unit.

### Step 2. Annotating with parser pipeline
The atomic units are annotated with a parser pipeline. The parser pipeline take a list of annotation parser pipelist and apply each pipeline on the atomic units.

There is an option to use the default pipeline or create your own custom pipeline and pass them in the list.


### Step 3: Saving the Annotation in Pecha format
In pecha format, there will be three different kind of files:
1. base file: The base file is the original text file in .txt format.
2. annotation file: The annot file is the file that contains the annotations in .json STAM format.
3. meta file: The meta file is the file that contains the metadata of the base file in .json STAM format.


### Example
For this example, we will use the following input text and annote chapter and tsawa. 

For chapter, we will have to extract the chapter name and the content of the chapter. The chapter name is enclosed in double quotes and the content is the text after the double quotes.

For tsawa, we will consider text being separated by two newlines as tsawa.

One important thing is that following text should not be considered as tsawa.
`ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།" ` and `ch2-"སྡིག་པ་བཤགས་པ།"`. These are chapter names and should not be considered as tsawa.How do we do this?

Use filtering pipelines, where we can filter out the text that should not be considered as tsawa when we are going through each atomic string units. When building a particular chapter parser pipeline, you can pass the string through a series of inbuilt or custom filter pipelines to filter out the text that should not be considered.


#### Input text 
```
རྒྱ་གར་སྐད་དུ། བོ་དྷི་སཏྭ་ཙརྱ་ཨ་བ་ཏཱ་ར།

བོད་སྐད་དུ། བྱང་ཆུབ་སེམས་དཔའི་སྤྱོད་པ་ལ་འཇུག་པ།

སངས་རྒྱས་དང་བྱང་ཆུབ་སེམས་དཔའ་ཐམས་ཅད་ལ་ཕྱག་འཚལ་ལོ། །

ch1-"བྱང་ཆུབ་སེམས་ཀྱི་ཕན་ཡོན་བཤད་པ།" བདེ་གཤེགས་ཆོས་ཀྱི་སྐུ་མངའ་སྲས་བཅས་དང་། །ཕྱག་འོས་ཀུན་ལའང་གུས་པར་ཕྱག་འཚལ་ཏེ། །བདེ་གཤེགས་སྲས་ཀྱི་སྡོམ་ལ་འཇུག་པ་ནི། །ལུང་བཞིན་མདོར་བསྡུས་ནས་ནི་བརྗོད་པར་བྱ། །

ch2-"སྡིག་པ་བཤགས་པ།" དགེ་བ་བསྒོམ་ཕྱིར་བདག་གི་དད་པའི་ཤུགས། །འདི་དག་གིས་ཀྱང་རེ་ཞིག་འཕེལ་འགྱུར་ལ། །བདག་དང་སྐལ་བ་མཉམ་པ་གཞན་གྱིས་ཀྱང་། །ཅི་སྟེ་འདི་དག་མཐོང་ན་དོན་ཡོད་འགྱུར། །

དལ་འབྱོར་འདི་ནི་རྙེད་པར་ཤིན་ཏུ་དཀའ། །སྐྱེས་བུའི་དོན་སྒྲུབ་ཐོབ་པར་གྱུར་པ་ལ། །གལ་ཏེ་འདི་ལ་ཕན་པ་མ་བསྒྲུབས་ན། །ཕྱིས་འདི་ཡང་དག་འབྱོར་པར་ག་ལ་འགྱུར། །
```

### Code illustration

```python
from openpecha.pecha.parsers.plaintext.parser import PechaFrameWork

openpecha_framework = PechaFrameWork(input_text)

```
- instantiate the PechaFrameWork with the input text.
- The input text is split into atomic units, you can access the atomic units by calling `openpecha_framework.data['raw_string']`

```python

pipeline_definition = ["chapter_parser_pipe", "tsawa_parser_pipe"]
openpecha_framework.parser_pipeline(pipeline_definition)
```
- `pipeline_definition` is a list of parser pipeline that will be applied to the atomic units.
- If the element in the pipeline_definition is a string, it will be considered as a default pipeline.
- If the element in the pipeline_definition is a callable function, it will be considered as a custom pipeline.
- The information gained from the each parser pipeline is stored in `openpecha_framework.data`. Eg `openpecha_framework.data['Chapter']`, `openpecha_framework.data['Tsawa']`.


```python

pecha_convertor_pipe_definition = ["Chapter", "Tsawa"]
pecha_ann_file_paths = openpecha_framework.pecha_convertor_pipeline(
    pecha_convertor_pipe_definition, output_path
)
```
- `pecha_convertor_pipe_definition` is a list of convertor pipeline that will be applied to the data gained from the parser pipeline.
- The string given in the `pecha_convertor_pipe_definition` should be the key in the `openpecha_framework.data`.
- The string given should also be defined in the openpecha.pecha.layer.LayerEnum class.
