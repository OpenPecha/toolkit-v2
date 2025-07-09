from openpecha.pecha import Pecha


class JsonSerializer:
    def get_base(self, pecha: Pecha):
        basename = list(pecha.bases().keys())[0]
        base = pecha.get_base(basename)
        return base
