import pytest

from pygnuutils.human_readable import parse_specs, HumanReadableOption as HRO, human_readable


@pytest.mark.parametrize('specs, result_size, result_ops', [
    ('', 0, HRO.CEILING),
    ('human-readable', 1, HRO.AUTOSCALE | HRO.SI | HRO.BASE_1024),
    ('si', 1, HRO.AUTOSCALE | HRO.SI),
    ('k', 1000, HRO.SI),
    ('kB', 1000, HRO.SI | HRO.B),
    ('kiB', 1000, HRO.SI | HRO.BASE_1024),
    ('2k', 2000, HRO.CEILING),
    ('2kB', 2000, HRO.B),
    ('2kiB', 2000, HRO.BASE_1024),
    ('5', 5, HRO.CEILING),
    ('0x10', 16, HRO.CEILING),
    ('0x22kiB', 0x22 * 1000, HRO.BASE_1024),
    ('\'0x2kiB', 2000, HRO.BASE_1024 | HRO.GROUP_DIGITS),
    ('\'0b111GiB', 7000000000, HRO.BASE_1024 | HRO.GROUP_DIGITS),
])
def test_parse_specs(specs, result_size, result_ops):
    assert parse_specs(specs) == (result_size, result_ops)


@pytest.mark.parametrize('size, opts, from_block_size, to_block_size, result', [
    (1, HRO.SI | HRO.BASE_1024 | HRO.AUTOSCALE, 4096, 1, '4.0K'),
    (2, HRO.SI | HRO.BASE_1024 | HRO.AUTOSCALE, 4096, 1, '8.0K'),
    (14, HRO.SI | HRO.BASE_1024 | HRO.AUTOSCALE, 1, 1, '14'),
    (2048, HRO.SI | HRO.BASE_1024 | HRO.GROUP_DIGITS, 1, 1, '2,048'),
    (1000000, HRO.SI | HRO.GROUP_DIGITS, 1, 1, '1,000,000'),
    (1000000, HRO.SI, 1, 1000, '1000k'),
    (1000000, HRO.SI | HRO.BASE_1024, 1, 1000, '1000K'),
    (1000000, HRO.SI, 1, 1000000, '1M'),
])
def test_human_readable(size, opts, from_block_size, to_block_size, result):
    assert human_readable(size, opts, from_block_size, to_block_size) == result
