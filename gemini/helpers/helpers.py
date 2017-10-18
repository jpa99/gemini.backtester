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
    return initial_capital * (multiplier + 1.0) - initial_capital


class Period:
    """
    Strange, for what use class
    """

    def __init__(self, data):
        self.data = data

    def loc(self, i):
        """
        Return data to date
        :param i:
        :return:
        """
        if i > 0:
            raise ValueError("Error: Cannot look forward!")
        if i <= -(len(self.data)):
            raise ValueError("Error: Cannot look too far back!")
        return self.data.iloc[i - 1]
