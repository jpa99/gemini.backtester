import time
import bokeh.plotting
import numpy as np
import exchange
import helpers


class Run():
    def __init__(self, Data):
        self.Data = Data

    def Start(self, InitialCapital, Logic, TradingInterval, LookbackPeriod):

        self.Account = exchange.Account(InitialCapital)

        # Enter backtest ---------------------------------------------
        TradingIntervalCounter = TradingInterval
        for Index, Today in self.Data.iterrows():
            # print(Index)
            # Update account variables
            self.Account.Date = Today['date']
            self.Account.Equity.append(self.Account.TotalValue(Today['close']))

            # Execute trading logic
            Lookback = self.Data[0:Index + 1]
            if TradingIntervalCounter == TradingInterval:
                Logic(self.Account, Lookback, LookbackPeriod)
                TradingIntervalCounter = 0
            else:
                TradingIntervalCounter += 1

            # Cleanup empty positions
            self.Account.PurgePositions()
            # ------------------------------------------------------------

    def Results(self):
        print("-------------- Results ----------------\n")
        BeginPrice = self.Data.iloc[0]['open']
        FinalPrice = self.Data.iloc[-1]['close']

        percentchange = helpers.percent_change(BeginPrice, FinalPrice)
        print("Buy and Hold : {0}%".format(round(percentchange * 100, 2)))
        print("Net profit   : {0}".format(
            round(helpers.profit(self.Account.InitialCapital, percentchange), 2)))

        percentchange = helpers.percent_change(self.Account.InitialCapital,
                                               self.Account.TotalValue(FinalPrice))
        print("Strategy     : {0}%".format(round(percentchange * 100, 2)))
        print("Net profit   : {0}".format(
            round(helpers.profit(self.Account.InitialCapital, percentchange), 2)))

        Longs = len([T for T in self.Account.OpenedTrades if T.Type == 'Long'])
        Sells = len([T for T in self.Account.ClosedTrades if T.Type == 'Long'])
        Shorts = len([T for T in self.Account.OpenedTrades if T.Type == 'Short'])
        Covers = len([T for T in self.Account.ClosedTrades if T.Type == 'Short'])

        print("Longs        : {0}".format(Longs))
        print("Sells        : {0}".format(Sells))
        print("Shorts       : {0}".format(Shorts))
        print("Covers       : {0}".format(Covers))
        print("--------------------")
        print("Total Trades : {0}".format(Longs + Sells + Shorts + Covers))
        print("\n---------------------------------------")

    def Chart(self, Title, ShowTrades=False):
        bokeh.plotting.output_file("chart.html", title=Title)
        p = bokeh.plotting.figure(x_axis_type="datetime", plot_width=1000, plot_height=400,
                                  title=Title)
        p.grid.grid_line_alpha = 0.3
        p.xaxis.axis_label = 'Date'
        p.yaxis.axis_label = 'Equity'
        Shares = self.Account.InitialCapital / self.Data.iloc[0]['open']
        BaseEquity = [Price * Shares for Price in self.Data['open']]
        p.line(self.Data['date'], BaseEquity, color='#CAD8DE', legend='Buy and Hold')
        p.line(self.Data['date'], self.Account.Equity, color='#49516F', legend='Strategy')
        p.legend.location = "top_left"

        if ShowTrades:
            for Trade in self.Account.OpenedTrades:
                try:
                    x = time.mktime(Trade.Date.timetuple()) * 1000
                    y = self.Account.Equity[
                        np.where(self.Data['date'] == Trade.Date.strftime("%Y-%m-%d"))[0][0]]
                    if Trade.Type == 'Long':
                        p.circle(x, y, size=6, color='green', alpha=0.5)
                    elif Trade.Type == 'Short':
                        p.circle(x, y, size=6, color='red', alpha=0.5)
                except:
                    pass

            for Trade in self.Account.ClosedTrades:
                try:
                    x = time.mktime(Trade.Date.timetuple()) * 1000
                    y = self.Account.Equity[
                        np.where(self.Data['date'] == Trade.Date.strftime("%Y-%m-%d"))[0][0]]
                    if Trade.Type == 'Long':
                        p.circle(x, y, size=6, color='blue', alpha=0.5)
                    elif Trade.Type == 'Short':
                        p.circle(x, y, size=6, color='orange', alpha=0.5)
                except:
                    pass

        bokeh.plotting.show(p)
