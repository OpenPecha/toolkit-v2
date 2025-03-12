from openpecha.utils import chunk_strings, parse_root_mapping


def test_parse_root_mapping():
    input = "1"
    assert parse_root_mapping(input) == [1]

    input = "1,2,3,4"
    assert parse_root_mapping(input) == [1, 2, 3, 4]

    input = "1-4"
    assert parse_root_mapping(input) == [1, 2, 3, 4]

    input = "1-4,5-8"
    assert parse_root_mapping(input) == [1, 2, 3, 4, 5, 6, 7, 8]


def test_chunk_strings():
    # Less than chunk_size
    strings = ["1", "2", "3", "4", "5"]
    chunk_size = 10
    expected = [["1", "2", "3", "4", "5"]]
    assert chunk_strings(strings, chunk_size) == expected

    # More than chunk_size
    strings = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    chunk_size = 3
    expected = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["10"]]
    assert chunk_strings(strings, chunk_size) == expected

    # Equal to chunk_size
    strings = ["1", "2", "3", "4", "5"]
    chunk_size = 5
    expected = [["1", "2", "3", "4", "5"]]
    assert chunk_strings(strings, chunk_size) == expected

    # Empty list
    strings = []
    chunk_size = 5
    expected = []
    assert chunk_strings(strings, chunk_size) == expected

    # Evenly divisible
    strings = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    chunk_size = 2
    expected = [["1", "2"], ["3", "4"], ["5", "6"], ["7", "8"], ["9", "10"]]
    assert chunk_strings(strings, chunk_size) == expected
