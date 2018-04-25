from passwordstrength.entropy import Entropy
from randomsentence import WordTool
from pronounceable import generate_word, PronounceableWord

from memorable_password import GeneratePassword

entropy = Entropy()
gp = GeneratePassword()
word_tool = WordTool()
pw = PronounceableWord()


def entropy_initial(length=15):
    """

    :return:
    length=10: Worst: 49.0044, 50.9478, 52.0044; Best: 59.8346, 59.8346, 60.7781
    length=15: Worst: 76.4500, 78.3934, 78.3934; Best: 91.1671, 91.1671, 93.0539
    """
    password = gp.new_initial_password(min_length=length)[0]
    if password is not None:
        return entropy.log_entropy(password[:length])
    else:
        return False


def entropy_diceware_policy_conformized(number_of_words=4):
    """

    :return:
    number_of_words=4: Worst: 148.7987, 149.8719, 159.6005; Best: 243.2369, 249.9373, 299.5016
    """
    password = gp.new_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return entropy.log_entropy(password)
    else:
        return False


def entropy_common_diceware_policy_conformized(number_of_words=6):
    """

    :return:
    number_of_words=4: Worst: 91.0373, 104.1952, 107.8390; Best: 204.5035, 216.8478, 222.7913
    number_of_words=6: Worst: 167.7018, 168.0013, 169.2443; Best: 282.6540, 290.2979, 308.5856
    """
    password = gp.new_common_diceware_password(number_of_words=number_of_words)[0]
    if password is not None:
        return entropy.log_entropy(password)
    else:
        return False


def entropy_common_diceware_all_lower(number_of_words=4):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Worst: 81.9075, 81.9075, 81.9075; Best: 161.8150, 171.2158, 190.0176
    number_of_words=6: Worst: 100.7092, 124.2114, 138.3128; Best: 241.7224, 251.1233, 255.8237
    number_of_words=4, non_common: Worst: 138.3128, 148.7136, 153.4141; Best: 241.7224, 249.6093, 284.0264
    """
    password = ''.join([word_tool.get_random_word() for _ in range(number_of_words)])
    return entropy.log_entropy(password)


def entropy_pronounceable_word_all_lower(number_of_words=6):
    """

    :param number_of_words:
    :return:
    number_of_words=4: Worst: 53.7048, 53.7048, 58.4053; Best: 91.3084, 91.3084, 96.0088
    number_of_words=6: Worst: 81.9075, 86.6079, 91.3084; Best: 124.2114, 128.9119, 138.3128
    """
    password = ''.join([generate_word() for _ in range(number_of_words)])
    return entropy.log_entropy(password)


def entropy_pronounceable_length_all_lower(min_length=20):
    """

    :param min_length:
    :return:
    min_length=15: Worst: 72.5066, 72.5066, 72.5066; Best: 91.3084, 91.3084, 91.3084
    min_length=20: Worst: 96.0088, 96.0088, 96.0088; Best: 114.8106, 114.8106, 114.8106
    """
    password = pw.length(min_length, min_length+5)
    return entropy.log_entropy(password)


def check_entropy(func, rep=50):
    entropy_list = []
    for i in range(rep):
        print('Rep:', i+1)
        log_entropy = func()
        if log_entropy:
            entropy_list.append(log_entropy)

    entropy_list = sorted(entropy_list)
    print('Worst: {:.4f}, {:.4f}, {:.4f}'.format(*entropy_list[:3]), end='; ')
    print('Best: {:.4f}, {:.4f}, {:.4f}'.format(*entropy_list[-3:]))


if __name__ == '__main__':
    # from tests import timeit
    # timeit(test_initial_entropy, validator=lambda x: x)
    from functools import partial

    check_entropy(entropy_pronounceable_length_all_lower)
