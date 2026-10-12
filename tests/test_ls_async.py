import asyncio
from io import StringIO

import pytest

from pygnuutils.ls import AsyncLs, Ls, LsStub


class LsTestStub(LsStub):
    def __init__(self):
        self.stdout = StringIO()

    def print(self, *objects, sep=' ', end='\n', file=None, flush=False):
        print(*objects, sep=sep, end=end, flush=flush, file=self.stdout)

    def setlocale(self, locale_setting=''):
        super(LsTestStub, self).setlocale('C.UTF-8')


class AsyncLsTestStub(LsTestStub):
    def __init__(self):
        super(AsyncLsTestStub, self).__init__()
        self.suspensions = 0

    async def _suspend(self):
        self.suspensions += 1
        await asyncio.sleep(0)

    async def stat(self, path, dir_fd=None, follow_symlinks=True):
        await self._suspend()
        return super(AsyncLsTestStub, self).stat(path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

    async def readlink(self, path, dir_fd=None):
        await self._suspend()
        return super(AsyncLsTestStub, self).readlink(path, dir_fd=dir_fd)

    async def listdir(self, path='.'):
        await self._suspend()
        return super(AsyncLsTestStub, self).listdir(path)


@pytest.fixture
def tree(tmp_path):
    (tmp_path / 'hello.txt').write_text('hello')
    (tmp_path / '.hidden').write_text('hidden')
    (tmp_path / 'link').symlink_to('hello.txt')
    sub_dir = tmp_path / 'sub'
    sub_dir.mkdir()
    (sub_dir / 'world.txt').write_text('world')
    (sub_dir / 'deep').mkdir()
    (sub_dir / 'deep' / 'file').write_text('deep')
    return tmp_path


def sync_ls(*files, **options):
    stub = LsTestStub()
    Ls(stub)(*files, **options)
    return stub.stdout.getvalue()


@pytest.mark.parametrize('options', [
    {},
    {'long': True},
    {'recursive': True},
    {'all_': True},
    {'long': True, 'recursive': True, 'all_': True, 'classify': True},
])
def test_async_same_output_as_sync(tree, options):
    stub = AsyncLsTestStub()
    asyncio.run(AsyncLs(stub)(str(tree), **options))
    assert stub.suspensions
    assert stub.stdout.getvalue() == sync_ls(str(tree), **options)
    assert 'hello.txt' in stub.stdout.getvalue()


def test_async_no_such_file(tree):
    missing = str(tree / 'missing')
    stub = AsyncLsTestStub()
    asyncio.run(AsyncLs(stub)(missing, str(tree)))
    assert stub.stdout.getvalue() == sync_ls(missing, str(tree))
    assert stub.stdout.getvalue().startswith(f'ls: cannot access \'{missing}\'')


def test_sync_inside_running_event_loop(tree):
    async def main():
        return sync_ls(str(tree), long=True, recursive=True)

    assert asyncio.run(main()) == sync_ls(str(tree), long=True, recursive=True)


def test_sync_propagates_stub_errors(tree):
    class FailingStub(LsTestStub):
        def listdir(self, path='.'):
            raise PermissionError(13, 'Permission denied')

    with pytest.raises(PermissionError):
        Ls(FailingStub())(str(tree))
