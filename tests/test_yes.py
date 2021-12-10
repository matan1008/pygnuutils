from io import StringIO

from pygnuutils.yes import Yes, YesStub


class YesTestStub(YesStub):
    def __init__(self, yes_count=-1):
        self.stdout = StringIO()
        self._yes_count = yes_count
        self.current_count = 0

    def print(self, *objects, sep=' ', end='\n', file=None, flush=False):
        if self.current_count == self._yes_count:
            raise KeyboardInterrupt()
        print(*objects, sep=sep, end=end, flush=flush, file=self.stdout)
        self.current_count += 1


def test_sanity():
    stub = YesTestStub(5)
    yes = Yes(stub)
    yes()
    assert stub.stdout.getvalue().splitlines() == ['y'] * 5


def test_specifying_string():
    stub = YesTestStub(5)
    yes = Yes(stub)
    yes('hey')
    assert stub.stdout.getvalue().splitlines() == ['hey'] * 5


def test_specifying_multiple_strings():
    stub = YesTestStub(5)
    yes = Yes(stub)
    yes('hey', 'you')
    assert stub.stdout.getvalue().splitlines() == ['hey you'] * 5
