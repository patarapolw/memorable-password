"""
Generate a new password/PIN with associated sentence.
"""

from randomsentence import SentenceTool, WordTool, Brown
from time import time
import string
import re

from memorable_password.mnemonic import Mnemonic
from memorable_password.policy import Conformize

__doctest_skip__ = ['PasswordGenerator.refresh', 'PasswordGenerator.new_password', 'PasswordGenerator.new_pin']


class PasswordGenerator:
    def __init__(self):
        self.sentence_tool = SentenceTool()
        self.word_tool = WordTool()
        self.brown = Brown()
        self.conformizer = Conformize()
        self.mnemonic = Mnemonic()

        self.tokens = None

    def refresh(self, count_common=4, min_common=1000, timeout=20):
        """
        Generate a new sentence
        :param int count_common: the number of words with minimal commonness
        :param int min_common: the minimal commonness based on Google common word list
        :param float timeout: time in seconds to timeout
        :return list of str: return tokens on success

        >>> PasswordGenerator().refresh()
        ['The', 'men', 'in', 'power', 'are', 'committed', 'in', 'principle', 'to', 'modernization', ',', 'but', 'economic', 'and', 'social', 'changes', 'are', 'proceeding', 'only', 'erratically', '.']
        """
        start = time()
        while time() - start < timeout:
            tokens = [token for token, pos in self.brown.get_tagged_sent()]
            current_count = 0
            for word, commonness in self.sentence_tool.rate(tokens):
                if commonness > min_common:
                    current_count += 1
                if current_count >= count_common:
                    self.tokens = tokens
                    return self.tokens

        raise TimeoutError

    def new_password(self, min_length=20, max_length=30, timeout=20,
                     count_common=4, min_common=1000, refresh_timeout=3):
        """
        Return a suggested password
        :param int min_length: minimum password length
        :param int max_length: maximum password length
        :param float timeout: main timeout in seconds
        :param int count_common: number of less common words needed
        :param int min_common: minimum commonness required
        :param float refresh_timeout: timeout to new sentence
        :return tuple: a suggested password and a sentence

        >>> PasswordGenerator().new_password()
        ('Ancho2edpastpredi$%osit!on', [('Social', False), ('process', False), ('is', False), ('always', False), ('anchored', True), ('in', False), ('past', True), ('predisposition', True)])
        """
        self.refresh(count_common, min_common, refresh_timeout)
        current_keywords_with_rating = self.sentence_tool.rate(self.tokens)
        start = time()
        while time() - start < timeout:
            keywords = [keyword for keyword, _ in current_keywords_with_rating if self.word_tool.is_word(keyword)]
            password = self.conformizer.conformize(
                re.sub('{}'.format(re.escape(string.punctuation)), '', ''.join(keywords)))
            if password is None:
                password = ''
            if min_length <= len(password) <= max_length:
                return password, list(self.overlap_keywords(keywords, self.tokens))

            elif min_length > len(password):
                self.refresh(count_common, min_common, refresh_timeout)
                current_keywords_with_rating = self.sentence_tool.rate(self.tokens)
            elif len(password) > max_length:
                min_rating_pair = min(current_keywords_with_rating, key=lambda x: x[1])
                current_keywords_with_rating.remove(min_rating_pair)

        return None


    @staticmethod
    def overlap_keywords(keywords, tokens):
        index = 0
        for token in tokens:
            if index >= len(keywords):
                break

            is_overlap = (keywords[index] == token)
            yield token, is_overlap
            if is_overlap:
                index += 1

    def new_pin(self, min_length=4, min_common=1000, timeout=20, refresh_timeout=3):
        """
        Return a suggested PIN

        :param int min_length: minimum length of the PIN generated
        :param int min_common: the minimal commonness to be considered convertible to a PIN
        :param float timeout: main timeout in seconds
        :param float refresh_timeout: timeout to new sentence
        :return str: a string of digits

        >>> PasswordGenerator().new_pin()
        ('32700', [('His', False), ('mouth', True), ('was', False), ('open', False), (',', False), ('his', False), ('neck', True), ('corded', True), ('with', False), ('the', False), ('strain', True), ('of', False), ('his', False), ('screams', True)])
        """
        self.refresh(count_common=min_length, min_common=min_common, timeout=refresh_timeout)
        rating = self.sentence_tool.rate(self.tokens)

        start = time()
        while time() - start < timeout:
            pin = ''
            for token, commonness in rating:
                if commonness >= min_common:
                    key = self.mnemonic.word_to_key('major_system', token.lower())
                    if key is not None:
                        pin += key

            if len(pin) < min_length:
                self.refresh(count_common=min_length, min_common=min_common, timeout=refresh_timeout)
                rating = self.sentence_tool.rate(self.tokens)
            else:
                return pin, list(self.overlap_pin(pin, self.tokens))

        return None

    def overlap_pin(self, pin, tokens):
        index = 0
        for token in tokens:
            if index >= len(pin):
                break

            is_overlap = (pin[index] == self.mnemonic.word_to_key('major_system', token.lower()))
            yield token, is_overlap
            if is_overlap:
                index += 1


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
