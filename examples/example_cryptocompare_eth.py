from gemini.gemini import Gemini
from gemini.helpers import cryptocompare as cc
from gemini.helpers.analyze import analyze_mpl


def logic(algo, data):
    """
    Main algorithm method, which will be called every tick.

    :param algo: Gemini object with account & positions
    :param data: History for current day
    """
    # Load into period class to simplify indexing
    if len(data) < 2:
        # Skip short history
        return

    today = data.iloc[-1]  # Current candle
    yesterday = data.iloc[-2]  # Previous candle
    print('from {} to {}'.format(yesterday.name, today.name))

    if today['close'] < yesterday['close']:
        exit_price = today['close']
        for position in algo.account.positions:
            if position.type_ == 'Long':
                algo.account.close_position(position, 1, exit_price)

    if today['close'] > yesterday['close']:
        entry_capital = algo.account.buying_power
        if entry_capital > 0.0001:
            algo.account.enter_position('Long', entry_capital, today['close'])


# Data settings
pair = ['ETH', 'BTC']  # Use ETH pricing data on the BTC market
days_history = 360  # From there collect X days of data
exchange = 'Bitfinex'

# Request data from cryptocompare.com
df = cc.load_dataframe(pair, days_history, exchange)

# Algorithm settings
sim_params = {
    'capital_base': 1000,
    'fee': {
        'Long': 0.0025 + 0.001,  # fee + spread
        'Short': 0.0025 + 0.001,
    }
}
r = Gemini(logic=logic, sim_params=sim_params, analyze=analyze_mpl)

# start backtesting custom logic with 1000 (BTC) intital capital
r.run(df,
      title='History: {}'.format(days_history),
      show_trades=True)
