import yaml
from time import time
from random import randrange
import re
import string
try:
    from secrets import choice
except ImportError:
    from random import choice

from memorable_password.dir import database_path

__doctest_skip__ = ['Conformize.conformize']


class Conformize:
    def __init__(self):
        self.policy = Policy()
        with open(database_path('leetspeak.yaml')) as f:
            self.leetspeak = yaml.safe_load(f)['min']

    def conformize(self, password, timeout=3):
        """

        :param str password:
        :param float timeout:
        :return str | None:
        >>> Conformize().conformize('uNlikelypiezoelectricgrounds')
        'uN1iKe1yP!EZoe13ctriCgr0UND5'
        """
        password = re.sub('{}'.format(re.escape(string.punctuation)), '', password)

        start = time()
        while time()-start < timeout:
            if not self.policy.is_conform(password):
                char_to_substitute_index = randrange(len(password))
                char_to_substitute = password[char_to_substitute_index]
                substitutions = self.leetspeak.get(char_to_substitute, []) \
                                + [char_to_substitute.lower()
                                   if char_to_substitute.isupper() else char_to_substitute.upper()]

                password = password[:char_to_substitute_index] \
                           + choice(substitutions) \
                           + password[char_to_substitute_index+1:]
            else:
                return password

        print('Non-conformed password:', password)
        return None


class Policy:
    def __init__(self):
        with open(database_path('policy.yaml')) as f:
            self.policy = yaml.safe_load(f)['policy']

    @staticmethod
    def both_upper_and_lower(password):
        """

        :param str password:
        :return bool:

        >>> Policy.both_upper_and_lower('aB')
        True
        >>> Policy.both_upper_and_lower('ab')
        False
        >>> Policy.both_upper_and_lower('AB')
        False
        """
        if any([char.islower() for char in password]) and any([char.isupper() for char in password]):
            return True

        return False

    @staticmethod
    def digit_count(password):
        """

        :param password:
        :return:
        >>> Policy.digit_count('12')
        2
        """
        return len([char for char in password if char.isdigit()])

    @staticmethod
    def punctuation_count(password):
        """

        :param password:
        :return:
        >>> Policy().punctuation_count('@')
        1
        """
        return len([char for char in password if char in string.punctuation])

    def is_conform(self, password):
        if self.policy['both_upper_and_lower']:
            if not self.both_upper_and_lower(password):
                return False

        if self.digit_count(password) < self.policy['digit_count']:
            return False

        if self.punctuation_count(password) < self.policy['punctuation_count']:
            return False

        return True
