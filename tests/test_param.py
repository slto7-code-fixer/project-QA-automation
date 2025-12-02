import pytest


@pytest.mark.parametrize("number,expected", [(1, True), (2, False), (3, True)])
def test_is_odd(number, expected):
    assert (number % 2 == 1) is expected
