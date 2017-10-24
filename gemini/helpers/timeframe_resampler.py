import pandas as pd


def resample(data, period, date='date'):
    """
    Return resampled dataframe
    available periods: H - hour, D - day, W - week, M - month
    :param data:
    :param period:
    :param date: 'date' for poloniex, 'time' for cryptocompare
    :return:
    """
    data = pd.DataFrame(data).set_index([date], drop=False)
    data.index = pd.to_datetime(data.index, unit='s')
    try:
        if date == 'date':
            data = data.resample(period).apply({
                'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum',
            }).dropna()
        else:
            data = data.resample(period).apply({
                'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last'
            }).dropna()
    except ValueError as e:
        print('Time frame error: {}. Will use default value'.format(e))
    data['date'] = data.index
    print(data)
    return data
