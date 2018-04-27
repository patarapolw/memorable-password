"""
10.8698 seconds per PasswordGenerator, do_markovify=False
25.7119 seconds per PasswordGenerator, do_markovify=True
0.0900 seconds per PasswordGenerator.refresh
0.0935 seconds per PasswordGenerator.new_password
0.0799 seconds per PasswordGenerator.new_pin
"""
import pytest

from memorable_password.password import GeneratePassword

pg = GeneratePassword()


def test_refresh():
    for token in pg.refresh():
        assert isinstance(token, str)


@pytest.mark.repeat
def test_new_initial_password():
    """
    200 rep passed.
    :return:
    """
    password, overlap_list = pg.new_initial_password()
    print(password)

    for token, is_overlap in overlap_list:
        if is_overlap:
            print(token)
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)


@pytest.mark.repeat
def test_new_diceware_password():
    """
    200 rep passed.
    :return:
    """
    password, overlap_list = pg.new_diceware_password()
    print(password)

    if overlap_list is None:
        return

    for token, is_overlap in overlap_list:
        if is_overlap:
            print(token)
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)


@pytest.mark.repeat
def test_new_common_diceware_password():
    password, overlap_list = pg.new_common_diceware_password()
    print(password, overlap_list)

    if overlap_list is not None:
        return True
    else:
        return False


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
    from functools import partial

    timeit(test_new_common_diceware_password)
