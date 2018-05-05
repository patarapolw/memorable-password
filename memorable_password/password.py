"""
Generate a new password/PIN with associated sentence.
"""

from randomsentence import SentenceTool, Brown
from diceware_utils.policy import Conformize
from diceware_utils.wordlist import Wordlist
from time import time

from memorable_password.mnemonic import Mnemonic, InitialSoftener
from memorable_password.sentence import ToSentence

__doctest_skip__ = ['GeneratePassword.refresh', 'GeneratePassword.new_diceware_password',
                    'GeneratePassword.new_common_diceware_password', 'GeneratePassword.new_pin']


class GeneratePassword:
    def __init__(self, do_markovify=True):
        self.sentence_tool = SentenceTool()
        self.conformizer = Conformize()
        self.mnemonic = Mnemonic()
        self.initial_softener = InitialSoftener()
        self.to_sentence = ToSentence()
        self.wordlist = Wordlist()

        self.brown = Brown(do_markovify=do_markovify)

        self.tokens = None

    def refresh(self, count_common=4, min_common=1000, timeout=20):
        """
        Generate a new sentence
        :param int count_common: the number of words with minimal commonness
        :param int min_common: the minimal commonness based on Google common word list
        :param float timeout: time in seconds to timeout
        :return list of str: return tokens on success

        >>> GeneratePassword().refresh()
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

    def new_common_diceware_password(self, number_of_words=6, hint=''):
        """
        Return a suggested password
        :param int number_of_words: number of words generated
        :param str hint:
        :return tuple: a suggested password and a sentence

        >>> GeneratePassword().new_common_diceware_password()
        ('rive2sidelauraarchitectss!mplytheOreticalassessMeNt$', [('Mynheer', False), (',', False), ('Sir', False), ('Francis', False), (',', False), ('the', False), ('riverside', True), ('laura', True), (',', False), ('the', False), ('very', False), ('architects', True), ('of', False), ('the', False), ('river', False), ('on', False), ('his', False), ('right', False), ('purling', False), ('simply', True), ('to', False), ('the', False), ('bay', False), ('past', False), ('fish', False), ('weirs', False), ('and', False), ('rocks', False), (',', False), ('and', False), ('ahead', False), ('the', False), ('theoretical', True), ('assessments', True)])
        """
        keywords = [self.wordlist.get_random_word() for _ in range(number_of_words)]
        password = self.conformizer.conformize(keywords)
        if hint:
            keywords = [hint] + keywords
        return password, self.to_sentence.from_keywords(keywords)

    @staticmethod
    def overlap_keywords(keywords, tokens):
        index = 0
        for token in tokens:
            if index >= len(keywords):
                break

            is_overlap = (keywords[index].lower() == token.lower())
            yield token, is_overlap
            if is_overlap:
                index += 1

    def new_initial_password(self, min_length=8, min_common=500, timeout=20, refresh_timeout=3):
        self.refresh(count_common=min_length, min_common=min_common, timeout=refresh_timeout)
        rating = self.sentence_tool.rate(self.tokens)

        start = time()
        while time() - start < timeout:
            password = ''
            for token, commonness in rating:
                if commonness >= min_common:
                    key = self.initial_softener.word_to_key(token.lower())
                    if key is not None:
                        password += key

            if len(password) < min_length:
                self.refresh(count_common=min_length, min_common=min_common, timeout=refresh_timeout)
                rating = self.sentence_tool.rate(self.tokens)
            else:
                return self.conformizer.conformize(password), list(self.overlap_initials(password, self.tokens))

        return None

    def new_pin(self, min_length=4, min_common=1000, timeout=20, refresh_timeout=3):
        """
        Return a suggested PIN

        :param int min_length: minimum length of the PIN generated
        :param int min_common: the minimal commonness to be considered convertible to a PIN
        :param float timeout: main timeout in seconds
        :param float refresh_timeout: timeout to new sentence
        :return str: a string of digits

        >>> GeneratePassword().new_pin()
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

    def overlap_initials(self, initials, tokens):
        index = 0
        for token in tokens:
            if index >= len(initials):
                break

            is_overlap = (initials[index] == self.initial_softener.word_to_key(token.lower()))
            yield token, is_overlap
            if is_overlap:
                index += 1

    def generate(self, password_from, password_type, password_material, hint=''):
        if password_from == 'random':
            if password_type == 'initials':
                tagged_password = self.new_initial_password()
            elif password_type == 'diceware':
                tagged_password = self.new_common_diceware_password(hint=hint)
            else:
                tagged_password = self.new_pin()

            if tagged_password is not None:
                password, tagged_sentence = tagged_password
            else:
                password = tagged_sentence = ''

        elif password_from == 'keywords':
            keywords = [keyword.strip() for keyword in password_material.replace(' ', ',').split(',')]
            if len(keywords) < 6:
                keywords += [self.wordlist.get_random_word() for _ in range(6-len(keywords))]

            tagged_sentence = self.to_sentence.from_keywords(keywords)
            if password_type in ['initials', 'diceware']:
                password = self.conformizer.conformize(keywords)
            else:
                password = ''.join([self.initial_softener.word_to_key(keyword.lower()) for keyword in keywords])
        elif password_from == 'pin':
            tagged_sentence = self.to_sentence.from_pin(password_material)
            if password_type == 'diceware':
                keywords = [token for token, overlap in tagged_sentence if overlap]
                password = self.conformizer.conformize(keywords)
            else:
                password = password_material
        else:  # from 'initials'
            initials = password_material
            tagged_sentence = self.to_sentence.from_initials(initials)
            if password_type == 'initials':
                password = self.conformizer.conformize(initials)
            elif password_type == 'diceware':
                keywords = [token for token, overlap in tagged_sentence if overlap]
                password = self.conformizer.conformize(keywords)
            else:
                password = ''.join([self.mnemonic.word_to_key('major_system', char.lower()) for char in initials])

        return password, tagged_sentence

    def get_policy(self):
        return self.conformizer.get_policy()

    def update_policy(self, policy_dict):
        self.conformizer.update_policy(policy_dict)


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
