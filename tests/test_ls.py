import datetime
import re
from getpass import getuser
from io import StringIO

import pytest

from pygnuutils.ls import Ls, LsStub, LsConfig, Formats


class LsTestStub(LsStub):
    def __init__(self):
        self.stdout = StringIO()

    def print(self, *objects, sep=' ', end='\n', file=None, flush=False):
        print(*objects, sep=sep, end=end, flush=flush, file=self.stdout)

    def setlocale(self, locale_setting=''):
        super(LsTestStub, self).setlocale('C.UTF-8')


def test_single_file_dir_long(tmp_path):
    now = datetime.datetime.now()
    file_example = tmp_path / 'hello.txt'
    file_example.write_text('hello')
    file_example.chmod(0o664)
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=Formats.LONG_FORMAT))
    output = stub.stdout.getvalue().splitlines()
    assert output[0].startswith('total ')
    match = re.match(fr'-rw-rw-r-- 1 {getuser()} \w* 5 (.*) hello.txt', output[1])
    assert now.replace(second=0, microsecond=0, year=1900) <= datetime.datetime.strptime(match.group(1), '%b %d %H:%M')


def test_single_file_long(tmp_path):
    now = datetime.datetime.now()
    file_example = tmp_path / 'hello.txt'
    file_example.write_text('hello')
    file_example.chmod(0o664)
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(file_example), config=LsConfig(format=Formats.LONG_FORMAT))
    match = re.match(fr'-rw-rw-r-- 1 {getuser()} \w* 5 (.*) {file_example}', stub.stdout.getvalue())
    assert now.replace(second=0, microsecond=0, year=1900) <= datetime.datetime.strptime(match.group(1), '%b %d %H:%M')


def test_one_column(tmp_path):
    file_example = tmp_path / (('a' * 75) + '.txt')
    file_example.write_text('hello')
    file_example.chmod(0o664)
    file_example = tmp_path / 'hello_2.txt'
    file_example.write_text('hello')
    file_example.chmod(0o664)
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=Formats.MANY_PER_LINE, line_length=80))
    assert stub.stdout.getvalue().splitlines() == [
        'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa.txt',
        'hello_2.txt                                                                    '
    ]


def test_multiple_files_dir_long(tmp_path):
    now = datetime.datetime.now().replace(second=0, microsecond=0, year=1900)
    for i in range(20):
        file_example = tmp_path / f'hello_{i}.txt'
        file_example.write_text('hello')
        file_example.chmod(0o664)
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=Formats.LONG_FORMAT))
    output = stub.stdout.getvalue().splitlines()
    assert output[0].startswith('total ')
    for i, name in enumerate(sorted(map(str, range(20)))):
        match = re.match(fr'-rw-rw-r-- 1 {getuser()} \w* 5 (.*) hello_{name}.txt', output[i + 1])
        assert now <= datetime.datetime.strptime(match.group(1), '%b %d %H:%M')


def test_recursive_dir_long(tmp_path):
    now = datetime.datetime.now().replace(second=0, microsecond=0, year=1900)
    for dir_index in range(3):
        dir_path = tmp_path / f'test_dir_{dir_index}'
        dir_path.mkdir(exist_ok=True, parents=True, mode=0o755)
        for sub_dir_index in range(2):
            sub_dir_path = dir_path / f'test_sub_dir_{sub_dir_index}'
            sub_dir_path.mkdir(exist_ok=True, parents=True, mode=0o755)
            for i in range(2):
                file_example = sub_dir_path / f'hello_{i}.txt'
                file_example.write_text('hello')
                file_example.chmod(0o664)
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=Formats.LONG_FORMAT, recursive=True))
    root_path = str(tmp_path).replace('/', '\\/')
    output_pattern = (
        f'{root_path}:\n'
        'total \\d*\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_dir_0\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_dir_1\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_dir_2\n'
        '\n'
        f'{root_path}\\/test_dir_0:\n'
        'total \\d*\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_sub_dir_0\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_sub_dir_1\n'
        '\n'
        f'{root_path}\\/test_dir_0\\/test_sub_dir_0:\n'
        'total \\d*\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_0\\.txt\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_1\\.txt\n'
        '\n'
        f'{root_path}\\/test_dir_0\\/test_sub_dir_1:\n'
        'total \\d*\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_0\\.txt\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_1\\.txt\n'
        '\n'
        f'{root_path}\\/test_dir_1:\n'
        'total \\d*\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_sub_dir_0\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_sub_dir_1\n'
        '\n'
        f'{root_path}\\/test_dir_1\\/test_sub_dir_0:\n'
        'total \\d*\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_0\\.txt\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_1\\.txt\n'
        '\n'
        f'{root_path}\\/test_dir_1\\/test_sub_dir_1:\n'
        'total \\d*\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_0\\.txt\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_1\\.txt\n'
        '\n'
        f'{root_path}\\/test_dir_2:\n'
        'total \\d*\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_sub_dir_0\n'
        f'drwxr-xr-x \\d* {getuser()} \\w* \\d* (.*) test_sub_dir_1\n'
        '\n'
        f'{root_path}\\/test_dir_2\\/test_sub_dir_0:\n'
        'total \\d*\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_0\\.txt\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_1\\.txt\n'
        '\n'
        f'{root_path}\\/test_dir_2\\/test_sub_dir_1:\n'
        'total \\d*\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_0\\.txt\n'
        f'-rw-rw-r-- 1 {getuser()} \\w* 5 (.*) hello_1\\.txt\n'
    )
    match = re.match(output_pattern, stub.stdout.getvalue())
    for group in match.groups():
        assert now <= datetime.datetime.strptime(group, '%b %d %H:%M')


