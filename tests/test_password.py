"""
5.3048 seconds per PasswordGenerator
0.0900 seconds per PasswordGenerator.refresh
0.0935 seconds per PasswordGenerator.new_password
0.0799 seconds per PasswordGenerator.new_pin
"""
import pytest

from memorable_password.password import PasswordGenerator

pg = PasswordGenerator()


def test_refresh():
    for token in pg.refresh():
        assert isinstance(token, str)


@pytest.mark.repeat
def test_new_password():
    """
    200 rep passed.
    :return:
    """
    password, overlap_list = pg.new_password()
    print(password)

    for token, is_overlap in overlap_list:
        if is_overlap:
            print(token)
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)


@pytest.mark.repeat
def test_new_pin():
    pin, overlap_list = pg.new_pin()
    print(pin)

    for token, is_overlap in overlap_list:
        if is_overlap:
            print(token)
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)


if __name__ == '__main__':
    from tests import timeit

    timeit(test_new_pin, rep=1000)