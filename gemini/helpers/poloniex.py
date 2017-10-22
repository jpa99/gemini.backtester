import time

import pandas as pd
import requests

pd.set_option('precision', 8)
pd.set_option('display.float_format', lambda x: '%.8f' % x)


def get_now(pair):
    """
    Return last info for crypto currency pair
    :param pair:
    :return:
    """
    return requests.get(
        'https://poloniex.com/public?command=returnTicker').json()[pair]


def get_past(pair, period, days_history=30):
    """
    Return historical charts data from poloniex.com
    :param pair:
    :param period:
    :param days_history:
    :return:
    """
    end = int(time.time())
    start = end - (24 * 60 * 60 * days_history)
    params = {
        'command': 'returnChartData',
        'currencyPair': pair,
        'start': start,
        'end': end,
        'period': period
    }

    response = requests.get('https://poloniex.com/public', params=params)
    return response.json()


def load_dataframe(pair, period, days_history=30):
    """
    Return historical charts data from poloniex.com
    :param pair:
    :param period:
    :param days_history:
    :return: pandas.DataFrame
    """
    data = get_past(pair, period, days_history)

    # print(data)
    # Convert to Pandas dataframe with datetime format
    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['date'], unit='s')

    return df
