from randomsentence import WordTool
from pronounceable import generate_word, PronounceableWord, Complexity

from memorable_password import GeneratePassword

complexity = Complexity()
# gp = GeneratePassword()
word_tool = WordTool()
pw = PronounceableWord()


def complexity_initial(length=15):
    """

    :return:
    length=10: Best: -1, 1, 2; Worst: 16, 16, 17
    length=15: Best: 1, 2, 4; Worst: 20, 20, 25
    """
    password = gp.new_initial_password(min_length=length)[0]
    if password is not None:
        return complexity.complexity(password[:length])
    else:
        return False


def complexity_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: -8, -6, -4; Worst: 20, 21, 31
    """
    password = gp.new_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: -4, -3, 2; Worst: 28, 34, 41
    number_of_words=6: Best: -10, -8, -6; Worst: 23, 31, 46
    """
    password = gp.new_common_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_all_lower(number_of_words=6):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: -20, -18, -18; Worst: -3, -1, 1
    number_of_words=6: Best: -33, -28, -27; Worst: -9, -7, -5
    """
    password = ''.join([word_tool.get_random_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_word_all_lower(number_of_words=4):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: -27, -27, -26; Worst: -7, -6, -4
    number_of_words=6: Best: -11, -11, -11; Worst: -5, -5, -4
    """
    password = ''.join([generate_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_length_all_lower(min_length=15):
    """

    :param min_length:
    :return:
    min_length=15: Worst: Best: -8, -8, -8; Worst: -2, -2, 1
    min_length=20: Worst: Best: -11, -11, -10; Worst: -5, -4, -4
    """
    password = pw.length(min_length, min_length+5)
    return complexity.complexity(password)


def check_complexity(func, rep=50):
    complexity_list = []
    for i in range(rep):
        print('Rep:', i+1)
        complexity_result = func()
        if complexity_result:
            complexity_list.append(complexity_result)

    complexity_list = sorted(complexity_list)
    print('Best: {}, {}, {}'.format(*complexity_list[:3]), end='; ')
    print('Worst: {}, {}, {}'.format(*complexity_list[-3:]))


if __name__ == '__main__':
    # from tests import timeit
    # timeit(test_initial_entropy, validator=lambda x: x)
    from functools import partial

    check_complexity(complexity_pronounceable_length_all_lower)
