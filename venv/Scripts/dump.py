from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt
import pandas as pd


# Create a Stratey
class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries

        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.zone = self.datas[0].open - self.datas[0].close

        # print(c)
        # print("Zone")
        # print(self.zone)
        # print("Shift")
        # print(self.shift)
        # self.shift = self.datas[0].open

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        self.log('Open, %.2f' % self.dataopen[0])
        self.log('Zone, %.2f' % self.zone[0])
        self.log('shift, %.2f' % self.zone[-1])
        #
        if self.zone[0] > 0:
            # current close less than previous close

            if self.zone[-1] < 0:
                # previous close less than the previous close
                if self.zone[0] < 1.5 * self.zone[-1]:

                # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    self.buy()


if __name__ == '__main__':
    # Create a cerebro entity
    args = parse_args()
    cerebro = bt.Cerebro()

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Datas are in a subfolder of the samples. Need to find where the script is
    # because it could have been called from anywhere
    datapath = os.path.join(r'C:\Users\Nael\PycharmProjects\BackTesting\venv\Scripts\HistoricalData.csv')

    # Create a Data Feed

    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0
    dataframe = pd.read_csv(datapath,
                                skiprows=skiprows,
                                header=header,
                                parse_dates=True,
                                index_col=0)

    # Add the Data Feed to Cerebro
    cerebro.adddata(dataname=dataframe)

    # Set our desired cash start
    cerebro.broker.setcash(100000.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
