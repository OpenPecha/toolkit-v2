from openpecha.pecha import Pecha


def test_pecha_base_update():
    pecha = Pecha(path="tests/pecha/data/P0001")
    pecha.update_base("0001", "00123456789")
