import time
import bokeh.plotting
import numpy as np
import exchange
import helpers


class Run:
    def __init__(self, data):
        self.data = data

    def start(self, initial_capital, logic, trading_interval=None, lookback_period=None):

        self.account = exchange.Account(initial_capital)

        # Enter backtest ---------------------------------------------
        trading_interval_counter = trading_interval
        for index, today in self.data.iterrows():
            # print(Index)
            # Update account variables
            self.account.date = today['date']
            self.account.equity.append(self.account.total_value(today['close']))

            # Execute trading logic
            lookback = self.data[0:index + 1]
            if trading_interval_counter == trading_interval:
                logic(self.account, lookback, lookback_period)
                trading_interval_counter = 0
            else:
                trading_interval_counter += 1

            # Cleanup empty positions
            self.account.purge_positions()
            # ------------------------------------------------------------

    def results(self):
        print("-------------- results ----------------\n")
        begin_price = self.data.iloc[0]['open']
        final_price = self.data.iloc[-1]['close']

        percentchange = helpers.percent_change(begin_price, final_price)
        print("Buy and Hold : {0}%".format(round(percentchange * 100, 2)))
        print("Net profit   : {0}".format(
            round(helpers.profit(self.account.initial_capital, percentchange), 2)))

        percentchange = helpers.percent_change(self.account.initial_capital,
                                               self.account.total_value(final_price))
        print("Strategy     : {0}%".format(round(percentchange * 100, 2)))
        print("Net profit   : {0}".format(
            round(helpers.profit(self.account.initial_capital, percentchange), 2)))

        longs = len([t for t in self.account.opened_trades if t.type == 'Long'])
        sells = len([t for t in self.account.closed_trades if t.type == 'Long'])
        shorts = len([t for t in self.account.opened_trades if t.type == 'Short'])
        covers = len([t for t in self.account.closed_trades if t.Type == 'Short'])

        print("Longs        : {0}".format(longs))
        print("Sells        : {0}".format(sells))
        print("Shorts       : {0}".format(shorts))
        print("Covers       : {0}".format(covers))
        print("--------------------")
        print("Total Trades : {0}".format(longs + sells + shorts + covers))
        print("\n---------------------------------------")

    def chart(self, title=None, show_trades=False):
        bokeh.plotting.output_file("chart.html", title=title)
        p = bokeh.plotting.figure(x_axis_type="datetime", plot_width=1000, plot_height=400,
                                  title=title)
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Equity'
        shares = self.account.initial_capital / self.data.iloc[0]['open']
        base_equity = [price * shares for price in self.data['open']]
        p.line(self.data['date'], base_equity, color='#CAD8DE', legend='Buy and Hold')
        p.line(self.data['date'], self.account.equity, color='#49516F', legend='Strategy')
        p.legend.location = "top_left"

        if show_trades:
            for trade in self.account.opened_trades:
                try:
                    x = time.mktime(trade.date.timetuple()) * 1000
                    y = self.account.equity[
                        np.where(self.data['date'] == trade.date.strftime("%Y-%m-%d"))[0][0]]
                    if trade.type == 'Long':
                        p.circle(x, y, size=6, color='green', alpha=0.5)
                    elif trade.type == 'Short':
                        p.circle(x, y, size=6, color='red', alpha=0.5)
                except:
                    pass

            for trade in self.account.closed_trades:
                try:
                    x = time.mktime(trade.date.timetuple()) * 1000
                    y = self.account.equity[
                        np.where(self.data['date'] == trade.date.strftime("%Y-%m-%d"))[0][0]]
                    if trade.type == 'Long':
                        p.circle(x, y, size=6, color='blue', alpha=0.5)
                    elif trade.type == 'Short':
                        p.circle(x, y, size=6, color='orange', alpha=0.5)
                except:
                    pass

        bokeh.plotting.show(p)
