import pandas as pd
import gemini
import cryptocompare as cc
import helpers
from datetime import *

pair = ['ETH', 'USD']  # Use ETH pricing data on the BTC market
daysBack = 0  # Grab data starting X days ago
daysData = 365 * 2  # From there collect X days of data
LookbackPeriod = 18  # How many days to lookback for momentum
TradingInterval = 1  # Run trading logic every X days
FeesSpread = 0.0025 + 0.001  # Fees 0.25% + Bid/ask spread to account for http://data.bitcoinity.org/markets/spread/6m/USD?c=e&f=m20&st=log&t=l using Kraken 0.1% as worse case
# Request data from cryptocompare
data = cc.getPast(pair, daysBack, daysData)

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)
data['date'] = pd.to_datetime(data['time'], unit='s')


def Logic(Account, Lookback, LookbackPeriod):
    try:
        # Load into period class to simplify indexing
        Lookback = helpers.Period(Lookback)

        Today = Lookback.loc(0)  # Current candle
        Yesterday = Lookback.loc(-LookbackPeriod)  # Previous candle
        print('from {} to {}'.format(Yesterday['date'], Today['date']))

        if Today['close'] < Yesterday['close']:
            ExitPrice = Today['close']
            for Position in Account.Positions:
                if Position.Type == 'Long':
                    Account.ClosePosition(Position, 1, ExitPrice)

        if Today['close'] > Yesterday['close']:
            EntryPrice = Today['close'] + (Today['close'] * FeesSpread)
            EntryCapital = Account.BuyingPower
            if EntryCapital > 0:
                Account.EnterPosition('Long', EntryCapital, EntryPrice)
    except ValueError:
        pass  # Handles lookback errors in beginning of dataset


# Load the data into a backtesting class called Run
r = gemini.Run(data)

# Start backtesting custom logic with 1000 (BTC) intital capital and 2 day trading interval
r.Start(1000, Logic, TradingInterval, LookbackPeriod)

r.Results()
r.Chart('LookbackPeriod: {}, TradingInterval: {}'.format(LookbackPeriod, TradingInterval),
        ShowTrades=True)
