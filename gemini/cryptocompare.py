import requests
import time


def getNow(pair):
    return requests.get(
        'https://min-api.cryptocompare.com/data/pricehistorical?fsym={}}&tsyms={}'.format(
            *pair)).json()


def getPast(pair, daysBack, daysData, Exchange):
    now = int(time.time())
    end = now - (24 * 60 * 60 * daysBack)
    response = requests.get(
        'https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&toTs={}&limit={}&aggregate=1&e={}'.format(
            pair[0], pair[1], end, daysData, Exchange))
    results = response.json()['data']
    # print(results)
    return results
