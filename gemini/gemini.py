import logging
import types

import gemini.settings as settings
from gemini import exchange
from gemini.helpers import helpers

FEES = getattr(settings, "FEES", dict())

logger = logging.getLogger(__name__)


class Gemini:
    """
    Main class of Backtester
    """
    data = None  # storage for history data
    account = None  # exchange account simulator
    sim_params = {
        'capital_base': 10e5,
        'data_frequency': 'd',  # TODO Make to use it with pd.resample
        'fee': FEES,  # Fees in percent of trade amount
    }
    records = []

    def __init__(self, initialize=None, logic=None, analyze=None,
                 sim_params=None):
        """
        Create backtester with own methods.

        sim_params :: Backtester's settings:
            * start_session :: not use
            * end_session :: not use
            * capital_base :: default 10k
            * data_frequency :: not use
            *

        :param initialize:
        :param logic:
        :param analyze:
        :param sim_params:
        """

        if initialize is not None:
            self.initialize = types.MethodType(initialize, self)

        if logic is not None:
            self.logic = types.MethodType(logic, self)

        if analyze is not None:
            self.analyze = types.MethodType(analyze, self)

        if sim_params is not None:
            self.sim_params = sim_params

    def initialize(self):
        """
        First method which will be called after start algorithm
        :return:
        """
        pass

    def logic(self, data):
        """
        Central method which will be called for every tick
        in trading interval.

        :param data:
        :return:
        """
        pass

    def run(self, data, **kwargs):
        """
        Main method to start backtest
        :param data :: history data with ticks or bars
        :param logic:
        :param trading_interval:
        :param lookback_period:
        :return:
        """
        self.data = data
        self.account = exchange.Account(
            self.sim_params.get('capital_base', 10e5),
            fee=self.sim_params.get('fee', None)
        )
        self.records = []

        self.initialize()

        # Start cycle

        # TODO Add filter between start & end session from sim_params
        # TODO Resample data for data_frequency from sim_params

        for index, tick in self.data.iterrows():
            # print(Index)
            # Update account variables
            self.account.date = tick['date']
            # update total value in account
            # TODO Replace by pandas DataFrame
            self.account.equity.append(
                (tick['date'], self.account.total_value(tick['close'])))

            # Execute trading logic
            lookback_data = self.data[0:index + 1]
            try:
                self.logic(lookback_data)
            except Exception as ex:
                logger.exception(ex)

            # Cleanup empty positions
            self.account.purge_positions()

        self.results()
        self.analyze(**kwargs)

    def results(self):
        """
        Print results of backtest to console
        :return:
        """
        title = "{0} results {0}".format("=" * 25)
        print(title + "\n")
        begin_price = self.data.iloc[0]['open']
        final_price = self.data.iloc[-1]['close']

        percentchange = helpers.percent_change(begin_price, final_price)
        print("Buy and Hold : {0:.2f}%".format(percentchange * 100))
        print("Net profit   : {0:.2f}".format(
            helpers.profit(self.account.initial_capital, percentchange)))

        percentchange = helpers.percent_change(self.account.initial_capital,
                                               self.account.total_value(
                                                   final_price))
        print("Strategy     : {0:.2f}%".format(percentchange * 100))
        print("Net profit   : {0:.2f}".format(
            helpers.profit(self.account.initial_capital, percentchange)))

        longs = len(
            [t for t in self.account.opened_trades if t.type_ == 'Long'])
        sells = len(
            [t for t in self.account.closed_trades if t.type_ == 'Long'])
        shorts = len(
            [t for t in self.account.opened_trades if t.type_ == 'Short'])
        covers = len(
            [t for t in self.account.closed_trades if t.type_ == 'Short'])

        print("Longs        : {0}".format(longs))
        print("Sells        : {0}".format(sells))
        print("Shorts       : {0}".format(shorts))
        print("Covers       : {0}".format(covers))
        print("--------------------")
        print("Total Trades : {0}\n".format(longs + sells + shorts + covers))
        print("-" * len(title))

    def analyze(self):
        pass
