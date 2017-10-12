import requests
import time


def get_now(pair):
    """
    Return last info for crypto currency pair
    :param pair:
    :return:
    """
    return requests.get('https://poloniex.com/public?command=returnTicker').json()[pair]


def get_past(pair, period, days_back, days_data):
    """
    Return historical charts data from poloniex.com
    :param pair:
    :param period:
    :param days_back:
    :param days_data:
    :return:
    """
    now = int(time.time())
    end = now - (24 * 60 * 60 * days_back)
    start = end - (24 * 60 * 60 * days_data)
    params = {
        'command': 'returnChartData',
        'currencyPair': pair,
        'start': start,
        'end': end,
        'period': period
    }

    response = requests.get('https://poloniex.com/public', params=params)
    return response.json()
