from nltk.tokenize.moses import MosesDetokenizer

try:
    from secrets import choice
except ImportError:
    from random import choice

from randomsentence.word import WordTool


class SentenceTool:
    def __init__(self):
        self.detokenizer = MosesDetokenizer()
        self.word_tool = WordTool()

    def rate(self, tokens):
        """
        Convert tokens to Sentence.with_rating
        :param list of str tokens:
        :return dict:

        >>> SentenceTool().rate(['The', 'White', 'Russians', 'and', 'the', 'Ukrainians', 'would', 'say', 'that', 'Stalin', 'and', 'Molotov', 'were', 'far', 'less', 'reliable', 'defenders', 'of', 'Russia', 'than', 'Curzon', 'and', 'Clemenceau', '.'])
        [('the', 0), ('white', 347), ('russians', inf), ('and', 2), ('the', 0), ('ukrainians', inf), ('would', 85), ('say', 495), ('that', 9), ('stalin', inf), ('and', 2), ('molotov', inf), ('were', 87), ('far', 859), ('less', 534), ('reliable', 3638), ('defenders', inf), ('of', 1), ('russia', 2330), ('than', 98), ('curzon', inf), ('and', 2), ('clemenceau', inf), ('.', inf)]
        """
        rating = [(word.lower(), self.word_tool.commonness(word)) for word in tokens]

        return rating

    def detokenize(self, tokens):
        """
        Join words/sentence_tokens
        :param list of str tokens:
        :return str:
        >>> SentenceTool().detokenize(['The', 'White', 'Russians', 'and', 'the', 'Ukrainians', 'would', 'say', 'that', 'Stalin', 'and', 'Molotov', 'were', 'far', 'less', 'reliable', 'defenders', 'of', 'Russia', 'than', 'Curzon', 'and', 'Clemenceau', '.'])
        'The White Russians and the Ukrainians would say that Stalin and Molotov were far less reliable defenders of Russia than Curzon and Clemenceau.'
        """
        return self.detokenizer.detokenize(tokens, return_str=True)

    def detokenize_tagged(self, tagged_tokens):
        """

        :param tagged_tokens:
        :return:
        """
        return self.detokenize([token for token, tag in tagged_tokens])


if __name__ == '__main__':
    import doctest
    doctest.testmod()
