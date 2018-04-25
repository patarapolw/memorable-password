from randomsentence import WordTool
from pronounceable import generate_word, PronounceableWord, Complexity

from memorable_password import GeneratePassword

complexity = Complexity()
gp = GeneratePassword()
word_tool = WordTool()
pw = PronounceableWord()


def complexity_initial(length=10):
    """

    :return:
    length=10: Best: 1.78, 1.85, 1.91; Worst: 4.90, 5.52, 5.86
    length=15: Best: 2.24, 2.30, 2.31; Worst: 5.41, 5.79, 6.03
    """
    password = gp.new_initial_password(min_length=length)[0]
    if password is not None:
        return complexity.complexity(password[:length])
    else:
        return False


def complexity_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: 3.71, 3.78, 3.83; Worst: 6.51, 6.60, 6.65
    """
    password = gp.new_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_policy_conformized(number_of_words=6):
    """

    :return:
    number_of_words=4: Best: 2.57, 3.01, 3.18; Worst: 5.97, 6.62, 6.76
    number_of_words=6: Best: 4.08, 4.24, 4.42; Worst: 7.32, 7.97, 8.24
    """
    password = gp.new_common_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_all_lower(number_of_words=4):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: 2.15, 2.15, 2.21; Worst: 4.09, 4.13, 4.14
    number_of_words=6: Best: 2.37, 3.35, 3.37; Worst: 5.61, 6.04, 6.61
    """
    password = ''.join([word_tool.get_random_common_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_word_all_lower(number_of_words=6):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: 1.12, 1.13, 1.13; Worst: 2.34, 2.65, 2.73
    number_of_words=6: Best: 1.53, 1.67, 1.69; Worst: 3.13, 3.17, 3.79
    """
    password = ''.join([generate_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_length_all_lower(min_length=20):
    """

    :param min_length:
    :return:
    min_length=15: Best: 1.00, 1.06, 1.09; Worst: 2.40, 2.43, 2.72
    min_length=20: Best: 1.52, 1.69, 1.69; Worst: 2.88, 3.07, 3.17
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
    print('Best: {:.2f}, {:.2f}, {:.2f}'.format(*complexity_list[:3]), end='; ')
    print('Worst: {:.2f}, {:.2f}, {:.2f}'.format(*complexity_list[-3:]))


if __name__ == '__main__':
    # from tests import timeit
    # timeit(test_initial_entropy, validator=lambda x: x)
    from functools import partial

    check_complexity(complexity_common_diceware_policy_conformized)
