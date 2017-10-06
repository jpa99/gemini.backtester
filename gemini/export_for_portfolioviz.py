import pandas as pd
import gemini
import cryptocompare as cc
import helpers
from datetime import *

pair = ['BTC', 'USD']  # Use ETH pricing data on the BTC market
daysBack = 0  # Grab data starting X days ago
daysData = 365 * 5  # From there collect X days of data
# Exchange = 'Bitstamp'
# Request data from cryptocompare
data = cc.getPast(pair, daysBack, daysData, Exchange='CCCAGG')

# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)
data = data.set_index(['time'])
data.index = pd.to_datetime(data.index, unit='s')
# data['date'] = pd.to_datetime(data['time'], unit='s')
data_MS = data.resample('M').last()
# print(data1)
data_MS['Period'] = data_MS.index.strftime('%Y-%m')
data_MS['Return'] = data_MS['close'].pct_change()
csv_out = data_MS.to_csv(columns=['Period', 'Return'])
print(csv_out)

#
# def Logic(Account, Lookback, LookbackPeriod):
#     try:
#         # Load into period class to simplify indexing
#         Lookback = helpers.Period(Lookback)
#
#         Today = Lookback.loc(0) # Current candle
#         Yesterday = Lookback.loc(-LookbackPeriod) # Previous candle
#         print('Lookback from {} to {}'.format(Yesterday['date'],Today['date']))
#
#         if Today['close'] < Yesterday['close']:
#             ExitPrice = Today['close']
#             for Position in Account.Positions:
#                 if Position.Type == 'Long':
#                     print("{} Sell {}BTC @ ${} = ${} balance".format(Today['date'],Position.Shares,ExitPrice,Position.Shares*ExitPrice))
#                     Account.ClosePosition(Position, 1, ExitPrice)
#
#         if Today['close'] > Yesterday['close']:
#             EntryPrice   = Today['close']+(Today['close']*FeesSpread)
#             EntryCapital = Account.BuyingPower
#             if EntryCapital > 0:
#                 Account.EnterPosition('Long', EntryCapital, EntryPrice)
#                 print("{} Buy ${} of BTC @ ${} = {}BTC balance".format(Today['date'],EntryCapital,EntryPrice,EntryCapital/EntryPrice))
#     except ValueError:
#         pass # Handles lookback errors in beginning of dataset
#
# # Load the data into a backtesting class called Run
# r = gemini.Run(data)
#
# # Start backtesting custom logic with 1000 (BTC) intital capital and 2 day trading interval
# r.Start(1000, Logic, TradingInterval, LookbackPeriod)
#
# r.Results()
# r.Chart('LookbackPeriod: {}, TradingInterval: {}'.format(LookbackPeriod,TradingInterval),ShowTrades=True)