@pytest.mark.parametrize('format_, result', [
    (Formats.ONE_PER_LINE, 'hello.txt\n'),
    (Formats.MANY_PER_LINE, 'hello.txt\n'),
    (Formats.HORIZONTAL, 'hello.txt\n'),
    (Formats.WITH_COMMAS, 'hello.txt\n'),
])
def test_single_file_dir_short(tmp_path, format_, result):
    file_example = tmp_path / 'hello.txt'
    file_example.write_text('hello')
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=format_))
    assert stub.stdout.getvalue() == result


@pytest.mark.parametrize('format_, result_factory', [
    (Formats.ONE_PER_LINE, lambda file_example: f'{file_example}\n'),
    (Formats.MANY_PER_LINE, lambda file_example: f'{file_example}\n'),
    (Formats.HORIZONTAL, lambda file_example: f'{file_example}\n'),
    (Formats.WITH_COMMAS, lambda file_example: f'{file_example}\n'),
])
def test_single_file_short(tmp_path, format_, result_factory):
    file_example = tmp_path / "hello.txt"
    file_example.write_text('hello')
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(file_example), config=LsConfig(format=format_))
    assert stub.stdout.getvalue() == result_factory(file_example)


@pytest.mark.parametrize('format_, result', [
    (Formats.ONE_PER_LINE, ('hello_0.txt\n'
                            'hello_1.txt\n'
                            'hello_10.txt\n'
                            'hello_11.txt\n'
                            'hello_12.txt\n'
                            'hello_13.txt\n'
                            'hello_14.txt\n'
                            'hello_15.txt\n'
                            'hello_16.txt\n'
                            'hello_17.txt\n'
                            'hello_18.txt\n'
                            'hello_19.txt\n'
                            'hello_2.txt\n'
                            'hello_3.txt\n'
                            'hello_4.txt\n'
                            'hello_5.txt\n'
                            'hello_6.txt\n'
                            'hello_7.txt\n'
                            'hello_8.txt\n'
                            'hello_9.txt\n')),
    (Formats.MANY_PER_LINE, (
            'hello_0.txt   hello_12.txt  hello_16.txt  hello_2.txt  hello_6.txt\n'
            'hello_1.txt   hello_13.txt  hello_17.txt  hello_3.txt  hello_7.txt\n'
            'hello_10.txt  hello_14.txt  hello_18.txt  hello_4.txt  hello_8.txt\n'
            'hello_11.txt  hello_15.txt  hello_19.txt  hello_5.txt  hello_9.txt\n'
    )),
    (Formats.HORIZONTAL, (
            'hello_0.txt   hello_1.txt   hello_10.txt  hello_11.txt\n'
            'hello_12.txt  hello_13.txt  hello_14.txt  hello_15.txt\n'
            'hello_16.txt  hello_17.txt  hello_18.txt  hello_19.txt\n'
            'hello_2.txt   hello_3.txt   hello_4.txt   hello_5.txt \n'
            'hello_6.txt   hello_7.txt   hello_8.txt   hello_9.txt \n'
    )),
    (Formats.WITH_COMMAS, (
            'hello_0.txt, hello_1.txt, hello_10.txt, hello_11.txt, hello_12.txt,\n'
            'hello_13.txt, hello_14.txt, hello_15.txt, hello_16.txt, hello_17.txt,\n'
            'hello_18.txt, hello_19.txt, hello_2.txt, hello_3.txt, hello_4.txt, hello_5.txt,\n'
            'hello_6.txt, hello_7.txt, hello_8.txt, hello_9.txt\n'
    )),
])
def test_multiple_files_dir_short(tmp_path, format_, result):
    for i in range(20):
        file_example = tmp_path / f'hello_{i}.txt'
        file_example.write_text('hello')
        file_example.chmod(0o664)
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=format_, line_length=80))
    assert stub.stdout.getvalue() == result


