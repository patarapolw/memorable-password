import yaml

from memorable_password.dir import database_path


class Mnemonic:
    def __init__(self):
        with open(database_path('mnemonic.yaml')) as f:
            self.mnemonic = yaml.safe_load(f)

    def starters(self, system):
        """

        :param str system: mnemonic system. Major system for numbers.
        :return list: a list of all possible starters

        >>> sorted(Mnemonic().starters('major_system'))
        ['b', 'c', 'd', 'f', 'g', 'h', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'th', 'v', 'w', 'x', 'z']
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

        >>> Mnemonic().word_to_key('major_system', '8')

        """
        for k, v in self.mnemonic[system].items():
            for starter in v:
                if word.startswith(starter):
                    return k

        return None

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


class InitialSoftener(Mnemonic):
    def word_to_key(self, word, system='initials'):
        """

        :param word:
        :param system:
        :return:
        >>> InitialSoftener().word_to_key('Exaltation')
        'x'
        >>> InitialSoftener().word_to_key('Normalword')
        'n'
        """
        for k, v in self.mnemonic[system].items():
            for starter in v:
                if word.lower().startswith(starter):
                    return k

        if word[0].isalpha():
            return word.lower()[0]
        else:
            return ''

    def reality_to_starter(self, mem, system='initials'):
        """

        :param mem:
        :param system:
        :return:
        >>> InitialSoftener().reality_to_starter('x')
        ['ex']
        >>> InitialSoftener().reality_to_starter('n')
        ['n']
        """
        return self.mnemonic[system].get(mem.lower(), [mem.lower()[0]] if mem[0].isalpha() else [])


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
