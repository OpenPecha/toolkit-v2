from unittest import TestCase

import pytest

from openpecha.pecha.blupdate import Blupdate, DiffMatchPatch


class TestDiffMatchPatch(TestCase):
    def setUp(self):
        pass

    def test_insertion(self):
        old_base = "Hello"
        new_base = "Hello World"
        diff = DiffMatchPatch(old_base, new_base)

        assert diff.get_updated_coord(0) == 0
        assert diff.get_updated_coord(1) == 1
        assert diff.get_updated_coord(5) == 11  # insertion at the end
        assert diff.get_updated_coord(4) == 4  # before insertion
        assert diff.get_updated_coord(3) == 3

    def test_deletion(self):
        old_base = "Hello World"
        new_base = "Hello"
        diff = DiffMatchPatch(old_base, new_base)

        assert diff.get_updated_coord(0) == 0
        assert diff.get_updated_coord(5) == 5  # end of retained text
        assert diff.get_updated_coord(6) == 5  # start of deleted text
        assert diff.get_updated_coord(10) == 5
        assert diff.get_updated_coord(11) == 5  # end of original string

    def test_insertion_in_between(self):
        old_base = "Hello World"
        new_base = "Hello!! World"
        diff = DiffMatchPatch(old_base, new_base)

        assert diff.get_updated_coord(0) == 0
        assert diff.get_updated_coord(5) == 7
        assert diff.get_updated_coord(6) == 8  # shift due to '!!' insertion at 5
        assert diff.get_updated_coord(10) == 12  # overall shift of 2
        assert diff.get_updated_coord(11) == 13

    def test_deletion_in_between(self):
        old_base = "Good morning, Everyone"
        new_base = "Good Everyone"
        diff = DiffMatchPatch(old_base, new_base)

        assert diff.get_updated_coord(0) == 0
        assert diff.get_updated_coord(4) == 4  # "Good"
        assert diff.get_updated_coord(5) == 5
        assert diff.get_updated_coord(12) == 5  # within deleted " morning,"
        assert diff.get_updated_coord(17) == 8  # start of "Everyone" shifts left
        assert diff.get_updated_coord(23) == 14  # end of original

    def test_insertion_and_deletion(self):
        old_base = "Good morning, Ladies and Gentlemen"
        new_base = "Good Attractive Ladies and Gentlemen"
        diff = DiffMatchPatch(old_base, new_base)

        assert diff.get_updated_coord(0) == 0
        assert diff.get_updated_coord(5) == 5  # after insertion of " Attractive"
        assert diff.get_updated_coord(14) == 16
        assert diff.get_updated_coord(15) == 17
        assert diff.get_updated_coord(len(old_base)) == len(new_base)


@pytest.fixture(params=[{"srcbl": "abefghijkl", "dstbl": "abcdefgkl"}])
def inputs(request):
    return request.param


@pytest.fixture(
    params=[
        {
            "input": {"srcbl": "abefghijkl", "dstbl": "abcdefgkl"},
            "expected_result": [(0, 2, 0), (2, 5, 2), (8, 10, -1)],
        },
        {"input": {"srcbl": "abcd", "dstbl": "cd"}, "expected_result": [(2, 4, -2)]},
    ]
)
def compute_cctv_test_cases(request):
    return request.param


def test_compute_cctv(compute_cctv_test_cases):
    updater = Blupdate(
        compute_cctv_test_cases["input"]["srcbl"],
        compute_cctv_test_cases["input"]["dstbl"],
    )

    result = updater.cctv

    assert result == compute_cctv_test_cases["expected_result"]


@pytest.fixture(
    params=[
        {"srcblcoord": 3, "expected_result": (2, True)},
        {"srcblcoord": 7, "expected_result": (1, False)},
        {"srcblcoord": 9, "expected_result": (-1, True)},
        {"srcblcoord": 5, "expected_result": (1, False)},
    ]
)
def cctv_for_coord_test_cases(request):
    return request.param


def test_get_cctv_for_coord(inputs, cctv_for_coord_test_cases):
    updater = Blupdate(inputs["srcbl"], inputs["dstbl"])

    result = updater.get_cctv_for_coord(cctv_for_coord_test_cases["srcblcoord"])

    assert result == cctv_for_coord_test_cases["expected_result"]


@pytest.fixture(
    params=[
        {"srcblcoord": 3, "expected_result": ("abe", "fghi")},
        {"srcblcoord": 7, "expected_result": ("fghi", "jkl")},
    ]
)
def get_context_test_cases(request):
    return request.param


def test_get_context(inputs, get_context_test_cases):
    updater = Blupdate(inputs["srcbl"], inputs["dstbl"], context_len=4)

    result = updater.get_context(get_context_test_cases["srcblcoord"])

    assert result == get_context_test_cases["expected_result"]


@pytest.fixture(
    params=[
        {
            "input": {"srcbl": "abefghijkl", "dstbl": "abcdefgkl"},
            "context": ("fghi", "jkl"),
            "dstcoordestimate": 8,
            "expected_result": 7,
        },
        {
            "input": {"srcbl": "abefghijkl", "dstbl": "abcdefgkl"},
            "context": ("ab", "efgh"),
            "dstcoordestimate": 4,
            "expected_result": 4,
        },
        {
            "input": {"srcbl": "abefghijkl", "dstbl": "abcdefgkl"},
            "context": ("ghij", "kl"),
            "dstcoordestimate": 7,
            "expected_result": 7,
        },
        {
            "input": {"srcbl": "abefghijkl", "dstbl": "abcdefgkl"},
            "context": ("ghij", "kl"),
            "dstcoordestimate": 7,
            "expected_result": 7,
        },
        {  # deleting chars of length >= content_len at start
            "input": {"srcbl": "abcdefgkl", "dstbl": "efgkl"},
            "context": ("", "abcd"),
            "dstcoordestimate": 0,
            "expected_result": -1,
        },
    ]
)
def dmp_find_test_cases(request):
    return request.param


def test_dmp_find(dmp_find_test_cases):
    updater = Blupdate(
        dmp_find_test_cases["input"]["srcbl"],
        dmp_find_test_cases["input"]["dstbl"],
        context_len=4,
    )
    updater.get_cctv_for_coord(0)

    result = updater.dmp_find(
        dmp_find_test_cases["context"], dmp_find_test_cases["dstcoordestimate"]
    )

    assert result == dmp_find_test_cases["expected_result"]


@pytest.fixture(
    params=[
        {"srcblcoord": 0, "expected_result": 0},
        {"srcblcoord": 2, "expected_result": 4},
        {"srcblcoord": 7, "expected_result": 7},
    ]
)
def updated_coord(request):
    return request.param


def test_updated_coord(inputs, updated_coord):
    updater = Blupdate(inputs["srcbl"], inputs["dstbl"], context_len=4)

    result = updater.get_updated_coord(updated_coord["srcblcoord"])

    assert result == updated_coord["expected_result"]
