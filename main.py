from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import argparse
import datetime  # For datetime objects
import os.path  # To manage paths

import backtrader as bt
import backtrader.feeds as btfeeds

import pandas


class TestStrategy(bt.Strategy):

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.order = None
        self.dataclose = self.datas[0].close
        self.dataopen = self.datas[0].open
        self.zone = self.datas[0].close - self.datas[0].open

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
                self.stoploss = self.dataclose[0]
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
        self.log('Open, %.2f' % self.dataopen[0])
        self.log('Zone, %.2f' % self.zone[0])
        self.log('shift, %.2f' % self.zone[-1])

        print(len(self))
        print(self.order)
        print(self.position)
        #
        """Enters Long position if below conditions are met"""
        if self.zone[0] < 0:
            print("Bar is red")
            # current close less than previous close

            if self.zone[1] > 0:
                print("Next candle is green")
                # Next close less than the previous close
                if 1.5*abs(self.zone[0]) < abs(self.zone[1]):
                    print("Buy Zone found")

                # BUY, BUY, BUY!!! (with all possible default parameters)
                    self.log('BUY CREATE, %.2f' % self.dataclose[0])
                    # self.buy()
                    #currently buying at next days open instead of last days close see May 03 for example buying?? limit at 37729 instead of
                    self.order = self.buy_bracket(limitprice=self.dataopen[0], price=self.dataopen[0], stopprice=self.dataclose[0])
                    # print(self.order)
                    print(self.order)

        # if self.position.isbuy():
        #     if self.zone[0] < self.dataclose[0]:








def runstrat():
    args = parse_args()

    # Create a cerebro entity
    cerebro = bt.Cerebro(stdstats=False)

    # Add a strategy
    cerebro.addstrategy(TestStrategy)

    # Get a pandas dataframe
    datapath = (r'C:\Users\Nael\PycharmProjects\BackTesting\venv\datas\HistoricalData.csv')

    # Simulate the header row isn't there if noheaders requested
    skiprows = 1 if args.noheaders else 0
    header = None if args.noheaders else 0

    dataframe = pandas.read_csv(datapath,
                                skiprows=skiprows,
                                header=header,
                                parse_dates=True,
                                index_col=0)

    if not args.noprint:
        print('--------------------------------------------------')
        print(dataframe)
        print('--------------------------------------------------')

    # Pass it to the backtrader datafeed and add it to the cerebro
    data = bt.feeds.PandasData(dataname=dataframe)

    cerebro.adddata(data)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    # Print out the final result
    print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


def parse_args():
    parser = argparse.ArgumentParser(
        description='Pandas test script')

    parser.add_argument('--noheaders', action='store_true', default=False,
                        required=False,
                        help='Do not use header rows')

    parser.add_argument('--noprint', action='store_true', default=False,
                        help='Print the dataframe')

    return parser.parse_args()


if __name__ == '__main__':
    runstrat()
