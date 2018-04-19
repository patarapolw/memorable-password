import os
import yaml

from memorable_password.dir import ROOT


class Mnemonic:
    def __init__(self):
        with open(os.path.join(ROOT, 'mnemonic.yaml')) as f:
            self.mnemonic = yaml.safe_load(f)

    def starters(self, system):
        """

        :param str system: mnemonic system. Major system for numbers.
        :return list: a list of all possible starters

        >>> Mnemonic().starters('major_system')
        ['s', 'z', 'x', 't', 'th', 'n', 'm', 'r', 'l', 'd', 'c', 'k', 'g', 'q', 'b', 'h', 'v', 'w', 'p', 'f']
        """
        result = []
        for k, v in self.mnemonic[system].items():
            result.extend(v)

        return result

    def word_to_key(self, system, word):
        """

        :param str system: mnemonic system. Major system for numbers.
        :param str word: the word to test
        :return str: the corresponding key

        >>> Mnemonic().word_to_key('major_system', 'hello')
        '8'
        >>> Mnemonic().word_to_key('major_system', 'Hello')
        ''
        >>> Mnemonic().word_to_key('major_system', '8')
        ''
        """
        for k, v in self.mnemonic[system].items():
            for starter in v:
                if word.startswith(starter):
                    return k

        return ''

    def reality_to_starter(self, system, mem):
        """

        :param str system: mnemonic system. Major system for numbers.
        :param str mem: resultant mem. Numbers for Major system
        :return list: a list of all possible starters

        >>> Mnemonic().reality_to_starter('major_system', '8')
        ['b', 'h', 'v', 'w']
        >>> Mnemonic().reality_to_starter('major_system', 'H')
        []
        """
        return self.mnemonic[system].get(mem, [])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
