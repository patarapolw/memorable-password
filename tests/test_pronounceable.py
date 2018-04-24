from memorable_password import GeneratePassword
from pronounceable import Complexity

gp = GeneratePassword()
comp = Complexity()


def test_initial_complexity():
    """

    :return:
    Complexity: 9 - 25
    """
    password = gp.new_initial_password()[0]
    if password is not None:
        print(password, comp.complexity(password))
        return True
    else:
        return False


def test_diceware_complexity():
    """

    :return:
    Complexity: (-7) - 24
    """
    password = gp.new_diceware_password()[0]
    if password is not None:
        print(password, comp.complexity(password))
        return True
    else:
        return False


def test_common_diceware_complexity():
    """

    :return:
    Complexity: (-3) - 32
    """
    password = gp.new_common_diceware_password()[0]
    if password is not None:
        print(password, comp.complexity(password))
        return True
    else:
        return False


if __name__ == '__main__':
    from tests import timeit

    timeit(test_common_diceware_complexity, validator=lambda x: x)
