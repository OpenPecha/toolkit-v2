from openpecha.utils import parse_root_mapping


def test_parse_root_mapping():
    input = "1"
    assert parse_root_mapping(input) == [1]

    input = "1,2,3,4"
    assert parse_root_mapping(input) == [1, 2, 3, 4]

    input = "1-4"
    assert parse_root_mapping(input) == [1, 2, 3, 4]

    input = "1-4,5-8"
    assert parse_root_mapping(input) == [1, 2, 3, 4, 5, 6, 7, 8]


test_parse_root_mapping()
