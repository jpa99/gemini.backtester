import talib

from gemini.gemini import Gemini
from gemini.helpers import poloniex as px
from gemini.helpers.analyze import analyze_bokeh


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
    short = talib.SMA(data['close'].values, timeperiod=20)
    long = talib.SMA(data['close'].values, timeperiod=100)

    if short[-1] > long[-1] and short[-2] < long[-2]:
        print(today.name, 'BUY signal')
        entry_capital = algo.account.buying_power
        if entry_capital >= 0:
            algo.account.enter_position('Long', entry_capital, current_price)

    if short[-1] < long[-1] and short[-2] > long[-2]:
        print(today.name, 'SELL signal')
        for position in algo.account.positions:
            if position.type_ == 'Long':
                algo.account.close_position(position, 1, current_price)

    algo.records.append({
        'date': today.name,
        'price': current_price,
        'sma20': short[-1],
        'sma100': long[-1],
    })


# Data settings
pair = "BTC_ETH"  # Use ETH pricing data on the BTC market
period = 1800  # Use 1800 second candles
days_history = 300  # From there collect 60 days of data

# Request data from Poloniex
df = px.load_dataframe(pair, period, days_history, timeframe='H')

# Algorithm settings
sim_params = {
    'capital_base': 100,
    'fee': {
        'Long': 0.0025,
        'Short': 0.0025,
    },
    'data_frequency': '30T'
}
gemini = Gemini(logic=logic, sim_params=sim_params, analyze=analyze_bokeh)

# start backtesting custom logic with 1000 (BTC) intital capital
gemini.run(df,
           title='SMA 5x30 History: {}'.format(days_history),
           show_trades=True)
