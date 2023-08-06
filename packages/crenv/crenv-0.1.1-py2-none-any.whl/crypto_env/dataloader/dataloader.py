from abc import ABC, abstractmethod

import numpy as np


class DataLoader(ABC):
    _features: list
    _idx: int
    _transaction_fee: np.array = None
    _transaction_fee_type: str = None

    @abstractmethod
    def __init__(self, start_idx, end_idx):
        super(DataLoader, self).__init__()
        self._start_idx = start_idx,
        self._end_idx = end_idx

    def __iter__(self):
        return self

    def get_transaction_fee_type(self):
        return self._transaction_fee_type

    def get_transaction_fee(self, idx=None):
        if idx is None:
            return self._transaction_fee[self._idx]
        return self._transaction_fee[idx]

    def load_transaction_fee(self, values, fee_type='percentage'):
        if not (fee_type == 'percentage' or fee_type == 'fix'):
            raise ValueError("fee_type should be 'fix' or 'percentage'.")

        record_length = len(self)
        values = np.array(values, dtype=np.float32)
        # sanity check
        values_len = values.shape[0]
        if values_len != record_length:
            raise ValueError(f"The length of input should be "
                             f"identical to the length of record. Got {values_len}, "
                             f"but the length of record is {record_length}.")
        self._transaction_fee = values
        self._transaction_fee_type = fee_type

    @abstractmethod
    def __next__(self):
        raise NotImplementedError()

    @abstractmethod
    def __len__(self):
        raise NotImplementedError()

    @abstractmethod
    def reset(self):
        raise NotImplementedError()
    
    def get_idx(self):
        raise NotImplementedError()

    @abstractmethod
    def get_feature(self, feature_name):
        raise NotImplementedError()

    @abstractmethod
    def get_duration(self):
        raise NotImplementedError()

    @property
    def idx(self):
        return self._idx
