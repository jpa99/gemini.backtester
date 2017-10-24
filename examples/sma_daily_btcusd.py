import talib

from gemini.gemini import Gemini
from gemini.helpers import cryptocompare as cc
from gemini.helpers.analyze import analyze_mpl, analyze_bokeh


def logic(algo, data):
    """
    Main algorithm method, which will be called every tick.

    :param algo: Gemini object with account & positions
    :param data: History for current day
    """
    # Load into period class to simplify indexing
    if len(data) < 20:
        # Skip short history
        return

    today = data.iloc[-1]
    current_price = today['close']
    short = talib.SMA(data['close'].values, timeperiod=5)
    long = talib.SMA(data['close'].values, timeperiod=30)

    if short[-1] > long[-1] and short[-2] < long[-2]:
        print(today['date'], 'BUY signal', len(data))
        entry_capital = algo.account.buying_power
        if entry_capital >= 0:
            algo.account.enter_position('Long', entry_capital, current_price)

    if short[-1] < long[-1] and short[-2] > long[-2]:
        print(today['date'], 'SELL signal', len(data))
        for position in algo.account.positions:
            if position.type_ == 'Long':
                algo.account.close_position(position, 1, current_price)

    algo.records.append({
        'date': today['date'],
        'price': current_price,
        'sma20': short[-1],
        'sma100': long[-1],
    })


pair = ['BTC', 'USD']  # Use ETH pricing data on the BTC market
days_history = 300  # From there collect X days of data
fees_spread = 0.0025 + 0.001  # Fees 0.25% + Bid/ask spread to account for http://data.bitcoinity.org/markets/spread/6m/USD?c=e&f=m20&st=log&t=l using Kraken 0.1% as worse case
exchange = 'Bitstamp'

# Request data from cryptocompare.com
df = cc.load_dataframe(pair, days_history, exchange)

# Algorithm settings
sim_params = {
    'capital_base': 10000
}
gemini = Gemini(logic=logic, sim_params=sim_params, analyze=analyze_bokeh)

# start backtesting custom logic with 1000 (BTC) intital capital
gemini.run(df,
           title='SMA 5x30 History: {}'.format(days_history),
           show_trades=True)
