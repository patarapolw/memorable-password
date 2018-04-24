from passwordstrength.entropy import Entropy

from memorable_password import GeneratePassword

entropy = Entropy()
gp = GeneratePassword()


def test_initial_entropy():
    """

    :return:
    Entropy: [44.490350688396, 47.490350688396, 47.490350688396]
    [128.6408026502871, 144.09826561493566, 184.64519983169802]
    """
    password = gp.new_initial_password()[0]
    if password is not None:
        return entropy.log_entropy(password)
    else:
        return False


def test_diceware_entropy():
    """

    :return:
    Entropy: [124.99694646051239, 150.4425615228515, 159.57237121961128]
    [264.01013800474516, 264.95355447637877, 288.8118968773095]
    """
    password = gp.new_diceware_password()[0]
    if password is not None:
        return entropy.log_entropy(password)
    else:
        return False


def test_common_diceware_entropy():
    """

    :return:
    number_of_words = 4:
    Entropy: [75.69298899724255, 94.86753432005926, 100.44697082796058]
    [173.94476011355695, 179.28905602147276, 187.40222307820548]
    number_of_words = 6:
    Entropy: [148.19958476935895, 153.19958476935895, 154.60046420564112]
    [261.394772357307, 262.01013800474516, 266.411414997334]
    """
    password = gp.new_common_diceware_password(number_of_words=6)[0]
    if password is not None:
        return entropy.log_entropy(password)
    else:
        return False


if __name__ == '__main__':
    # from tests import timeit
    # timeit(test_initial_entropy, validator=lambda x: x)
    entropy_list = []
    for _ in range(50):
        log_entropy = test_common_diceware_entropy()
        if log_entropy:
            entropy_list.append(log_entropy)

    entropy_list = sorted(entropy_list)
    print(entropy_list[:3], entropy_list[-3:])
