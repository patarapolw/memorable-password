from secrets import choice
# import language_check

from mnemopass.reader import PartOfSpeech
from mnemopass.grammar import ValidGrammar
from mnemopass.const import PARTS_OF_SPEECH


class Sentence:
    def __init__(self):
        self.word_generator = dict()
        for pos in PARTS_OF_SPEECH:
            self.word_generator[pos] = PartOfSpeech(pos)

        self.valid_grammar = ValidGrammar()
        # self.corrector = language_check.LanguageTool('en-US')

    def generate(self, length):
        grammar = self.valid_grammar.generate(length)
        keywords = []
        for pos in grammar:
            keywords.append(choice(self.word_generator[pos]))

        sentence = ' '.join(keywords)
        # language_check.correct(sentence, self.corrector.check(sentence))

        return {
            'keywords': keywords,
            'sentence': sentence
        }


if __name__ == '__main__':
    print(Sentence().generate(5))
