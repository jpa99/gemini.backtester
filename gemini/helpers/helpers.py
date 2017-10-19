def percent_change(d1, d2):
    """
    calculate percent change between two values
    :param d1:
    :param d2:
    :return:
    """
    return (d2 - d1) / d1


def profit(initial_capital, multiplier):
    """
    Return profit? Don't understand this
    :param initial_capital:
    :param multiplier:
    :return:
    """
    r = initial_capital * (multiplier + 1.0) - initial_capital
    return r
