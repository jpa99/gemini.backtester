<p align="center"><img src="https://github.com/Crypto-AI/Gemini/blob/master/media/logo.png" width="150px"><p>

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
![Python](https://img.shields.io/badge/python-v3.5+-blue.svg)
![Dependencies](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)
[![GitHub Issues](https://img.shields.io/github/issues/friendly-pig/gemini.backtester.svg)](https://github.com/friendly-pig/gemini.backtester/issues)
![Contributions welcome](https://img.shields.io/badge/contributions-welcome-orange.svg)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)
<br>
<p align="center"><img src="https://github.com/Crypto-AI/Gemini/blob/master/media/schematic.gif" width="550px"><p>


## Examples

### Input Data (Optional)
If you have your own data that has/hasn't been processed, you should conform to the following structure. Basically, load your data into a Pandas dataframe object and be sure to convert the dates to datetime format and include the following lowercase column titles.
```text
               date         high          low         open        close
2017-07-08 11:00:00  2480.186778  2468.319314  2477.279567  2471.314030  
2017-07-08 11:30:00  2471.314030  2455.014057  2471.202796  2458.073602
2017-07-08 12:00:00  2480.000000  2456.000000  2458.073602  2480.000000
```

### Loading Data into the Backtester
If you don't have your own data, we've included a useful function for grabbing historical charting data from the Poloniex exchange. In this example, we'll trade the BTC/ETH pair on a 30 minute timeframe. To demonstrate the versatility of our data grabber, we will ignore the last 30 days of data in our backtest and look at the 60 days before then. With the poloniex helper function, it's easy to do that.
```python
from gemini.gemini import Gemini
import poloniex as px

def logic(algo, data):
    """
    Main algorithm method, which will be called every tick.
    
    :param algo: Gemini object with account & positions
    :param data: History for current day
    """
    pass

pair = "BTC_ETH"    # Use ETH pricing data on the BTC market
period = 1800       # Use 1800 second candles
days_history = 360       # history length

# Request data from Poloniex
df = px.load_dataframe(pair, period, days_history)

# Algorithm settings
sim_params = {
    'capital_base': 1000,
}
gemini = Gemini(logic=logic, sim_params=sim_params, analyze=analyze)

# start backtesting custom logic with 1000 (BTC) intital capital
gemini.run(df)
```

### Creating your Strategy
In addition to loading the data, you must define the strategy you want to test. 
To do this, we'll create a logic function that can be passed to the backtester 
when you start. The backtester will proceed step-wise through the dataset, copying 
the current/past datapoints into a variable called "Lookback" to prevent lookahead 
bias. If the data hasn't already been processed, you may process it within the 
logic function (this makes the simulation more accurate but significantly increases 
runtime). With those, you may execute long, sell, short, and 
cover positions directly on the "Account" class based on your strategy.


```python
def logic(algo, data):
    # Process dataframe to collect signals
    if len(data) < 2:
        # Skip short history
        return

    today = data.iloc[-1]  # Current candle
    yesterday = data.iloc[-2]  # Previous candle

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

```

#### Analyzing your Strategy
After the backtest, you can analyze your strategy by printing the results to console. 
As of now, these include simple statistics of your run but we plan to implement more 
complicated metrics for a stronger understanding of performance.

```text
Buy and Hold : -3.03%
Net profit   : -30.26
Strategy     : 40.0%
Net profit   : 400.01
Longs        : 156
Sells        : 137
Shorts       : 0
Covers       : 0
--------------------
Total Trades : 293
```

#### Visualizing the Equity Curve
You can visualize the performance of your strategy by comparing the equity curve with a buy and hold baseline. The equity curve simply tracks your account value throughout the backtest and will optionally show where your algorithm made its trades including longs, sells, shorts, and covers.
```python
gemini.run(df, show_trades=False)
```
<p align="center"><img src="https://raw.githubusercontent.com/friendly-pig/gemini.backtester/master/media/example.png"><p>

## Contributing
Please take a look at our [contributing](https://github.com/friendly-pig/gemini.backtester/blob/master/CONTRIBUTING.md) guidelines if you're interested in helping!
