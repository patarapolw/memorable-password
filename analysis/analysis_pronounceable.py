from randomsentence import WordTool
from pronounceable import generate_word, PronounceableWord, Complexity

from memorable_password import GeneratePassword

complexity = Complexity()
gp = GeneratePassword()
word_tool = WordTool()
pw = PronounceableWord()


def complexity_initial(length=15):
    """

    :return:
    length=10: Best: 3.69, 3.72, 3.87; Worst: 6.36, 6.56, 6.77
    length=15: Best: 3.74, 4.77, 4.82; Worst: 6.97, 7.25, 7.50
    """
    password = gp.new_initial_password(min_length=length)[0]
    if password is not None:
        return complexity.complexity(password[:length])
    else:
        return False


def complexity_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: 5.65, 6.11, 6.13; Worst: 9.89, 9.96, 11.63
    """
    password = gp.new_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: 4.31, 4.69, 4.97; Worst: 9.13, 9.15, 9.33
    number_of_words=6: Best: 5.71, 5.78, 5.93; Worst: 10.98, 11.27, 12.09
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
    number_of_words=4: Best: 2.25, 2.30, 2.58; Worst: 4.49, 4.52, 4.56
    number_of_words=6: Best: 3.62, 3.65, 3.71; Worst: 6.10, 6.22, 6.23
    """
    password = ''.join([word_tool.get_random_common_word() for _ in range(number_of_words)])
    print(password)
    return complexity.complexity(password)


def complexity_pronounceable_word_all_lower(number_of_words=6):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: 2.16, 2.67, 3.08; Worst: 4.31, 4.51, 4.72
    number_of_words=6: Best: 3.56, 3.58, 3.69; Worst: 5.33, 5.33, 5.74
    """
    password = ''.join([generate_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_length_all_lower(min_length=20):
    """

    :param min_length:
    :return:
    min_length=15: Best: 1.70, 2.44, 2.61; Worst: 4.51, 4.51, 4.92
    min_length=20: Best: 2.33, 2.41, 2.57; Worst: 4.92, 4.92, 4.92
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
    # timeit(complexity_initial, validator=lambda x: x)
    from functools import partial

    check_complexity(complexity_common_diceware_policy_conformized)
