import logging
import time

import bokeh.plotting
import numpy as np
import pandas as pd
from bokeh.models import LinearAxis, Range1d

logger = logging.getLogger(__name__)


def analyze(algo, title=None,
            show_trades=False):
    """
    Draw charts for backtest results
    :param title:
    :param show_trades:
    :return:
    """
    # FIXME Please. Too much time for chart when show_trades=True

    bokeh.plotting.output_file("chart.html", title=title)
    p = bokeh.plotting.figure(x_axis_type="datetime", plot_width=1000,
                              plot_height=400,
                              title=title)
    p.grid.grid_line_alpha = 0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Equity'
    shares = algo.account.initial_capital / algo.data.iloc[0]['close']
    base_equity = [price * shares for price in algo.data['close']]

    if algo.records:
        # Setting the second y axis range name and range
        p.extra_y_ranges = {
            "Records": Range1d(start=0, end=algo.data['close'].max())}
        # Adding the second axis to the plot.
        p.add_layout(LinearAxis(y_range_name="Records"), 'right')

        records = pd.DataFrame(algo.records)
        for c in records.columns:
            if c == 'date':
                continue

            p.line(records['date'], records[c], color='grey',
                   legend=c, y_range_name="Records")

    # print(algo.data[['date', 'close', 'sma50', 'sma150']])

    p.line(algo.data['date'], base_equity, color='#CAD8DE',
           legend='Buy and Hold')
    p.line(algo.data['date'], algo.account.equity, color='#49516F',
           legend='Strategy')
    p.legend.location = "top_left"

    if show_trades:
        for trade in algo.account.opened_trades:
            try:
                x = time.mktime(trade.date.timetuple()) * 1000
                y = algo.account.equity[
                    np.where(algo.data['date'] == trade.date.strftime(
                        "%Y-%m-%d"))[0][0]]
                if trade.type_ == 'Long':
                    p.circle(x, y, size=6, color='green', alpha=0.5)
                elif trade.type_ == 'Short':
                    p.circle(x, y, size=6, color='red', alpha=0.5)
            except:
                pass

        for trade in algo.account.closed_trades:
            try:
                x = time.mktime(trade.date.timetuple()) * 1000
                y = algo.account.equity[
                    np.where(algo.data['date'] == trade.date.strftime(
                        "%Y-%m-%d"))[0][0]]
                if trade.type_ == 'Long':
                    p.circle(x, y, size=6, color='blue', alpha=0.5)
                elif trade.type_ == 'Short':
                    p.circle(x, y, size=6, color='orange', alpha=0.5)
            except:
                pass

    bokeh.plotting.show(p)
