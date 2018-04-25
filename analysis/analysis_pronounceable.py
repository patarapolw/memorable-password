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
    length=10: Best: 0.40, 0.40, 0.40; Worst: 13.40, 15.20, 16.20
    length=15: Best: 3.13, 3.60, 3.67; Worst: 18.87, 18.93, 20.00
    """
    password = gp.new_initial_password(min_length=length)[0]
    if password is not None:
        return complexity.complexity(password[:length])
    else:
        return False


def complexity_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Best: 14.75, 14.80, 14.91; Worst: 30.85, 32.04, 42.59
    """
    password = gp.new_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return complexity.complexity(password)
    else:
        return False


def complexity_common_diceware_policy_conformized(number_of_words=6):
    """

    :return:
    number_of_words=4: Best: 8.48, 9.80, 11.00; Worst: 28.70, 29.43, 30.00
    number_of_words=6: Best: 14.20, 16.33, 16.75; Worst: 36.95, 38.61, 41.93
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
    number_of_words=4: Best: 2.50, 4.09, 4.26; Worst: 11.77, 12.75, 12.80
    number_of_words=6: Best: 8.73, 8.77, 8.83; Worst: 20.49, 21.50, 22.48
    """
    password = ''.join([word_tool.get_random_common_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_word_all_lower(number_of_words=6):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Best: -1.82, -1.00, -0.82; Worst: 4.50, 5.26, 6.20
    number_of_words=6: Best: 2.04, 2.09, 2.14; Worst: 9.80, 10.86, 10.89
    """
    password = ''.join([generate_word() for _ in range(number_of_words)])
    return complexity.complexity(password)


def complexity_pronounceable_length_all_lower(min_length=20):
    """

    :param min_length:
    :return:
    min_length=15: Worst: Best: -0.74, -0.59, -0.40; Worst: 4.60, 5.33, 5.33
    min_length=20: Worst: Best: 1.09, 1.20, 2.09; Worst: 8.00, 8.04, 8.09
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

    check_complexity(complexity_initial)
