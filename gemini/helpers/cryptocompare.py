import time

import pandas as pd
import requests

pd.set_option('precision', 8)
pd.set_option('display.float_format', lambda x: '%.8f' % x)


def get_now(pair):
    return requests.get(
        'https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}'.format(
            *pair)).json()


def get_past(pair, days_history, exchange):
    """
    Return historical charts data from cryptocompare.com
    :param pair:
    :param days_history:
    :param exchange:
    :return:
    """
    now = int(time.time())
    params = {
        'fsym': pair[0],
        'tsym': pair[1],
        'toTs': now,
        'limit': days_history,
        'aggregate': 1,
        'e': exchange
    }

    response = requests.get('https://min-api.cryptocompare.com/data/histoday',
                            params=params)
    results = response.json()['Data']
    # print(results)
    return results


def load_dataframe(pair, days_history=30, exchange='Bitfinex'):
    """
    Return historical charts data from cryptocompare.com
    :param pair:
    :param period:
    :param days_history:
    :return: pandas.DataFrame
    """
    data = get_past(pair, days_history, exchange)

    # print(data)
    # Convert to Pandas dataframe with datetime format
    df = pd.DataFrame(data)

    df['date'] = pd.to_datetime(df['time'], unit='s')

    return df
