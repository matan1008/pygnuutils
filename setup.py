from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent.resolve(strict=True)
VERSION = '0.0.2'
PACKAGE_NAME = 'pygnuutils'
PACKAGES = [p for p in find_packages() if not p.startswith('tests')]


def parse_requirements():
    reqs = []
    with open(BASE_DIR / 'requirements.txt', 'r') as fd:
        for line in fd.readlines():
            line = line.strip()
            if line:
                reqs.append(line)
    return reqs


def get_description():
    return (BASE_DIR / 'README.md').read_text()


if __name__ == '__main__':
    setup(
        version=VERSION,
        name=PACKAGE_NAME,
        description='A python implementation for GNU utils',
        long_description=get_description(),
        long_description_content_type='text/markdown',
        cmdclass={},
        packages=PACKAGES,
        data_files=[('.', ['requirements.txt'])],
        author='Matan Perelman',
        install_requires=parse_requirements(),
        entry_points={
            'console_scripts': [
                'pygnuutils=pygnuutils.__main__:main',
            ],
        },
        classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
        url='https://github.com/matan1008/pygnuutils',
        project_urls={
            'pygnuutils': 'https://github.com/matan1008/pygnuutils'
        },
        tests_require=['pytest'],
    )
