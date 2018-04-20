import yaml
from time import time
from random import randrange
try:
    from secrets import choice
except ImportError:
    from random import choice

from memorable_password.dir import database_path


class Policy:
    def __init__(self):
        with open(database_path('policy.yaml')) as f:
            self.policy = yaml.safe_load(f)['policy']
        with open(database_path('leetspeak.yaml')) as f:
            self.leetspeak = yaml.safe_load(f)['min']

    def is_conform(self, password):
        """

        :param str password:
        :return bool:
        >>> Policy().is_conform('uNlikelypiezoelectricgrounds')
        False
        >>> Policy().is_conform('uN1!ke1y%!3z0313c72!cg20und$')
        True
        """
        # both_upper_and_lower
        if self.policy['both_upper_and_lower']:
            if not (any([char.islower() for char in password]) and any([char.isupper() for char in password])):
                return False

        # includes_digit
        if self.policy['includes_digit']:
            if not any([char.isdigit() for char in password]):
                return False

        # allowed_characters
        if any([(char not in ''.join(self.policy['allowed_characters'])) for char in password]):
            return False

        # includes
        if not any([(must in password) for must in self.policy['includes']]):
            return False

        return True

    def conformize(self, password, timeout=3):
        """

        :param str password:
        :param float timeout:
        :return str | None:
        >>> Policy().conformize('uNlikelypiezoelectricgrounds')
        'uN1!ke1y%!3z0313c72!cg20und$'
        """
        start = time()
        while time()-start < timeout:
            if not self.is_conform(password):
                char_to_substitute_index = randrange(len(password))
                char_to_substitute = password[char_to_substitute_index]
                substitutions = self.leetspeak.get(char_to_substitute, None)
                if substitutions is None:
                    continue

                password = password[:char_to_substitute_index] \
                           + choice(substitutions) \
                           + password[char_to_substitute_index+1:]
            else:
                return password

        return None
