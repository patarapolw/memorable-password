"""
5.0696 seconds per ToSentence
"""
import pytest
from random import choice, randint
import string
from randomsentence import WordTool

from memorable_password.sentence import ToSentence

ts = ToSentence()
word_tool = WordTool()


@pytest.mark.repeat
@pytest.mark.parametrize('length', [4, 5, 6])
def test_from_keyword(length):
    """

    :param length: number of keywords to be converted to a sentence.
    :return:

    length:
    4 - Success 997 of 1000, 0.0038 seconds per test
    5 - Success 995 of 1000, 0.0064 seconds per test
    6 - Success 995 of 1000, 0.0167 seconds per test
    """
    keyword_list = [word_tool.get_random_word() for _ in range(length)]
    print(keyword_list)
    marked_sentence = ts.from_keywords(keyword_list)
    if marked_sentence is None:
        return False

    for token, is_overlap in marked_sentence:
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)

    return True


@pytest.mark.repeat
@pytest.mark.parametrize('length', [3, 4, 5, 6])
def test_from_initials(length):
    """

    :param length:
    :return:
    length:
    3 - Success 999 of 1000, 0.0134 seconds per test_from_initials
    4 - Success 1000 of 1000, 0.0345 seconds per test_from_initials, worst 3.8249
    5 - Success 1000 of 1000, 0.0414 seconds per test_from_initials, worst 3.8146
    6 - Success 1000 of 1000, 0.0549 seconds per test_from_initials, worst 4.1465
    """
    initials = ''.join([choice(string.ascii_letters) for _ in range(length)])

    marked_sentence = ts.from_initials(initials)
    if marked_sentence is None:
        print(initials)
        return False

    for token, is_overlap in marked_sentence:
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)

    return True


@pytest.mark.repeat
@pytest.mark.parametrize('length', [3, 4, 5, 6])
def test_from_pin(length):
    """

    :param length:
    :return:
    6 - Success 1000 of 1000, 0.0116 seconds per test_from_pin, worst 3.8537588119506836
    """
    pin = ''.join(choice(string.digits) for _ in range(length))

    marked_sentence = ts.from_pin(pin)
    if marked_sentence is None:
        print(pin)
        return False

    for token, is_overlap in marked_sentence:
        assert isinstance(token, str)
        assert isinstance(is_overlap, bool)

    return True


if __name__ == '__main__':
    from tests import timeit
    from functools import partial

    print(sorted(timeit(partial(test_from_pin, length=6), validator=lambda x: x, rep=1000), reverse=True)[:3])
