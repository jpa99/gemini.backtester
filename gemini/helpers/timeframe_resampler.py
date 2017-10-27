import pandas as pd


def resample(data, period):
    """
    Return resampled dataframe
    available periods: H - hour, D - day, W - week, M - month
    :param data:
    :param period:
    :return:
    """

    data = data.resample(period).apply({
                'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum',
            }).dropna()
    data['date'] = data.index

    return data