[![Python application](https://github.com/matan1008/pygnuutils/workflows/Python%20application/badge.svg)](https://github.com/matan1008/pygnuutils/actions/workflows/python-app.yml "Python application action")
[![Pypi version](https://img.shields.io/pypi/v/pygnuutils.svg)](https://pypi.org/project/pygnuutils/ "PyPi package")

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
    * [CLI](#cli)
    * [Python](#python)

# Description

`pygnuutils` is a pure python implementation for GNU utils.

# Installation

Install the last released version using `pip`:

```shell
python3 -m pip install --user -U pygnuutils
```

Or install the latest version from sources:

```shell
git clone git@github.com:matan1008/pygnuutils.git
cd pygnuutils
python3 -m pip install --user -U -e .
```

# Usage

## CLI

You can run commands by using pygnuutils prefix. For example, in order to list `/tmp/foo` you can run:

```shell
pygnuutils ls -lRh /tmp/foo
```

## Python

To use `pygnuutils` you can write the following:

```python
from pygnuutils.ls import Ls

ls = Ls()
ls('/tmp', all_=True)
```

Perhaps the best reason to use this library instead of gnu is the dependency injection ability.

For example, in order to print a message each time a symlink is resolved:

```python
import os

from pygnuutils.ls import Ls, LsStub


class ReadlinkWatch(LsStub):
    def readlink(self, path, dir_fd=None):
        print(f'Resolving {path}...')
        return os.readlink(path, dir_fd=dir_fd)


ls = Ls(stub=ReadlinkWatch())
ls('/tmp', all_=True, long=True)
```

If the file system is reached with coroutines, use `AsyncLs`. Its stub implements `stat`, `readlink` and `listdir` as
coroutine functions, while the rest of the stub stays synchronous:

```python
import asyncio
import os

from pygnuutils.ls import AsyncLs, LsStub


class AsyncStub(LsStub):
    async def stat(self, path, dir_fd=None, follow_symlinks=True):
        return await asyncio.to_thread(os.stat, path, dir_fd=dir_fd, follow_symlinks=follow_symlinks)

    async def readlink(self, path, dir_fd=None):
        return await asyncio.to_thread(os.readlink, path, dir_fd=dir_fd)

    async def listdir(self, path='.'):
        return await asyncio.to_thread(os.listdir, path)


asyncio.run(AsyncLs(AsyncStub())('/tmp', all_=True, long=True))
```
