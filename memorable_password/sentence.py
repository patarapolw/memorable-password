from randomsentence.keyword import KeywordParse

from memorable_password.mnemonic import Mnemonic

__doctest_skip__ = ['ToSentence.*']


class ToSentence:
    def __init__(self):
        self.mnemonic = Mnemonic()
        self.keyword_parse = KeywordParse()

    def from_pin(self, pin, timeout=5):
        """
        Generate a sentence from PIN

        :param str pin: a string of digits
        :param float timeout: total time in seconds
        :return dict: {
            'sentence': sentence corresponding to the PIN,
            'overlap': overlapping positions, starting for 0
        }

        >>> ToSentence().from_pin('3492')
        [("Helva's", False), ('masking', True), ('was', False), ('not', False), ('without', False), ('real', True), (',', False), ('pretty', True), ('novels', True)]
        """
        return self.keyword_parse.from_initials_list([self.mnemonic.reality_to_starter('major_system', number)
                                                      for number in pin],
                                                     timeout)

    def from_initials(self, initials, timeout=5):
        """
        Generate a sentence from initial. X is then converted to EX.

        :param str initials: a string of initials. X is considered EX. Uppercase are converted to lowercase.
        :param float timeout: total time in seconds before raising error
        :return list of tuple:

        >>> ToSentence().from_initials('ABr')
        [('The', False), ('area', True), ('was', False), ('banked', True), ('to', False), ('remember', True)]
        """
        return self.keyword_parse.from_initials(initials, timeout)

    def from_keywords(self, keyword_list, strictness=2, timeout=3):
        """
        Generate a sentence from initial_list.

        :param list keyword_list: a list of keywords to be included in the sentence.
        :param int | None strictness: None for highest strictness. 2 or 1 for a less strict POS matching
        :param float timeout: timeout of this function
        :return list of tuple:

        >>> ToSentence().from_keywords(['gains', 'grew', 'pass', 'greene', 'escort', 'illinois'])
        [('The', False), ('gains', True), ('of', False), ('Bienville', False), ('upon', False), ('grew', True), ('liberal', False), ('pass', True), ('to', False), ('the', False), ('Indians', False), (',', False), ('in', False), ('greene', True), ('to', False), ('drive', False), ('back', False), ('the', False), ('Carolina', False), ('escort', True), (',', False), ('was', False), ('probably', False), ('a', False), ('illinois', True)]
        """
        return self.keyword_parse.from_keyword_list(keyword_list, strictness, timeout)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
