import os
import pandas as pd
import numpy as np

from .dataloader import DataLoader


class ETHLoader(DataLoader):

    def __init__(self, base_dir, start_idx, end_idx, features: list, dropna=False, download=True,
                 url="https://raw.githubusercontent.com/coinmetrics/data/master/csv/eth.csv"):
        self._dir = os.path.join(base_dir, 'eth_data')
        self._features = features
        addr = None
        if download:
            addr = url
        else:
            addr = os.path.join(self._dir, 'data.csv')
        self._data = pd.read_csv(addr)[[*features]].iloc[start_idx:end_idx]
        if dropna:
            self._data = self._data.dropna().reset_index()
        else:
            self._data = self._data.reset_index()

        if not os.path.isdir(self._dir):
            os.mkdir(self._dir)
        if 'index' in self._data.columns:
            self._data.drop('index', axis=1, inplace=True)
        self._data.to_csv(os.path.join(self._dir, 'data.csv'))
        # var for the iterator
        self._idx = 0
        self._duration = len(self._data)

    def __len__(self):
        return len(self._data)

    def __next__(self):
        # end of the iteration
        if self._idx == len(self._data):
            raise StopIteration()

        payload = self._data.iloc[self._idx]
        self._idx += 1
        return self._idx - 1, payload

    def get_feature(self, feature_name):
        return self._data[feature_name]

    def get_duration(self):
        return self._duration
    
    def get_idx(self):
        return pd.Series(np.arange(len(self)))

    def reset(self):
        self._idx = 0
        