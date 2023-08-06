from abc import ABCMeta, abstractmethod


class Exchange(metaclass=ABCMeta):

    def __init__(self):
        self.ccxt_inst = None

    def get_balance(self, market, ticker):
        return self.ccxt_inst.fetch_balance()[ticker]['total']
