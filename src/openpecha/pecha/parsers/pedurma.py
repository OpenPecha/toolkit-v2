import re

from stam import AnnotationStore, Selector

from botok import WordTokenizer
from botok.tokenizers.chunktokenizer import ChunkTokenizer

from openpecha.ids import get_id


wt = WordTokenizer()



def get_text_resource(collated_text):
    base_text = re.sub(r"\d+-\d+", "", collated_text)
    base_text = re.sub(r"\(\d+\) <.+?>", "", base_text)
    base_text = base_text.replace(":","")
    return base_text





def parse(collated_text):
    annotation_store = AnnotationStore(id=get_id("", length=8))
    text_resource = get_text_resource(collated_text)
    resource = annotation_store.add_resource(id=get_id("R", length=4), text=text_resource)
    add_annotations(annotation_store, collated_text, resource)
    return annotation_store