@pytest.mark.parametrize('format_, result', [
    (Formats.ONE_PER_LINE, lambda tmp_path: (
            f'{tmp_path}:\n'
            'test_dir_0\n'
            'test_dir_1\n'
            'test_dir_2\n'
            '\n'
            f'{tmp_path}/test_dir_0:\n'
            'test_sub_dir_0\n'
            'test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_0:\n'
            'hello_0.txt\n'
            'hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_1:\n'
            'hello_0.txt\n'
            'hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1:\n'
            'test_sub_dir_0\n'
            'test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_0:\n'
            'hello_0.txt\n'
            'hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_1:\n'
            'hello_0.txt\n'
            'hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2:\n'
            'test_sub_dir_0\n'
            'test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_0:\n'
            'hello_0.txt\n'
            'hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_1:\n'
            'hello_0.txt\n'
            'hello_1.txt\n'
    )),
    (Formats.MANY_PER_LINE, lambda tmp_path: (
            f'{tmp_path}:\n'
            'test_dir_0  test_dir_1  test_dir_2\n'
            '\n'
            f'{tmp_path}/test_dir_0:\n'
            'test_sub_dir_0  test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_0:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_1:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1:\n'
            'test_sub_dir_0  test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_0:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_1:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2:\n'
            'test_sub_dir_0  test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_0:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_1:\n'
            'hello_0.txt  hello_1.txt\n'
    )),
    (Formats.HORIZONTAL, lambda tmp_path: (
            f'{tmp_path}:\n'
            'test_dir_0  test_dir_1  test_dir_2\n'
            '\n'
            f'{tmp_path}/test_dir_0:\n'
            'test_sub_dir_0  test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_0:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_1:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1:\n'
            'test_sub_dir_0  test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_0:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_1:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2:\n'
            'test_sub_dir_0  test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_0:\n'
            'hello_0.txt  hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_1:\n'
            'hello_0.txt  hello_1.txt\n'
    )),
    (Formats.WITH_COMMAS, lambda tmp_path: (
            f'{tmp_path}:\n'
            'test_dir_0, test_dir_1, test_dir_2\n'
            '\n'
            f'{tmp_path}/test_dir_0:\n'
            'test_sub_dir_0, test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_0:\n'
            'hello_0.txt, hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_0/test_sub_dir_1:\n'
            'hello_0.txt, hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1:\n'
            'test_sub_dir_0, test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_0:\n'
            'hello_0.txt, hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_1/test_sub_dir_1:\n'
            'hello_0.txt, hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2:\n'
            'test_sub_dir_0, test_sub_dir_1\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_0:\n'
            'hello_0.txt, hello_1.txt\n'
            '\n'
            f'{tmp_path}/test_dir_2/test_sub_dir_1:\n'
            'hello_0.txt, hello_1.txt\n'
    )),
])
def test_recursive_dir_short(tmp_path, format_, result):
    for dir_index in range(3):
        dir_path = tmp_path / f'test_dir_{dir_index}'
        dir_path.mkdir(exist_ok=True, parents=True)
        for sub_dir_index in range(2):
            sub_dir_path = dir_path / f'test_sub_dir_{sub_dir_index}'
            sub_dir_path.mkdir(exist_ok=True, parents=True)
            for i in range(2):
                file_example = sub_dir_path / f'hello_{i}.txt'
                file_example.write_text('hello')
    stub = LsTestStub()
    ls = Ls(stub)
    ls.run(str(tmp_path), config=LsConfig(format=format_, recursive=True))
    assert stub.stdout.getvalue() == result(tmp_path)
