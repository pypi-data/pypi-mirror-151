import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from crypto_env.types import Transaction


class Recorder:
    def __init__(self, price_list, crypto_cap=0, fiat_cap=1000) -> None:
        self._transaction_record = list()
        self._info_record = list()
        self._idx = -1
        self._indexes = None
        self._price_list = price_list

    def reset(self):
        self._transaction_record = list()
        self._info_record = list()
        self._idx = 0
        self._indexes = None

    def insert_transaction(self, transaction: Transaction):
        self._transaction_record.append(transaction)
        self._idx += 1

    def insert_info(self, info):
        if self._indexes is None:
            self._indexes = info.index
        self._info_record.append(list(info))

    def get_transaction_record(self, idx=None):
        if idx is None:
            idx = self._idx
        return pd.DataFrame(self._transaction_record).iloc[0:idx]

    def get_info_record(self, to_dataframe=True):
        if to_dataframe:
            return pd.DataFrame(self._info_record, columns=self._indexes)
        return self._info_record

    def get_expenditure(self, idx=None):
        if idx is None:
            idx = self._idx
        transaction_record = self.get_transaction_record(idx)
        buy_record = transaction_record[transaction_record['signal'] == 0]
        buy_index = buy_record.index.to_list()
        buy_amount = buy_record.value.to_numpy()
        buy_price = self._price_list.iloc[buy_index].to_numpy()
        total_expenditure = np.multiply(buy_amount, buy_price).sum()
        return total_expenditure

    def get_income(self, idx=None):
        if idx is None:
            idx = self._idx
        transaction_record = self.get_transaction_record(idx)
        sell_record = transaction_record[transaction_record['signal'] == 1]
        sell_index = sell_record.index.to_list()
        sell_amount = sell_record.value.to_numpy()
        sell_price = self._price_list.iloc[sell_index].to_numpy()
        total_income = np.multiply(sell_amount, sell_price).sum()
        return total_income

    def get_fiat_balance(self, idx=None):
        if idx is None:
            idx = self._idx
        return self.get_income(idx) - self.get_expenditure(idx)

    def get_crypto_balance(self, idx=None):
        if idx is None:
            idx = self._idx
        transaction_record = self.get_transaction_record(idx)
        sell_amount = transaction_record[transaction_record['signal'] == 1].value.sum()
        buy_amount = transaction_record[transaction_record['signal'] == 0].value.sum()
        return buy_amount - sell_amount

    def get_crypto_value(self, idx=None):
        if idx is None:
            idx = self._idx
        crypto_balance = self.get_crypto_balance(idx)
        crypto_value = crypto_balance * self._price_list.iloc[idx]
        return crypto_value

    def get_roi(self, idx=None):
        if idx is None:
            idx = self._idx
        net_return = self.get_crypto_value(idx) + self.get_fiat_balance(idx)
        cost = self.get_expenditure(idx)
        return net_return / (cost + 0.0001)
