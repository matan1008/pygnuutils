from io import StringIO

import pytest

from pygnuutils.basename import Basename, BasenameStub


class BasenameTestStub(BasenameStub):
    def __init__(self):
        self.stdout = StringIO()

    def print(self, *objects, sep=' ', end='\n', file=None, flush=False):
        print(*objects, sep=sep, end=end, flush=flush, file=self.stdout)


@pytest.mark.parametrize('path, output', [
    ('a/b/c/d', 'd\n'),
    ('/a/b/c/d', 'd\n'),
    ('a//b/c/d', 'd\n'),
    ('a/b/c/d/', 'd\n'),
    ('a/b/\\c/d/', 'd\n'),
    ('a', 'a\n'),
])
def test_sanity(path, output):
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename(path)
    assert stub.stdout.getvalue() == output


def test_zero():
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename('a/b', zero=True)
    assert stub.stdout.getvalue() == 'b\x00'


def test_suffix_single():
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename('a/b.h', '.h')
    assert stub.stdout.getvalue() == 'b\n'


def test_multiple():
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename('a/b', 'a/h', multiple=True)
    assert stub.stdout.getvalue() == 'b\nh\n'


def test_multiple_zero():
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename('a/b', 'a/h', multiple=True, zero=True)
    assert stub.stdout.getvalue() == 'b\x00h\x00'


def test_multiple_suffix():
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename('a/b.py', 'a/h.py', multiple=True, suffix='.py')
    assert stub.stdout.getvalue() == 'b\nh\n'


def test_implicit_multiple_suffix():
    stub = BasenameTestStub()
    basename = Basename(stub)
    basename('a/b.py', 'a/h.py', suffix='.py')
    assert stub.stdout.getvalue() == 'b\nh\n'
