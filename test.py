from stam import AnnotationStore

store = AnnotationStore(
    file="tests/pecha/serializers/pecha_db/commentary/data/IC3797777/layers/0301/Sapche-C111.json"
)


for ann in store:
    ann_data = {}
    print(str(ann))
    for data in ann:
        ann_data[data.key().id()] = str(data.value())

    print(ann_data)
