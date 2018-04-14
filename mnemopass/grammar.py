from secrets import choice
from random import randrange

from mnemopass.const import PARTS_OF_SPEECH


class ValidGrammar:
    def __init__(self):
        self.basic_grammar = [
            ('adv', 'adj'),
            ('adj', 'noun'),
            ('verb', 'adv'),
            ('verb', 'noun'),
            ('noun', 'verb'),
            ('adj', 'adj'),
            ('adv', 'adv'),
            ('noun', 'noun')
        ]
        # verb is not appendable.

    def comes_after(self, pos):
        for pos1, pos2 in self.basic_grammar:
            if pos1 == pos:
                yield pos2

    def generate(self, length):
        if length == 1:
            return [choice(PARTS_OF_SPEECH)]
        elif length > 1:
            sentence = list(choice(self.basic_grammar))
            for _ in range(length - 2):
                current_word = sentence[-1]
                while True:
                    next_word = choice(list(self.comes_after(current_word)))
                    if 'verb' in sentence:
                        if next_word == 'verb':
                            continue

                    sentence.append(next_word)
                    break

            return sentence
        else:
            raise ValueError('Length must be positive')

    def is_valid(self, grammar):
        for i in range(len(grammar)-1):
            if (grammar[i], grammar[i+1]) not in self.basic_grammar:
                return False

        if 'verb' in grammar:
            grammar.remove('verb')
            if 'verb' in grammar:
                return False

        return True


if __name__ == '__main__':
    vg = ValidGrammar()
    for i in range(5):
        print(vg.generate(3))
