import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib
import pandas
from datetime import datetime
from sdzone import SupplyDemandZone

import pandas as pd

data = pd.read_csv(r'HistoricalData.csv')

class SDZone(bt.strategy):

    def __init__(self):
        """Create strategy of SD zone"""
        long_zone = bt.ind.sdz()

        self.longzonefound

    def next(self):
        if self.data == 1:
            self.buy()
        elif self.data == 0:
            self.sell()

cerebro = bt.Cerebro()

cerebro.adddata(data)
cerebro.addstrategy(SDZone)

cerebro.broker.setcash(100000)
cerebro.addsizer(bt.sizers.PercentSizer,percents = 1)