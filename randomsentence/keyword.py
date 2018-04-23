import nltk
from time import time
try:
    from secrets import choice
except ImportError:
    from random import choice

from randomsentence.brown import Brown

__doctest_skip__ = ['KeywordParse.from_keyword_list', 'KeywordParse.from_initials_list']


class KeywordParse:
    def __init__(self):
        self.brown = Brown()

    def from_keyword_list(self, keyword_list, strictness=2, timeout=3):
        """
        Convert a list of keywords to sentence. The result is sometimes None

        :param list keyword_list: a list of string
        :param int | None strictness: None for highest strictness. 2 or 1 for a less strict POS matching
        :param float timeout: timeout of this function
        :return list of tuple: sentence generated

        >>> KeywordParse().from_keyword_list(['Love', 'blind', 'trouble'])
        [('For', False), ('love', True), ('to', False), ('such', False), ('blind', True), ('we', False), ('must', False), ('turn', False), ('to', False), ('the', False), ('trouble', True)]
        """
        keyword_tags = nltk.pos_tag(keyword_list)

        start = time()
        while time() - start < timeout:
            index = 0
            output_list = []
            tagged_sent = self.brown.get_tagged_sent()
            for word, tag in tagged_sent:
                if index >= len(keyword_tags):
                    return self.get_overlap(keyword_list, output_list, is_word_list=True)

                if self.match_pos(tag, keyword_tags[index][1], strictness=strictness):
                    output_list.append(keyword_tags[index][0])
                    index += 1
                else:
                    output_list.append(word)

        return None

    def from_initials_list(self, initials_list, timeout=3):
        """

        :param list of lists of initials initials_list: e.g. [['a'], ['b']]
        :param float timeout: timeout of this function
        :return list of tuple: sentence generated
        >>> KeywordParse().from_initials_list([['a'], ['re'], ['ex']])
        [('Mrs.', False), ('Freight', False), ('(', False), ('Knight', False), ('Dream-Miss', False), ('Reed', False), (')', False), ('amounts', True), ('butter', True)]
        """
        start = time()
        while time() - start < timeout:
            index = 0
            output_list = []
            tagged_sent = self.brown.get_tagged_sent()
            for word, pos in tagged_sent:
                if index >= len(initials_list):
                    return self.get_overlap(initials_list, output_list, is_word_list=False)

                poses = self.brown.initials_to_pos(initials_list[index])
                if poses is None:
                    new_word_list = [w for w in self.brown.word_list_from_pos(pos)
                                     if any([w.startswith(initial) for initial in initials_list[index]])]
                    if len(new_word_list) > 0:
                        output_list.append(choice(new_word_list))
                        index += 1
                    else:
                        output_list.append(word)
                else:
                    if pos in poses:
                        output_list.append(self.brown.word_from_pos_and_initials(pos, initials_list[index]))
                        index += 1
                    else:
                        output_list.append(word)

        return None

    def from_initials(self, initials, timeout=3):
        """

        :param str initials:
        :param float timeout:
        :return list of tuple:
        >>> KeywordParse().from_initials('xyz')
        [('Charles', False), ('A.', False), ('Black', False), (',', False), ('exchange', True), ('year', True), (',', False), ('zipped', True)]
        """
        initials_list = [[char.lower()] if char.lower() != 'x' else ['ex'] for char in initials]
        return self.from_initials_list(initials_list, timeout)

    @staticmethod
    def match_pos(pos1, pos2, strictness=2):
        """
        Match part-of-speech as defined in https://catalog.ldc.upenn.edu/docs/LDC99T42/tagguid1.pdf
        :param pos1:
        :param pos2:
        :param int | None strictness: None is the strictest
        :return bool:

        >>> KeywordParse.match_pos('NN', 'PRP', 0)
        True
        """
        return pos1[:strictness] == pos2[:strictness]

    @staticmethod
    def get_overlap(initials_list_or_word_list, tokens, is_word_list=True):
        """

        :param list of str | list of lists initials_list_or_word_list:
        :param list of str tokens:
        :param bool is_word_list: If False, initials_list
        :return list of tuple:

        """
        index = 0
        result = []
        for token in tokens:
            if index >= len(initials_list_or_word_list):
                break
            if ((is_word_list and token.lower() == initials_list_or_word_list[index].lower()) or
                    (not is_word_list and
                     any([token.startswith(initial) for initial in initials_list_or_word_list[index]]))):
                result.append((token, True))
                index += 1
            else:
                result.append((token, False))

        if index != len(initials_list_or_word_list):
            raise ValueError('Does not overlap')
        else:
            return result


if __name__ == '__main__':
    print(KeywordParse().from_keyword_list(['Love', 'blind', 'trouble']))
