import os
from contextlib import contextmanager


@contextmanager
def cwd(path):
    """
    A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
