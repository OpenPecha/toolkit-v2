
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

### Step 2. Annotating with pipeline
The atomic units are annotated with a parser pipeline. The parser pipeline take a list of annotation parser pipelist and apply each pipeline on the atomic units.

There is an option to use the default pipeline or create your own custom pipeline and pass them in the list.


### Step 3: Saving the Annotation in Pecha format
In pecha format, there will be three different kind of files:
1. base file: The base file is the original text file in .txt format.
2. annotation file: The annot file is the file that contains the annotations in .json STAM format.
3. meta file: The meta file is the file that contains the metadata of the base file in .json STAM format.


