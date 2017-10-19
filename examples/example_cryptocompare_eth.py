from gemini.gemini import Gemini
from gemini.helpers import cryptocompare as cc
from gemini.helpers.analyze import analyze


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
    print('from {} to {}'.format(yesterday['date'], today['date']))

    if today['close'] < yesterday['close']:
        exit_price = today['close']
        for position in algo.account.positions:
            if position.type_ == 'Long':
                algo.account.close_position(position, 1, exit_price)

    if today['close'] > yesterday['close']:
        entry_price = today['close'] + (today['close'] * fees_spread)
        entry_capital = algo.account.buying_power
        if entry_capital > 0:
            algo.account.enter_position('Long', entry_capital, entry_price)


# Data settings
pair = ['ETH', 'BTC']  # Use ETH pricing data on the BTC market
days_history = 360  # From there collect X days of data
fees_spread = 0.0025 + 0.001  # Fees 0.25% + Bid/ask spread to account for http://data.bitcoinity.org/markets/spread/6m/USD?c=e&f=m20&st=log&t=l using Kraken 0.1% as worse case
exchange = 'Bitfinex'

# Request data from cryptocompare.com
df = cc.load_dataframe(pair, days_history, exchange)

# Algorithm settings
sim_params = {
    'capital_base': 1000,
}
r = Gemini(logic=logic, sim_params=sim_params, analyze=analyze)

# start backtesting custom logic with 1000 (BTC) intital capital
r.run(df,
      title='History: {}'.format(days_history),
      show_trades=True)
