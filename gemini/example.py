import pandas as pd
import gemini
import poloniex as px
import helpers

pair = "BTC_ETH"  # Use ETH pricing data on the BTC market
period = 1800  # Use 1800 second candles
daysBack = 30  # Grab data starting 30 days ago
daysData = 3  # From there collect 60 days of data

# Request data from Poloniex
data = px.get_past(pair, period, daysBack, daysData)
print(data)
# Convert to Pandas dataframe with datetime format
data = pd.DataFrame(data)

data['date'] = pd.to_datetime(data['date'], unit='s')


def Logic(Account, Lookback):
    try:
        # Process dataframe to collect signals
        # Lookback = helpers.getSignals(Lookback)

        # Load into period class to simplify indexing
        Lookback = helpers.Period(Lookback)

        Today = Lookback.loc(0)  # Current candle
        Yesterday = Lookback.loc(-1)  # Previous candle
        # print(Today)
        if Today['close'] < Yesterday['close']:
            ExitPrice = Today['close']
            for Position in Account.Positions:
                if Position.Type == 'Long':
                    Account.ClosePosition(Position, 0.5, ExitPrice)

        if Today['close'] > Yesterday['close']:
            Risk = 0.03
            EntryPrice = Today['close']
            EntryCapital = Account.BuyingPower * Risk
            if EntryCapital >= 0:
                Account.EnterPosition('Long', EntryCapital, EntryPrice)

    except ValueError:
        pass  # Handles lookback errors in beginning of dataset


# Load the data into a backtesting class called Run
r = gemini.Run(data)

# Start backtesting custom logic with 1000 (BTC) intital capital
r.Start(1000, Logic)

r.Results()
r.Chart(ShowTrades=False)
