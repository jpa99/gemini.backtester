import pandas as pd

import gemini.gemini as gemini
from gemini.helpers import cryptocompare as cc, helpers

pair = ['ETH', 'BTC']  # Use ETH pricing data on the BTC market
days_back = 1  # Grab data starting X days ago
days_data = 180  # From there collect X days of data
lookback_period = 1  # How many days to lookback for momentum
trading_interval = 1  # Run trading logic every X days
fees_spread = 0.0025 + 0.001  # Fees 0.25% + Bid/ask spread to account for http://data.bitcoinity.org/markets/spread/6m/USD?c=e&f=m20&st=log&t=l using Kraken 0.1% as worse case
exchange = 'Bitfinex'

# Request data from cryptocompare.com
data = cc.get_past(pair, days_back, days_data, exchange)

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)
data['date'] = pd.to_datetime(data['time'], unit='s')


def logic(account, lookback, lookback_period):
    # Load into period class to simplify indexing
    lookback = helpers.Period(lookback)

    today = lookback.loc(0)  # Current candle
    yesterday = lookback.loc(-lookback_period)  # Previous candle
    print('from {} to {}'.format(yesterday['date'], today['date']))

    if today['close'] < yesterday['close']:
        exit_price = today['close']
        for position in account.positions:
            if position.order_type == 'Long':
                account.close_position(position, 1, exit_price)

    if today['close'] > yesterday['close']:
        entry_price = today['close'] + (today['close'] * fees_spread)
        entry_capital = account.buying_power
        if entry_capital > 0:
            account.enter_position('Long', entry_capital, entry_price)


# Load the data into a backtesting class called Run
r = gemini.Run(data)

# start backtesting custom logic with 1000 (BTC) intital capital and 2 day trading interval
r.start(1000, logic, trading_interval, lookback_period)

r.results()
r.chart('Lookback Period: {}, Trading Interval: {}'.format(lookback_period,
                                                           trading_interval),
        show_trades=True)
