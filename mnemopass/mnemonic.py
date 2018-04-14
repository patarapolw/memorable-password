import yaml
from secrets import choice

from mnemopass.sentence import Sentence
from mnemopass.dir import database_path


class MnemonicGenerator(Sentence):
    def __init__(self):
        super().__init__()

        self.mnemonic = Mnemonic()

    def generate_pin(self, length):
        grammar = self.valid_grammar.generate(length)
        keywords = []
        for pos in grammar:
            appended = False
            while True:
                word = choice(self.word_generator[pos])
                for starter in self.mnemonic.starters('major_system'):
                    if word.startswith(starter):
                        keywords.append(word)
                        appended = True
                        break
                if appended:
                    break

        sentence = ' '.join(keywords)
        # language_check.correct(sentence, self.corrector.check(sentence))

        return {
            'keywords': keywords,
            'sentence': sentence,
            'PIN': ''.join([self.mnemonic.word_to_key('major_system', keyword) for keyword in keywords])
        }

    def memorize_pin(self, pin):
        grammar = self.valid_grammar.generate(len(pin))
        keywords = []
        for i, pos in enumerate(grammar):
            while True:
                word = choice(self.word_generator[pos])
                if any([word.startswith(x) for x in self.mnemonic.reality_to_starter('major_system', pin[i])]):
                    keywords.append(word)
                    break

        sentence = ' '.join(keywords)
        # language_check.correct(sentence, self.corrector.check(sentence))

        return {
            'keywords': keywords,
            'sentence': sentence,
        }


class Mnemonic:
    def __init__(self, filename=database_path('mnemonic.yaml')):
        with open(filename) as f:
            self.mnemonic = yaml.safe_load(f)

    def starters(self, system):
        result = []
        for k, v in self.mnemonic[system].items():
            result.extend(v)

        return result

    def word_to_key(self, system, word):
        for k, v in self.mnemonic[system].items():
            for starter in v:
                if word.startswith(starter):
                    return k

    def reality_to_starter(self, system, mem):
        return self.mnemonic[system].get(mem)


if __name__ == '__main__':
    mg = MnemonicGenerator()
    print(mg.generate_pin(6))
    print(mg.memorize_pin("2613"))
