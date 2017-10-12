import requests
import time


def get_now(pair):
    return requests.get(
        'https://min-api.cryptocompare.com/data/pricehistorical?fsym={}&tsyms={}'.format(
            *pair)).json()


def get_past(pair, days_back, days_data, exchange):
    """
    Return historical charts data from cryptocompare.com
    :param pair:
    :param days_back:
    :param days_data:
    :param exchange:
    :return:
    """
    now = int(time.time())
    end = now - (24 * 60 * 60 * days_back)
    params = {
        'fsym': pair[0],
        'tsym': pair[1],
        'toTs': end,
        'limit': days_data,
        'aggregate': 1,
        'e': exchange
    }

    response = requests.get('https://min-api.cryptocompare.com/data/histoday', params=params)
    results = response.json()['Data']
    # print(results)
    return results
