from gemini.gemini import Gemini
from gemini.helpers import poloniex as px
from gemini.helpers.analyze import analyze_mpl


def logic(algo, data):
    """
    Main algorithm method, which will be called every tick.

    :param algo: Gemini object with account & positions
    :param data: History for current day
    """
    # Process dataframe to collect signals
    if len(data) < 2:
        # Skip short history
        return

    today = data.iloc[-1]  # Current candle
    yesterday = data.iloc[-2]  # Previous candle
    #print('from {} to {}'.format(data.index[-2], data.index[-1]))

    # print(Today)
    if today['close'] < yesterday['close']:
        exit_price = today['close']
        for position in algo.account.positions:
            if position.type_ == 'Long':
                algo.account.close_position(position, 1, exit_price)

    elif today['close'] > yesterday['close']:
        risk = 0.03
        entry_price = today['close']
        entry_capital = algo.account.buying_power * risk
        if entry_capital >= 0:
            algo.account.enter_position('Long', entry_capital, entry_price)


# Data settings
pair = "BTC_ETH"  # Use ETH pricing data on the BTC market
period = 1800  # Use 1800 second candles
days_history = 100  # From there collect 60 days of data

# Request data from Poloniex
df = px.load_dataframe(pair, period, days_history, timeframe='D')

# Algorithm settings
sim_params = {
    'capital_base': 1000,
    'fee': {
        'Long': 0.0025,
        'Short': 0.0025,
    },
    'data_frequency': '30T'
}
gemini = Gemini(logic=logic, sim_params=sim_params, analyze=analyze_mpl)

# start backtesting custom logic with 1000 (BTC) intital capital
gemini.run(df, show_trades=True)
