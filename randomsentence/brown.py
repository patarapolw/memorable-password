from nltk.corpus import brown
import yaml
from time import time
import markovify

try:
    from secrets import choice
except ImportError:
    from random import choice

from randomsentence.dir import database_path

__doctest_skip__ = ['Brown.get_tagged_sent', 'Brown.word_from_pos_and_initials']


class Brown:
    def __init__(self, do_markovify=False):
        self.tagged_sents = brown.tagged_sents()
        if do_markovify:
            self.model = markovify.Chain(self.tagged_sents, 2)

        self.words_from_pos = dict()
        for word, tag in brown.tagged_words():
            self.words_from_pos.setdefault(tag, []).append(word)
        with open(database_path('settings.yaml')) as f:
            self.startswith = yaml.safe_load(f)['startswith']['brown']

    def get_tagged_sent(self):
        """

        :return list of tuples of non-space-separated strings:
        >>> Brown().get_tagged_sent()
        [('As', 'CS'), ('she', 'PPS'), ('was', 'BEDZ'), ('rather', 'QL'), ('tired', 'VBN'), ('this', 'DT'), ('evening', 'NN'), (',', ','), ('her', 'PP$'), ('simple', 'JJ'), ('``', '``'), ('Thank', 'VB'), ('you', 'PPO'), ('for', 'IN'), ('the', 'AT'), ('use', 'NN'), ('of', 'IN'), ('your', 'PP$'), ('bath', 'NN'), ("''", "''"), ('--', '--'), ('when', 'WRB'), ('she', 'PPS'), ('sat', 'VBD'), ('down', 'RP'), ('opposite', 'IN'), ('him', 'PPO'), ('--', '--'), ('spoken', 'VBN'), ('in', 'IN'), ('a', 'AT'), ('low', 'JJ'), ('voice', 'NN'), (',', ','), ('came', 'VBD'), ('across', 'RB'), ('with', 'IN'), ('coolnesses', 'NNS'), ('of', 'IN'), ('intelligence', 'NN'), ('and', 'CC'), ('control', 'NN'), ('.', '.')]
        """
        try:
            return list(self.model.gen())
        except AttributeError:
            return choice(self.tagged_sents)

    def initials_to_pos(self, initials):
        """

        :param list of strings initials: e.g. ['a'] or ['t', 'th']
        :return list: list of allowed POS
        >>> Brown().initials_to_pos(['t', 'th'])
        ['VBD', 'NN', 'IN', 'JJ', 'NNS', 'VBZ', 'VBN', 'VB', 'RB', 'VBG', 'QL', 'JJT', 'NN-HL', 'VBN-HL', 'JJR', 'NN$', 'NNS-HL', 'VBG-HL', 'NNS$', 'JJ-HL', 'FW-NN', 'FW-NNS', 'NN-NC', 'NN+BEZ']
        >>> Brown().initials_to_pos(['a'])
        ['VBD', 'NN', 'JJ', 'NNS', 'VBZ', 'VBN', 'VB', 'RB', 'VBG', 'QL', 'NN-HL']
        """
        for v in self.startswith.values():
            for allowed_initials in v['allowed']:
                if set(initials) == set(allowed_initials):
                    return v['pos']

        return None

    def word_from_pos_and_initials(self, pos, initials, timeout=5):
        """

        :param str pos:
        :param list of strings initials: e.g. ['a'] or ['t', 'th']
        :param float timeout: number of seconds to timeout
        :return str: word
        >>> Brown().word_from_pos_and_initials("VBD", ['t', 'th'])
        'told'
        """
        start = time()
        while time() - start < timeout:
            word = choice(self.words_from_pos[pos])
            if any([word.startswith(initial) for initial in initials]):
                return word

        raise TimeoutError

    def word_list_from_pos(self, pos, strictness=2):
        word_list = []
        for k, v in self.words_from_pos.items():
            if k[:strictness] == pos:
                word_list.extend(v)
        return word_list


if __name__ == '__main__':
    import doctest
    doctest.testmod()
