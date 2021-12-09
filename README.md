[![Python application](https://github.com/matan1008/pygnuutils/workflows/Python%20application/badge.svg)](https://github.com/matan1008/pygnuutils/actions/workflows/python-app.yml "Python application action")
[![Pypi version](https://img.shields.io/pypi/v/pygnuutils.svg)](https://pypi.org/project/pygnuutils/ "PyPi package")
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/matan1008/pygnuutils.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/matan1008/pygnuutils/context:python)

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
