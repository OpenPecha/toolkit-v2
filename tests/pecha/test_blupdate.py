from unittest import TestCase

from openpecha.pecha.blupdate import DiffMatchPatch


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
