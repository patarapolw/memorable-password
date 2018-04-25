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
    length=10: Best: 1.19, 1.31, 1.45; Worst: 2.72, 2.93, 2.95
    length=15: Best: 1.88, 1.89, 1.99; Worst: 3.17, 3.29, 3.36
    """
    password = gp.new_initial_password(min_length=length)[0]
    if password is not None:
        return complexity.complexity(password[:length])
    else:
        return False


def complexity_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: 3.21, 3.24, 3.73; Worst: 6.21, 6.30, 6.64
    """
    password = gp.new_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: 2.65, 2.86, 2.95; Worst: 4.89, 5.05, 5.87
    number_of_words=6: Best: 3.80, 3.86, 4.02; Worst: 6.46, 6.57, 6.83
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
    number_of_words=4: Best: 2.00, 2.03, 2.05; Worst: 3.90, 4.05, 4.89
    number_of_words=6: Best: 3.55, 3.60, 3.72; Worst: 5.66, 5.69, 5.75
    """
    password = ''.join([word_tool.get_random_common_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_word_all_lower(number_of_words=4):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: 1.16, 1.18, 1.19; Worst: 2.15, 2.15, 2.26
    number_of_words=6: Best: 1.60, 1.89, 1.97; Worst: 3.00, 3.31, 3.43
    """
    password = ''.join([generate_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_length_all_lower(min_length=20):
    """

    :param min_length:
    :return:
    min_length=15: Best: 1.41, 1.58, 1.62; Worst: 2.21, 2.28, 2.41
    min_length=20: Best: 1.91, 2.02, 2.04; Worst: 2.76, 2.77, 2.83
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

    check_complexity(complexity_common_diceware_all_lower)
