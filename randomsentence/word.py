"""
Randomize a word from https://github.com/dwyl/english-words.
Rate commonness of a word with https://github.com/first20hours/google-10000-english
And some utility functions.
"""
import math
import re
import string
try:
    from secrets import choice
except ImportError:
    from random import choice

from randomsentence.dir import database_path

__doctest_skip__ = ['WordTool.get_random_word']


class WordTool:
    def __init__(self):
        """
        Commonness ref: https://github.com/first20hours/google-10000-english
        Word list: https://github.com/dwyl/english-words
        """
        with open(database_path('google-10000-english.txt')) as f:
            self.word_common = f.read().strip().split('\n')

        with open(database_path('words.txt')) as f:
            self.words = f.read().strip().split('\n')

    def get_random_word(self):
        """
        Randomize a word.
        :return str: a randomized word, attempting to use secrets.common first if present (Python >= 3.6)

        >>> WordTool().get_random_word()
        'huckle-bone'
        """
        return choice(self.words)

    def get_random_common_word(self, min_common=100, max_common=None):
        """

        :param int min_common:
        :param int | None max_common:
        :return:
        >>> WordTool().get_random_common_word()
        'sitemap'
        """
        return choice(self.word_common[min_common:max_common])

    def commonness(self, word):
        """
        Commonness of a word.

        :param str word: a word to check
        :return 0 | positive int | math.inf: If not in list: math.inf.
        If in list: the order in the list of commonness, starting from zero.

        >>> WordTool().commonness('bathrooms')
        7570
        >>> WordTool().commonness('Bathrooms')
        7570
        >>> WordTool().commonness('Elysa')
        inf
        """
        try:
            return self.word_common.index(word.lower())
        except ValueError:
            return math.inf

    @staticmethod
    def is_word(word):
        """
        Check if a keyword qualify as a "word". Punctuation removed, the word must be longer than 2 characters.

        :param str word: a word to check
        :return bool: whether is a word

        >>> WordTool.is_word('bathrooms')
        True
        >>> WordTool.is_word('adhserfsds')
        True
        >>> WordTool.is_word('on')
        False
        >>> WordTool.is_word('roll-on')
        True
        >>> WordTool.is_word('a.c.')
        False
        """
        word = re.sub('[{}]'.format(string.punctuation), '', word)
        if len(word) < 3:
            return False
        if word.isalpha():
            return True

        return False

    def in_dictionary(self, word):
        """
        Return whether the word is in https://github.com/dwyl/english-words
        :param word:
        :return:

        >>> WordTool().in_dictionary('on')
        True
        >>> WordTool().in_dictionary('e.g.')
        True
        >>> WordTool().in_dictionary('asdfrgrg')
        False
        """
        return word in self.words


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
